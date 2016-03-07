#!/usr/bin/env python

"""
Written by Dejanira Araiza-Illan, February 2016
"""
import sys
import rospy
import random
from geometry_msgs.msg import Point
from bert2_simulator.msg import *

x=0.0
y=0.0
z=0.0


def one_n_mapping_gaze(g_or_b):
	#Gaze_offset	0.1	0.5	0.2	 
	#Gaze_distance	0.5	0.8	0.6 
	#Gaze_angle	15.0	50.0	40.0

	#offset = sample_corner_case(0.2,0.1,0.5)
	#distance = sample_corner_case(0.6,0.5,0.8)
	#angle = sample_corner_case(40.0,15.0,50)

	if g_or_b == 1:
		offset = sample_variable(0.1,0.2)
		distance = sample_variable(0.5,0.6)
		angle = sample_variable(15.0,39.9999)
	else:
		offset = sample_variable(0.2,0.5)
		distance = sample_variable(0.6,0.8)
		angle = sample_variable(40.0,50.0)	
	pub = rospy.Publisher('gaze', Gaze, queue_size=1,latch=True)
	pub.publish(offset,distance,angle)
	rospy.sleep(0.2)



def one_n_mapping_location(g_or_b):
	#Location_x	0.5	1.0	0.75
	#Location_y	-0.3	1.0	0.25
	#Location_z	0.5	1.6	0.65

	if g_or_b == 1:
		rospy.sleep(0.5)
		rospy.Subscriber("piece_location", Point,check_point1) 
		rospy.sleep(0.2)
				
	else:
		rospy.sleep(0.5)
		rospy.Subscriber("piece_location", Point,check_point3)
		rospy.sleep(0.2)
	pub = rospy.Publisher('location',Location, queue_size=1,latch=True)
	pub.publish(x,y,z)
	rospy.sleep(0.2)
	
		

def sample_variable(min_value, max_value): #Sample within the range with uniform distribution
	return random.uniform(min_value, max_value)


def sample_corner_case(value,min_value,max_value): #Sample preferably near a specific value
	y = min_value-1
	while (y<min_value or y>max_value):
		y = random.gauss(value, value*0.2)
	return y
	
def check_point1(data):
	global x
	global y
	global z
	x = data.x+0.05
	y = data.y-0.1
	z = data.z-0.05
	
def check_point3(data):
	global x
	global y
	global z
	x = data.x+0.5+sample_variable(0.0,0.25)
	y = data.y-0.5-sample_variable(0.0,0.25)
	z = data.z+0.5+sample_variable(0.0,0.25)
