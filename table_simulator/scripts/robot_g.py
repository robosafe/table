#!/usr/bin/env python
"""
This script interfaces the robot motion with Gazebo, by setting the values of the joints. This script would be replaced by YARP interface to set up the real robot's joints.

Written by Dejanira Araiza-Illan, June 2015

Format of the vector of joint commands for Gazebo-ROS:
'hipRotor', 'hipFlexor', 'neckFlexor', 'neckRotor', 'leftShoulderFlexor', 'rightShoulderFlexor', 'leftShoulderAbduction',  'leftHumeralRotation', 'leftElbowFlexor','leftWristPronation', 'leftWristAbduction', 'leftWristFlexor'

Format of the vector of joint commands for the hand:
'leftThumb1', 'leftThumb2', 'leftIndex1', 'leftIndex2', 'leftMiddle1', 'leftMiddle2', 'leftAnular1', 'leftAnular2', 'leftLittle1', 'leftLittle2'
"""

import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState


def set_robot_joints(data): #In the real robot, this would communicate with the yarp to send commands to joints
	hipRotor = rospy.Publisher('/bert2/hip_rotor_joint_posControlr/command',Float64, queue_size=1,latch=True) 
	hipFlexor = rospy.Publisher('/bert2/hip_flexor_joint_posControlr/command',Float64, queue_size=1,latch=True) 
	neckFlexor = rospy.Publisher('/bert2/neck_flexor_joint_posControlr/command',Float64, queue_size=1,latch=True) 
	neckRotor = rospy.Publisher('/bert2/neck_rotor_joint_posControlr/command',Float64, queue_size=1,latch=True) 
	leftShoulderFlexor = rospy.Publisher('/bert2/left_shoulder_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	rightShoulderFlexor = rospy.Publisher('/bert2/right_shoulder_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftShoulderAbduction = rospy.Publisher('/bert2/left_shoulder_abduction_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftHumeralRotor = rospy.Publisher('/bert2/left_humeral_rot_joint_posControlr/command', Float64, queue_size=1,latch=True)
	leftElbowFlexor = rospy.Publisher('/bert2/left_elbow_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftWristPronation = rospy.Publisher('/bert2/left_wrist_pronation_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftWristAbduction = rospy.Publisher('/bert2/left_wrist_abduction_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftWristFlexor = rospy.Publisher('/bert2/left_wrist_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 

	if data[0]!=-1000.0:
		hipRotor.publish(data[0])
		rospy.sleep(0.01)
	if data[1]!=-1000.0:
		hipFlexor.publish(data[1])
		rospy.sleep(0.01)	
	if data[2]!=-1000.0:	
		neckFlexor.publish(data[2]) #Limit speed here
		rospy.sleep(0.01)
	if data[3]!=-1000.0:	
		neckRotor.publish(data[3])#Limit speed here
		rospy.sleep(0.01)
	if data[4]!=-1000.0:
		leftShoulderFlexor.publish(data[4])
		rospy.sleep(0.01)
	if data[5]!=-1000.0:
		rightShoulderFlexor.publish(data[5])#Limit speed here
		rospy.sleep(0.01)
	if data[6]!=-1000.0:
		leftShoulderAbduction.publish(data[6])
		rospy.sleep(0.01)
	if data[7]!=-1000.0:
		leftHumeralRotor.publish(data[7])
		rospy.sleep(0.01)
	if data[8]!=-1000.0:
		leftElbowFlexor.publish(data[8])
		rospy.sleep(0.01)
	if data[9]!=-1000.0:
		leftWristPronation.publish(data[9])
		rospy.sleep(0.01)
	if data[10]!=-1000.0:
		leftWristAbduction.publish(data[10])
		rospy.sleep(0.01)
	if data[11]!=-1000.0:
		leftWristFlexor.publish(data[11])
		rospy.sleep(0.01)

def move_hand(command): #In the real robot, this would communicate with the yarp to send commands to joints
	leftShoulderFlexor = rospy.Publisher('/bert2/left_shoulder_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftThumb1 = rospy.Publisher('/bert2/left_thumb_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftThumb2 = rospy.Publisher('/bert2/left_thumb2_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftIndex1 = rospy.Publisher('/bert2/left_index_finger_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftIndex2 = rospy.Publisher('/bert2/left_index_finger2_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftMiddle1 = rospy.Publisher('/bert2/left_mid_finger_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftMiddle2 = rospy.Publisher('/bert2/left_mid_finger2_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftAnular1 = rospy.Publisher('/bert2/left_anular_finger_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftAnular2 = rospy.Publisher('/bert2/left_anular_finger2_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftLittle1 = rospy.Publisher('/bert2/left_little_finger_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 
	leftLittle2= rospy.Publisher('/bert2/left_little_finger2_flex_joint_posControlr/command', Float64, queue_size=1,latch=True) 

	if command == 'open':
		leftThumb1.publish(-1.57)
		rospy.sleep(0.5)
		leftThumb2.publish(0.0)
		rospy.sleep(0.1)
		leftIndex1.publish(0.0)
		rospy.sleep(0.1)
		leftIndex2.publish(0.0)
		rospy.sleep(0.1)
		leftMiddle1.publish(0.0)
		rospy.sleep(0.1)
		leftMiddle2.publish(0.0)
		rospy.sleep(0.1)
		leftAnular1.publish(0.0)
		rospy.sleep(0.1)
		leftAnular2.publish(0.0)
		rospy.sleep(0.1)
		leftLittle1.publish(0.0)
		rospy.sleep(0.1)
		leftLittle2.publish(0.0)
		rospy.sleep(0.1)
	elif command == 'close':
		leftThumb2.publish(0.3)
		rospy.sleep(0.1)
		leftMiddle2.publish(-0.3)
		rospy.sleep(0.1)
		
		leftThumb2.publish(0.5)
		rospy.sleep(0.1)
		leftIndex2.publish(-0.3)
		rospy.sleep(0.1)
		
		leftThumb2.publish(0.75)
		rospy.sleep(0.1)
		leftIndex2.publish(-0.4)
		rospy.sleep(0.1)
		leftMiddle2.publish(-0.4)
		rospy.sleep(0.1)
		leftAnular2.publish(-0.2)
		rospy.sleep(0.1)
		leftLittle2.publish(-0.2)
		rospy.sleep(0.1)

		leftIndex2.publish(-0.7)
		rospy.sleep(0.1)
		leftMiddle2.publish(-0.7)
		rospy.sleep(0.1)
		leftAnular2.publish(-0.3)
		rospy.sleep(0.1)
		leftLittle2.publish(-0.3)
		rospy.sleep(0.1)




	
	
