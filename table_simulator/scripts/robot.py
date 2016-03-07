#!/usr/bin/env python
"""
This script implements the state machine of the robot element in the simulator. The types of states available are receiving signals, sending signals, reset the position of the robot, move and grab an object, sense the human, and decide what to do about the handover. The reset position assumes the robot is not holding anything.

Format of the vector of joint commands for Gazebo:
'hipRotor', 'hipFlexor', 'neckFlexor', 'neckRotor', 'leftShoulderFlexor', 'rightShoulderFlexor', 'leftShoulderAbduction',  'leftHumeralRotation', 'leftElbowFlexor','leftWristPronation', 'leftWristAbduction', 'leftWristFlexor'

Format of the vector of joint commands for the hand:
'leftThumb1', 'leftThumb2', 'leftIndex1', 'leftIndex2', 'leftMiddle1', 'leftMiddle2', 'leftAnular1', 'leftAnular2', 'leftLittle1', 'leftLittle2'

Format of the joints used for planning:
'hipRotor', 'hipFlexor', 'leftShoulderFlexor', 'leftShoulderAbduction',  'leftHumeralRotation', 'leftElbowFlexor','leftWristPronation', 'leftWristAbduction', 'leftWristFlexor'

Assembled from handover code by Dejanira Araiza-Illan February 2016.
"""
import sys
import os
import rospy
import smach
import smach_ros
import math
import random
import time
from robot_g import set_robot_joints #Script that has the Gazebo interface to move the robot
from robot_g import move_hand #Script that has the Gazebo interface to move the hand
from interface_plan import interface #Script that has the Moveit interface for planning
from bert2_simulator.msg import *
from std_msgs.msg import Float64
from std_msgs.msg import Int8
from geometry_msgs.msg import Point
from coverage import Coverage




#global variables
reception = 0
reception2 = 0
piece = 0
location_ok = 0
pressure_ok = 0
gaze_ok = 0
piece_location = []
the_timeout = 5.0
start = 0
count_timeout=0
leg_counter = 0
timeout_time = 0
table_timeout = 0
good_legs = 0

