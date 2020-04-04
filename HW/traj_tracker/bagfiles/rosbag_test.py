import rosbag
bag = rosbag.Bag('mr.bag')
for topic, msg, t in bag.read_messages(topics=['/turtle1/pose']):
    print msg.y,',,',
    # print msg.y
bag.close()


# rosbag play mr.bag
# rostopic echo /turtle1/pose/msg/x > output_x.txt
# rostopic echo /turtle1/pose/msg/y > output_y.txt
