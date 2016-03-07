#!/usr/bin/env python

"""
This script has the functions to change the gaze (head location) and hand location of the human in Gazebo. Inherited to the human.py script.

Created by Dejanira Araiza Illan, July 2015.
"""


import rospy
from bert2_simulator.msg import *
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Point
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Vector3
from std_msgs.msg import Int8


def move_head(data):
	angle = data.angle
	if angle<=40.0:
		setmodel = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)	
		setmodel(ModelState('human_head',Pose(Point(0.4,0.6,-0.25),Quaternion(0.0,-0.15,-0.25,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	else:
		setmodel = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)	
		setmodel(ModelState('human_head',Pose(Point(0.0,0.0,0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	
def move_hand(data):
	x = data.x
	y = data.y
	z = data.z
	gx = x-1.15
	gy = y+0.43
	gz = z-0.73
	setmodel2 = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)	
	setmodel2(ModelState('human_hand',Pose(Point(gx,gy,gz),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	
def reset_head_hand():
	setmodel = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)	
	setmodel(ModelState('human_head',Pose(Point(0.0,0.0,0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	setmodel(ModelState('human_hand',Pose(Point(0.0,0.0,0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	
def reset_head_hand2(data):
	setmodel = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)	
	setmodel(ModelState('human_head',Pose(Point(0.0,0.0,0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	setmodel(ModelState('human_hand',Pose(Point(0.0,0.0,0.0),Quaternion(0.0,0.0,0.0,1.0)),Twist(Vector3(0.0,0.0,0.0),Vector3(0.0,0.0,0.0)),'world'))
	
	
def main():
	rospy.init_node('human_gazebo_controller', anonymous=True)
    
    	#Reset conditions in Gazebo
    	reset_head_hand()

   	while not rospy.is_shutdown():
		rospy.sleep(0.005)
		rospy.Subscriber("location", Location, move_hand)
		rospy.sleep(0.005)
		rospy.Subscriber("gaze", Gaze, move_head)
		rospy.sleep(0.005)
		rospy.Subscriber("reset_human", Int8, reset_head_hand2)
		
#--------------------------------------------------------------------------------------
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException: #to stop the code when pressing Ctr+c
        	pass


