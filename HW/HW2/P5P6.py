#!/usr/bin/env python
import numpy as np
#==============================================================================
# Problem 5
#==============================================================================
#R = lambda t: np.matrix([[np.cos(t),-np.sin(t),0],[np.sin(t),np.cos(t),0],[0,0,1]])
#    
#r = R(np.pi/6)
##r = R(np.pi/3)
##r = R(np.pi/4)
#r.T
#print('r ',r)
#print('r.T ',r.T)
#print('inv(r) ',np.linalg.inv(r))
#print('det(r) ',np.linalg.det(r))
#n = r[:,0]
#s = r[:,1]
#a = r[:,2]
#print('n ',n)
#print('s ',s)
#print('a ',a)
#print('norm(n) ',np.linalg.norm(n))
#print('norm(s) ',np.linalg.norm(s))
#print('norm(a) ',np.linalg.norm(a))
#print('np.dot(n.T,s) ', np.dot(n.T,s) )
#print('np.dot(s.T,a) ', np.dot(n.T,s) )
#print('np.dot(s.T,n) ', np.dot(n.T,s) )

#==============================================================================
# Problem 6
#==============================================================================
def S(v):
    S = np.zeros((3,3))
    S[0][1] = -v[2]
    S[0][2] = v[1]
    S[1][0] = v[2]
    S[1][2] = -v[0]
    S[2][0] = -v[1]
    S[2][1] = -v[0]
    return S
    
v1 = np.array([1,2,3])
v2 = np.array([3,2,1])
A = S(v1)
B = S(v2)
C = np.cross(v1,v2)
D = np.dot(A, v2)
print(C)
print(D)

