#!/usr/bin/env python
"""
Implements assertion 5: if 'flag1==1' then check 'flag2==1' and check time difference


Written by Dejanira Araiza-Illan, July 2015
Modified by Dejanira Araiza-Illan, February 2016
"""
import sys
import rospy
import smach
import smach_ros
import time
from std_msgs.msg import Int8

receivedflag1=0
receivedflag2=0
stats = open('assertion5.txt','a')
fileno = 0
result = 0
globaltime = 0

class Flag1(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])

    def execute(self, userdata):
	global receivedflag1
	receivedflag1 = 0
	rospy.sleep(0.01)
	rospy.Subscriber("tabledone", Int8, callback1)
	if receivedflag1 == 1:
		receivedflag1 = 0
		return 'outcome1'
        else:
		return 'outcome2'

class Flag2(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])

    def execute(self, userdata):
	global receivedflag2
	global result
	result = 0
	receivedflag2 = 0
	rospy.sleep(0.01)
	rospy.Subscriber("tableontime", Int8, callback2)
	if receivedflag2 == 1 and result == 1:
		global stats
		stats.write('Assertion 5 at test '+ str(fileno) +': Passed at global time '+ str(time.time()-globaltime) +'\n')
		return 'outcome1'
	elif receivedflag == 1 and result == 0:
		global stats
		stats.write('Assertion 5 at test '+ str(fileno) +': Failed at global time '+ str(time.time()-globaltime) +'\n')
		return 'outcome1'
        else:
		return 'outcome2'


def callback1(data):
	global receivedflag1
	if data.data==1:
		receivedflag1 = 1
	else:
		receivedflag1 = 0
	

def callback2(data):
	global receivedflag2
	global result
	if data.data==1:
		receivedflag2 = 1
		result = 1
	else:
		receivedflag2 = 1
		result = 0

def main(number):
	rospy.init_node('assertion2', anonymous=True) #Start node first
	global fileno
	fileno = number
	# Create a SMACH state machine
    	sm = smach.StateMachine(outcomes=['Done'])

   	 # Open the container
   	with sm:
		#Receive signal
		smach.StateMachine.add('Flag1', Flag1(), 
                transitions={'outcome1':'Flag2','outcome2':'Flag1'})

		#Receive signal
		smach.StateMachine.add('Flag2', Flag2(),
		transitions={'outcome1':'Flag1','outcome2':'Flag2'})		


	# Execute SMACH plan
    	outcome = sm.execute()

if __name__ == '__main__':
	try:
		main(sys.argv[1])
	except	rospy.ROSInterruptException:
		pass
