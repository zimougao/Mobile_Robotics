#!/usr/bin/env python
import rospy
import numpy as np
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import SetPen
from math import pow, atan2, sqrt, cos, sin, pi
import os

class TurtleBot:

    def __init__(self):
        # Creates a node with name 'turtlebot_controller' and make sure it is a
        # unique node (using anonymous=True).
        rospy.init_node('turtlebot_controller', anonymous=True)

        # Publisher which will publish to the topic '/turtle1/cmd_vel'.
        self.velocity_publisher = rospy.Publisher('/turtle1/cmd_vel',
                                                  Twist, queue_size=2)
        self.pose_subscriber = rospy.Subscriber('/turtle1/pose',
                                                Pose, self.update_pose)
        self.pose = Pose()   
        self.SetPen = SetPen()     
        # self.goal_pose = rospy.get_param('trajectory_description')
        self.goal_pose = rospy.get_param('trajectory_description_1')
        self.delta_t = self.goal_pose['timestep']    
        self.rate = rospy.Rate(1/self.delta_t)
        self.off = 0

    def update_pose(self, data):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = data
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        self.pose.theta = round(self.pose.theta, 4)

    def euclidean_distance(self,desired_pose):
        """Euclidean distance between current pose and the goal."""
        return sqrt(pow((desired_pose.x - self.pose.x), 2) +
                    pow((desired_pose.y - self.pose.y), 2))

    def set_pen_client(self):
        rospy.wait_for_service('/turtle1/set_pen')    
        try:
            SetPen_data = rospy.ServiceProxy('/turtle1/set_pen',SetPen)
            rospy.loginfo(self.color_adj)
            SetPen_data(255,255,255,4,self.off)
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e

    def set_initial_pose(self):
        rospy.wait_for_service('/turtle1/set_pen')    
        try:
            SetPen_data = rospy.ServiceProxy('/turtle1/set_pen',SetPen)
            SetPen_data(255,50,50,4,1)
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e            

        rospy.wait_for_service('/turtle1/teleport_absolute')    
        try:
            Tele_data = rospy.ServiceProxy('/turtle1/teleport_absolute',TeleportAbsolute)
            Tele_data(2.0,2.0,1.57)
        except rospy.ServiceException, e:
            print "Service call failed: %s"%e  

    def move2goal(self):
        """Moves the turtle to the goal."""
        desired_pose = Pose()
        desired_pose_next = Pose()    
        desired_pose_next_next = Pose() 
        vel_msg = Twist() 
        rospy.loginfo('timestep is: ' + str(self.delta_t)) 
        rospy.loginfo('rate is: ' + str(1/self.delta_t)) 
        tic = rospy.get_time()
        
        # Set sigma and a to design k1 k2 k3
        sigma = 2#2
        a = 3 #3 

        # Set 0.02s for a single step, 0.02*51*4 = 4.08s for single round, 204 steps for one round
        # for j in np.arange(0,1):
        #     rospy.loginfo('Now is loop No ' + str(j))
        for i in np.arange(0,len(self.goal_pose['list_of_x'])-2):     
            # Read goal_troj of x,y,t           
            desired_pose.x = self.goal_pose['list_of_x'][i]
            desired_pose_next.x = self.goal_pose['list_of_x'][i+1]
            desired_pose_next_next.x = self.goal_pose['list_of_x'][i+2]
            desired_pose.y = self.goal_pose['list_of_y'][i]
            desired_pose_next.y = self.goal_pose['list_of_y'][i+1]
            desired_pose_next_next.y = self.goal_pose['list_of_y'][i+2]

            delta_x = desired_pose_next.x - desired_pose.x
            delta_y = desired_pose_next.y - desired_pose.y
            delta_next_x = desired_pose_next_next.x - desired_pose_next.x
            delta_next_y = desired_pose_next_next.y - desired_pose_next.y
            desired_pose.theta = atan2(delta_y,delta_x)
            desired_pose_next.theta = atan2(delta_next_y,delta_next_x)
            angle = desired_pose_next.theta - desired_pose.theta 

            if angle <= -pi:
                angle = angle + 2 * pi
            if angle >= pi:
                angle = angle - 2 * pi

            U_d = sqrt(pow(delta_y,2) + pow(delta_x,2)) /self.delta_t
            W_d = angle/self.delta_t
            # test omiga 
            if delta_x == 0 and delta_y == 0:
                W_d = 0
            if delta_next_x == 0 and delta_next_y == 0:
                W_d = 0
            # Calculate error
            e1_w = desired_pose.x - self.pose.x 
            e2_w = desired_pose.y - self.pose.y 
            e3_w = desired_pose.theta - self.pose.theta 
            if e3_w <= -pi:
                e3_w = e3_w + 2 * pi
            if e3_w >= pi:
                e3_w = e3_w - 2 * pi

            e1 = cos(desired_pose.theta) * e1_w + sin(desired_pose.theta) * e2_w
            e2 = -sin(desired_pose.theta) * e1_w + cos(desired_pose.theta) * e2_w
            e3 = e3_w

            # # Calculate k
            k1 = 2 * sigma * a
            k2 = (a*a - W_d*W_d)/(U_d + 1e-8)
            k3 = k1

            # Calculate u w
            u_1 = -k1 * e1
            u_2 = -k2 * e2 - k3 * e3
            u = U_d * cos(e3) - u_1
            w = W_d - u_2

            # Publish vel_msg            
            vel_msg.linear.x = u
            vel_msg.linear.y = 0
            vel_msg.linear.z = 0

            # Angular velocity in the z-axis.
            vel_msg.angular.x = 0
            vel_msg.angular.y = 0
            vel_msg.angular.z = w

            # Change the color of pen
            self.color_adj = self.euclidean_distance(desired_pose)
            self.color_adj = int(130*self.color_adj)
            if self.color_adj > 250:
                self.color_adj = 250
            if 4.6 <=self.pose.x <= 7.1 and self.pose.y <= 2.1:
                self.off = 1
            else:
                self.off = 0
            self.set_pen_client()

            self.velocity_publisher.publish(vel_msg)
                
            # Publish at the desired rate.
            self.rate.sleep()
        pass    



        rospy.spin()

if __name__ == '__main__':
    try:
        x = TurtleBot()
        x.set_initial_pose()
        x.move2goal()
    except rospy.ROSInterruptException:
        pass