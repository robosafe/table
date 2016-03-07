#!/usr/bin/env python

"""
Written by Dejanira Araiza-Illan, February 2016
"""
import rospy
from std_msgs.msg import Int8
from bert2_simulator.msg import *

command1 = 0
command2 = 0

def main():
	rospy.init_node('voice_commands', anonymous=True)
	
	while not rospy.is_shutdown():
		rospy.sleep(0.01) 
		rospy.Subscriber("human_voice_a1", Int8, activate_robot)
		global command1
		global command2
		if command1 == 1:
			h_signaling = rospy.Publisher('human_signals', Human, queue_size=1, latch=True) 
			h_signaling.publish(1, 0) 
			rospy.sleep(10)
		else:
			h_signaling = rospy.Publisher('human_signals', Human, queue_size=1, latch=True) 
			h_signaling.publish(0, 0) 
			rospy.sleep(0.1)
			
		rospy.sleep(0.01) 
		rospy.Subscriber("human_voice_a2", Int8, human_ready)
		if command2 == 1:
			h_signaling = rospy.Publisher('human_signals', Human, queue_size=1, latch=True) 
			h_signaling.publish(0, 1) 
			rospy.sleep(10)
		else:
			h_signaling = rospy.Publisher('human_signals', Human, queue_size=1, latch=True)
			h_signaling.publish(0, 0) 
			rospy.sleep(0.1)
		
def activate_robot(data):
	global command1
	if data.data == 1:
		command1 = 1
	else:
		command1 = 0	
	
def human_ready(data):
	global command2
	if data.data == 1:
		command2 = 1
	else:	
		command2 = 0
		
		
#--------------------------------------------------------------------------		
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException: #to stop the code when pressing Ctr+c
        	pass
