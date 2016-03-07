#!/usr/bin/env python

"""
This script draws a cylindrical object in Gazebo, and keeps a node with the location of its mass center in x,y,z coordinates (absolute from an origin at the base of the robot. The node is updated via a state machine. 

Written by Dejanira Araiza-Illan, March 2015.
"""

import rospy
import smach
import smach_ros
import random
import os
from bert2_simulator.msg import *
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.srv import GetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3
from std_msgs.msg import Int8

correction = 0

def main():
	rospy.init_node('object', anonymous=True)
	#Initial location (reset)	
	setmodel = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)	
	setmodel(ModelState('object',Pose(Point(0.0,0.0,0.0005),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	#Run loop for all the simulation time length
	while not rospy.is_shutdown():
    		rospy.sleep(0.01)
    		rospy.Subscriber('robot_has_piece', Int8,correct_gazebo)
    		if correction == 0:
    			getmodel = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
			data = getmodel('object','')
			piece=rospy.Publisher('piece_location', Point,queue_size=1,latch=True) 
			piece.publish(data.pose.position.x+0.3,data.pose.position.y-0.3,data.pose.position.z+0.555)
			print str(data.pose.position.x+0.3)+','+str(data.pose.position.y-0.3)+','+str(data.pose.position.z+0.555)
		else:
    			setmodel = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
    			#setmodel(ModelState('object',Pose(Point(0.0,0.0,0.0005),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))	
    			#setmodel(ModelState('object',Pose(Point(0.18,0.47,0.15),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
    			piece=rospy.Publisher('piece_location', Point,queue_size=1,latch=True) 
			piece.publish(0.48,0.17,0.705)
			print str(0.48)+','+str(0.17)+','+str(0.705)
		rospy.sleep(0.01)
		rospy.Subscriber('resetpiece', Int8,reset)
	
    			
def correct_gazebo(data):
	global correction
	if data.data == 1:
		correction = 1
	else:
		correction = 0
		
def reset(data):

	if data.data == 1:
		setmodel = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)	
		setmodel(ModelState('object',Pose(Point(0.0,0.0,0.0005),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
    	

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
