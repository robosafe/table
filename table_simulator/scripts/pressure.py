#!/usr/bin/env python
"""
This script simulates the events of pressure, in the current sensors located on BERT2's hand. When the piece is grabbed, code triggers a presure change event. When the human holds the piece simultaneously, another event is triggered, expecting another pressure change from the current readings. 

Written by Dejanira Araiza Illan, July 2015. 
"""

import rospy
from std_msgs.msg import Int8


e1 = 0
e2 = 0

def main():
	rospy.init_node('pressure', anonymous=True)

	while not rospy.is_shutdown():
		rospy.sleep(0.01)
		rospy.Subscriber("pressure_e1", Int8, check_e1)
		rospy.sleep(0.01)
		rospy.Subscriber("pressure_e2", Int8, check_e2)
	
		pub = rospy.Publisher("pressure", Int8, queue_size=1,latch=True)
		if e1 == 1 and e2 ==1: 
			pub.publish(1)
		else:
			pub.publish(0)
		rospy.sleep(0.1)
	
			
def check_e1(data):
	global e1
	if data.data == 1:
		e1 = 1
	else:
		e1 = 0

def check_e2(data):
	global e2
	if data.data == 1:
		e2 = 1
	else:
		e2 = 0
	
	
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException: #to stop the code when pressing Ctr+c
        	pass