#--------------------------------------------------------------------------------------------------------------------
class Reset(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])

    def execute(self, userdata):
    	#Reset position with hand open
	#global cov
	#cov.start()
    	theplans = interface([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	for i,plan in enumerate(theplans):
		set_robot_joints(plan)
	rospy.sleep(1)
	set_robot_joints([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
	move_hand('open')
	rospy.sleep(0.5)
	global table_timeout
	table_timeout = time.time()
	#cov.stop()
	#cov.save()
	return 'outcome1'
	

#--------------------------------------------------------------------------------------------------------------------
class ReceiveA1(smach.State): 
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2','outcome3'])

    def execute(self, userdata):
    	#global cov
    	#cov.start()
	global reception
	global count_timeout
	reception = 0
	rospy.sleep(0.05)
	rospy.Subscriber("human_signals", Human, callback_signals) 
	if reception == 1:
		count_timeout = 0
		#cov.stop()
		#cov.save()
		return 'outcome1'
        elif count_timeout<60:
        	count_timeout += 1
        	#cov.stop()
		#cov.save()
		return 'outcome2'
	else:
		print 'Timed out' #Timed out waiting for signals
		count_timeout = 0
		#cov.stop()
		#cov.save()
		return 'outcome3'
		

def callback_signals(data):
	global reception
    	if data.activateRobot==1 and data.humanIsReady==0: #activateRobot signal
		reception = 1
			#--------------------------------------------------------------------------------------------------------------------
class ReceiveA2(smach.State): 
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2','outcome3'])

    def execute(self, userdata):
    	global cov
    	#cov.start()
	global reception
	global count_timeout
	reception = 0
	rospy.sleep(0.05)
	rospy.Subscriber("human_signals", Human, callback_signals2) 
	if reception == 1:
		count_timeout = 0
		#cov.stop()
		#cov.save()
		return 'outcome1'
        elif count_timeout<60:
        	count_timeout += 1
        	#cov.stop()
        	#cov.save()
		return 'outcome2'
	else:
		print 'Timed out' #Timed out waiting for signals
		count_timeout = 0
		#cov.stop()
		#cov.save()
		return 'outcome3'
		

def callback_signals2(data):
	global reception
    	if data.activateRobot==0 and data.humanIsReady==1: #humanIsReady signal
		reception = 1

#--------------------------------------------------------------------------------------------------------------------
class Move(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])

    def execute(self, userdata):	
    	#global cov
    	#cov.start()	
	#Path planning towards the piece
	theplans = interface([-0.5,0.0,-0.75,0.0,1.39,0.0,0.0,-0.5,0.0])
	for i,plan in enumerate(theplans):
		set_robot_joints(plan)		
	theplans = interface([-1.15,0.05,-0.75,-1000.0,1.39,-1000.0,-1000.0,-0.5,-1000.0])
	for i,plan in enumerate(theplans):
		set_robot_joints(plan)
	theplans = interface([-1.15,0.05,-0.48,-1000.0,1.39,-1000.0,-1000.0,-0.5,-1000.0])
	for i,plan in enumerate(theplans):
		set_robot_joints(plan)
	move_hand('close')
	rospy.sleep(0.5)
	hand = rospy.Publisher('robot_gripper', Int8, queue_size=1,latch=True)
	hand.publish(1)
	rospy.sleep(0.5)
	hand.publish(0)
	pubpress = rospy.Publisher('pressure_e1', Int8, queue_size=1,latch=True)
	pubpress.publish(1)
	rospy.sleep(0.2)

	#Path planning towards goal location
	theplans = interface([0.0,0.05,-0.75,0.0,1.39,0.0,0.0,-0.5,0.0])
	#print theplans
	for i,plan in enumerate(theplans):
		set_robot_joints(plan)
	rospy.sleep(1)
	hand2 = rospy.Publisher('robot_has_piece', Int8, queue_size=1,latch=True)
	hand2.publish(1)
	rospy.sleep(0.1)
	#cov.stop()
	#cov.save()
	return 'outcome1'
	

#--------------------------------------------------------------------------------------------------------------------
class Send(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])

    def execute(self, userdata):
    	#global cov
    	#cov.start()
	global pubsignals
	rospy.sleep(0.5)
	pubsignals = rospy.Publisher('robot_signals', Robot, queue_size=1,latch=True)
	pubsignals.publish(1)	#RobotIsReady
	rospy.sleep(1)
	pubsignals.publish(0)
	rospy.sleep(0.1)
	global start
	start=time.time()
	#cov.stop()
	#cov.save()
	return 'outcome1'

#--------------------------------------------------------------------------------------------------------------------
class Sense(smach.State): #Collecting and analysing info from pressure, location and gaze
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2','outcome3'])

    def execute(self, userdata):
    	#global cov
    	#cov.start()
	global reception2
	global start
	reception2 = 0
	rospy.sleep(0.2)
	rospy.Subscriber("sensors", Sensors, callback_sensors)
	if (time.time()-start) >= timeout_time: #Timed out sensing
		#cov.stop()
		#cov.save()
		return 'outcome3'
	else:
		if reception2 == 1:
			#cov.stop()
			#cov.save()
        		return 'outcome1'
		else:
			#cov.stop()
			#cov.save()
			return 'outcome2'	

def callback_sensors(data):
	global reception2
	global gaze_ok
	global location_ok
	global pressure_ok
	if data.gaze==1:
		gaze_ok = 1
	else:
		gaze_ok = 0
	if data.location==1:
		location_ok = 1
	else:
		location_ok = 0
	if data.pressure == 1:
		pressure_ok = 1
	else:
		pressure_ok = 0
	reception2 = 1

#------------------------------------------------------------------------------------------------------------------
class WaitLong(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])

    def execute(self, userdata):
    	#global cov
    	#cov.start()
	rospy.sleep(2)
	#cov.stop()
	#cov.save()
	return 'outcome1'

#---------------------------------------------------------------------------------------------------------------------
class Timeout(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1'])

    def execute(self, userdata):
    	#global cov
    	#cov.start()
	print 'Robot timed out'
	#cov.stop()
	#cov.save()
	return 'outcome1'

#--------------------------------------------------------------------------------------------------------------------
class Decide(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])

    def execute(self, userdata):
    	#global cov
    	#cov.start()
	rospy.sleep(0.1)
	if gaze_ok == 1 and pressure_ok == 1 and location_ok == 1:
		pubgpl = rospy.Publisher('gpl_is_ok', Int8, queue_size=1,latch=True)
		print 'GPL is OK'
		pubgpl.publish(1)
		rospy.sleep(0.1)
		pubgpl.publish(0)
		#cov.stop()
		#cov.save()
		return 'outcome1'

	else:
		pubgpl = rospy.Publisher('gpl_is_not_ok', Int8, queue_size=1,latch=True)
		print 'GPL is not OK'
		pubgpl.publish(1)
		rospy.sleep(0.1)
		pubgpl.publish(0)
		#cov.stop()
		#cov.save()
		return 'outcome2'
	
#-------------------------------------------------------------------------------------------------------
class Release(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
       
    def execute(self, userdata):
    	#global cov
    	#cov.start()
    	print 'Piece is released'
    	global leg_counter
    	leg_counter = leg_counter + 1
    	global good_legs
    	good_legs = good_legs + 1
    	print leg_counter
    	move_hand('open')
	rospy.sleep(0.5)
	pubpress = rospy.Publisher('pressure_e1', Int8, queue_size=1,latch=True)
	pubpress.publish(0)
	rospy.sleep(0.1)
    	pubrel = rospy.Publisher('resetpiece', Int8, queue_size=1,latch=True)
    	pubrel.publish(1)
    	rospy.sleep(0.05)
    	pubrel.publish(0)
    	hand2 = rospy.Publisher('robot_has_piece', Int8, queue_size=1,latch=True)
	hand2.publish(0)
    	rospy.sleep(0.1)
    	pubpiecedone = rospy.Publisher('legdone', Int8, queue_size=1,latch=True)
    	pubpiecedone.publish(1)
    	#pubrel.publish(0)
    	rospy.sleep(0.1)
    	pubpiecedone.publish(0)
    	rospy.sleep(0.1)
    	if leg_counter < 4:
    		#cov.stop()
		#cov.save()
        	return 'outcome1'
        else:
        	leg_counter=0
        	if good_legs >= 4:
        		pubtabledone = rospy.Publisher('tabledone', Int8, queue_size=1,latch=True)
        		pubtabledone.publish(1)
        		rospy.sleep(0.1)
        		pubtableontime = rospy.Publisher('tableontime', Int8, queue_size=1,latch=True)
        		if (time.time()-table_timeout)<=300:
        			pubtableontime.publish(1)
        			rospy.sleep(0.1)
        			print 'Table on time'
        		else:
        			pubtableontime.publish(0)
        			rospy.sleep(0.1)
        			print 'Table not on time'
        	#cov.stop()
		#cov.save()
        	return 'outcome2'

#--------------------------------------------------------------------------------------------------------
class Discard(smach.State):
    def __init__(self):
    	smach.State.__init__(self, outcomes=['outcome1','outcome2'])
    
    def execute(self, userdata):
    	global leg_counter
    	leg_counter = leg_counter + 1
    	#print leg_counter
    	move_hand('open')
    	pubrel = rospy.Publisher('resetpiece', Int8, queue_size=1,latch=True)
    	pubrel.publish(1)
    	rospy.sleep(0.1)
    	pubrel.publish(0)
    	hand2 = rospy.Publisher('robot_has_piece', Int8, queue_size=1,latch=True)
	hand2.publish(0)
    	rospy.sleep(0.1)
    	pubpiecedone = rospy.Publisher('legdone', Int8, queue_size=1,latch=True) 
    	pubpiecedone.publish(0)
    	pubrel.publish(0)
    	rospy.sleep(0.2)
    	if leg_counter >= 4:
    		return 'outcome2'
        return 'outcome1'

#-------------------------------------------------------------------------------------------------------
def main(same_seed):
	random.seed(same_seed)
	rospy.init_node('robot', anonymous=True) #Start node first
	global timeout_time
	timeout_time = random.randint(10, 100)
	# Create a SMACH state machine
    	sm = smach.StateMachine(outcomes=['tableDone'])

   	# Open the container
   	with sm:
		#Reset state
		smach.StateMachine.add('Reset', Reset(), 
                transitions={'outcome1':'Receive1'})

		#Receive signal
		smach.StateMachine.add('Receive1', ReceiveA1(), transitions={'outcome1':'Move_hand','outcome2':'Receive1','outcome3':'Timeout1'})
		smach.StateMachine.add('Timeout1',Timeout(),transitions={'outcome1':'Receive1'})
		
		#Move robot towards piece (path planning)
		smach.StateMachine.add('Move_hand', Move(), transitions={'outcome1':'Send1'})

		#Send signal informHumanOfHandover
		smach.StateMachine.add('Send1', Send(), transitions={'outcome1':'Receive2'})

		#Receive signal humanIsReady
		smach.StateMachine.add('Receive2', ReceiveA2(), transitions={'outcome1':'Wait0','outcome2':'Receive2','outcome3':'Timeout2'})
		smach.StateMachine.add('Timeout2',Timeout(),transitions={'outcome1':'Discard'})

		#Wait for human
		smach.StateMachine.add('Wait0', WaitLong(), transitions={'outcome1':'Sensing'})		

		#Sense human with timeout
		smach.StateMachine.add('Sensing', Sense(), transitions={'outcome1':'Decide','outcome2':'Sensing','outcome3':'Timeout3'})
		smach.StateMachine.add('Timeout3',Timeout(), transitions={'outcome1':'Discard'}) 

		#Decide what to do
		smach.StateMachine.add('Decide', Decide(), transitions={'outcome1':'Release','outcome2':'Discard'})
		
		#Release piece
		smach.StateMachine.add('Release', Release(), transitions={'outcome1':'Receive1','outcome2':'tableDone'})
		
		#Discard piece
		smach.StateMachine.add('Discard', Discard(), transitions={'outcome1':'Receive1','outcome2':'tableDone'})
	# Execute SMACH plan
    	outcome = sm.execute()
	

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	cov = Coverage()
	cov.start()
	try:
    		main(sys.argv[1])
    		cov.stop()
    		cov.html_report(directory='covhtml')
	except rospy.ROSInterruptException: #to stop the code when pressing Ctr+c
		cov.stop()
    		cov.save()
    		cov.report_html()
        	pass
        	
        	

