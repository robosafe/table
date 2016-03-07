#!/usr/bin/env python

"""
This script performs a post-processing to adjust the coverage statistics, to account for statements that are marked as not executed when they might have been. 

Written by Dejanira Araiza-Illan, May 2015
"""

import rospy
import inspect
import sys
import robot
import os
import re


overhead = 77

#Discount classes (smach) -> 3 lines each
classes_number=0
for name, obj in inspect.getmembers(robot):
	if inspect.isclass(obj) and obj.__module__ == 'robot':
		classes_number+=1

#Discount functions (custom) -> 1 line each
functions_number=0
for name, obj in inspect.getmembers(robot):
	if inspect.isfunction(obj):
		functions_number+=1

#Get statistics from html reports
for i, line in enumerate(open('/home/dejanira/catkin_ws/covhtml/src_table_simulator_scripts_robot_py.html', 'r')): 
	for match in re.finditer("        <h2 class='stats'>",line):
		the_line = i+1
for i, line in enumerate(open('/home/dejanira/catkin_ws/covhtml/src_table_simulator_scripts_robot_py.html', 'r')): 
	if i==the_line:
		number = re.split("statements &nbsp;", line)
	if i==the_line+1:
		no_run = re.split("<span class='run hide_run shortkey_r button_toggle_run'>", line)
		no_run = re.split(" run</span>",no_run[1])
	if i==the_line+2:
		no_miss = re.split("<span class='mis shortkey_m button_toggle_mis'>", line)
		no_miss = re.split(" missing</span>",no_miss[1])

#Print adjusted statistics
f= open('stats.txt', 'a')
f.write('Considered statements:'+str(int(number[0])-overhead)+'\n')
f.write('Missing statements:'+str(int(no_miss[0])-overhead)+'\n')
f.write('Covered percentage:'+ str((int(number[0])-int(no_miss[0]))*100/(int(number[0])-overhead)) + '%\n')
f.write('-------------------\n')


