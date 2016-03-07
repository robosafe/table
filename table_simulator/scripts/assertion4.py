#!/usr/bin/env python
"""
Implements assertion 4: if 'flag1==1' 

Written by Dejanira Araiza-Illan, February 2016
"""
import sys
import rospy
import time
from sensor_msgs.msg import JointState
stats = open('assertion4.txt','a')
globaltime = 0
j1a = 0
j2a = 0
j3a = 0
j4a = 0
j5a = 0
j6a = 0
j7a = 0
j8a = 0
j9a = 0
j1 = 0
j2 = 0
j3 = 0
j4 = 0
j5 = 0
j6 = 0
j7 = 0
j8 = 0
j9 = 0
fail = 0

def main(number):
	rospy.init_node('assertion4', anonymous=True) #Start node first
	global fileno
	global fail
	fileno = number
	rospy.Subscriber("joint_states", JointState, callback1)
	while not rospy.is_shutdown():
		rospy.sleep(1)
		rospy.Subscriber("joint_states", JointState, callback2) #10Hz rate by default
       		if fail == 1:
               		stats.write('Assertion 4 at test '+ str(fileno) +': Failed at global time '+ str(time.time()-globaltime) +'\n')
               	fail = 0
                
def callback1(data):
	global j1a
	j1a = data.position[0]
	global j2a
	j2a = data.position[1]
	global j3a
	j3a = data.position[4]
	global j4a
	j4a = data.position[5]
	global j5a
	j5a = data.position[12]
	global j6a
	j6a = data.position[13]
	global j7a
	j7a = data.position[16]
	global j8a
	j8a = data.position[17]
	global j9a
	j9a = data.position[18]

	
def callback2(data):
	global j1
	j1 = data.position[0]
	global j2
	j2 = data.position[1]
	global j3
	j3 = data.position[4]
	global j4
	j4 = data.position[5]
	global j5
	j5 = data.position[12]
	global j6
	j6 = data.position[13]
	global j7
	j7 = data.position[16]
	global j8
	j8 = data.position[17]
	global j9
	j9 = data.position[18]
	global j1a
	global j2a
	global j3a
	global j4a
	global j5a
	global j6a
	global j7a
	global j8a
	global j9a
	global fail
	if abs(j1a-j1)>=0.25 or abs(j2a-j2)>=0.25 or (j3a-j3)>=0.25 or abs(j4a-j4)>=0.25 or abs(j5a-j5)>=0.25 or abs(j6a-j6)>=0.25 or abs(j7a-j7)>=0.25 or abs(j8a-j8)>=0.25 or abs(j9a-j9)>=0.25:	
		fail = 1
		#print fail
		#print abs(j1a-j1)/0.1, abs(j2a-j2)/0.1, (j3a-j3)/0.1, abs(j4a-j4)/0.1, abs(j5a-j5)/0.1, abs(j6a-j6)/0.1, abs(j7a-j7)/0.1, abs(j8a-j8)/0.1, abs(j9a-j9)/0.1
	else:
		fail = 0
	


              
if __name__ == '__main__':
	try:
		main(sys.argv[1])
	except	rospy.ROSInterruptException:
		pass
