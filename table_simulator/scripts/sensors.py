#!/usr/bin/env python
"""
This script simulates the sensors, which consider the human's gaze, position and location, to determine if they are within a threshold ("human is ready"), or not, and transmit the decision to the robot. The sensors have an error, implemented as a probability. 

Written by Dejanira Araiza-Illan February-March 2015.
Modified for table by Dejanira Araiza-Illan February 2016.

"""
import sys
import rospy
import random
from bert2_simulator.msg import *
from geometry_msgs.msg import Point
from std_msgs.msg import Int8

#Global variables
gaze_ok = -100 #initial values that indicate the sensors are undefined
pressure_ok = -100
location_ok = -100
piece_loc = [0,0,0]

#--------------------------------------------------------------------------------
def check_gaze(data):
	global gaze_ok 
	if data.offset <= 0.2 and data.distance <= 0.6 and data.angle < 40.0: 
		gaze_ok = 1
	else:
		gaze_ok = 0

#--------------------------------------------------------------------------------
def check_pressure(data):
	global pressure_ok
	if data.data==1: 
		pressure_ok = 1
	else:
		pressure_ok = 0	

#--------------------------------------------------------------------------------
def check_location(data):
	global location_ok
	rospy.Subscriber("piece_location", Point,check_point) 
	if abs(data.x - piece_loc[0])<=0.3 and abs(data.y - piece_loc[1]) <=0.3 and abs(data.z - piece_loc[2]) <=0.3: 
		location_ok = 1
	else:
		location_ok = 0

def check_point(data):
	global piece_loc
	piece_loc[0] = data.x
	piece_loc[1] = data.y
	piece_loc[2] = data.z
	

#-------------------------------------------------------------------------------
#---------------------------------------------------------------------------
def main(same_seed):
	random.seed(same_seed)
	rospy.init_node('sensors', anonymous=True)

	while not rospy.is_shutdown():
		rospy.sleep(0.005)
		rospy.Subscriber("pressure", Int8, check_pressure)
		rospy.sleep(0.005)
		rospy.Subscriber("location", Location, check_location)
		rospy.sleep(0.005)
		rospy.Subscriber("gaze", Gaze, check_gaze)
		
		#Sensing error
		global gaze_ok
		global pressure_ok
		global location_ok
		#gaze
		no = random.randint(0, 100)
		if no <= 5: #set probability
			if gaze_ok == 1:
				gaze_ok = 0 #false negative due to occlusions 
		#pressure
		no = random.randint(0, 100)
		if no <= 5:#set probability
			if pressure_ok == 0:
				pressure_ok = 1 #false positive due to piece wobbling in robot's hand
		#location
		no = random.randint(0, 100)
		if no <= 5:#set probability
			if location_ok == 1:
				location_ok = 0 #false negative due to occlusions

		pub = rospy.Publisher("sensors", Sensors, queue_size=1,latch=True)		
		pub.publish(gaze_ok,location_ok,pressure_ok)
		print str(gaze_ok)+','+str(location_ok)+','+str(pressure_ok)

#--------------------------------------------------------------------------------------
if __name__ == '__main__':
	try:
		main(sys.argv[1])
	except rospy.ROSInterruptException: #to stop the code when pressing Ctr+c
        	pass


