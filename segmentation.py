#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  segmentation.py
#  
#  Copyright 2015 Andy <Andy@ANDY-PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Software needed in your path to run this script:
#  bet   (found on FSL Package)
#  fast   (found on FSL package)
#
#

NUM_ARGUMENTS = 1
NUM_PARAMETERS = 1		
slash = "/"
import sys
import os
arguments = {}

def find_co_file(files):
  for f in files:
    if (len(f) > 1 and f[ :2 ] == "co"):
      return f
    
  return None

def checkParameters(parameters, valid_ones):
	for k in parameters.keys():
		if not (k in valid_ones):
			print "ERROR:", k, "is not a valid paramater!"
			print "For more information use --help"
			exit(-1)
		if parameters[k][0] == '-':
			print "ERROR:",parameters[k], "is not a valid parameter value for", k
			print "For more information use --help"
			exit(-1)

if len(sys.argv) > 1 and sys.argv[1] == "--help":
	print "This script segmentates a brain scan into three regions: csf, grey and white matter. It also removes the skull"
	print "Syntax to run this script: segmentation.py -config config_filename"
	print ""
	print "The config file requires the following format:"
	print "SubjectFolder: The folder where the subject content is located. This folder must contain a structural folder containing the brain scan. The brain scan name must start with 'co'."
	print ""
	print "The output will be located in a folder called \"convert\" "
	exit(0)

		
print "Num of arguments passed:",len(sys.argv) -1

if len(sys.argv)-1 != NUM_ARGUMENTS*2:
	print "ERROR: You must pass only",NUM_ARGUMENTS*2,"arguments!"
	print "For more information use --help"
	exit(-1)

i = 1
while i < len(sys.argv):
	print "!"
	if sys.argv[i].find("-") != -1:
		arguments[sys.argv[i][1:]] = sys.argv[i+1]
		i = i + 1
	i = i + 1
print arguments
print "working directory:",os.getcwd()

arguments_names = ["config", "SubjectFolder"]

checkParameters(arguments, arguments_names)

#reading config file and parsing its new parameters
f = open(arguments["config"])

lines = f.readlines()
if len(lines) != NUM_PARAMETERS:
	print "ERROR: the config file should only contain",NUM_PARAMETERS,"parameters"
	print "For more information use --help"
	exit(-1)
	
for i in range(0, NUM_PARAMETERS):
	if lines[i].find(":") == -1:
		print "ERROR: The line",i+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE"
		print "For more information use --help"
		exit(-1)
	tokens = lines[i].rstrip().split(":")
	
	arguments[tokens[0]] = tokens[1]

#checking

checkParameters(arguments, arguments_names)
print arguments

subject_folder = arguments["SubjectFolder"]

if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"

structural_folder = subject_folder + "structural/"
print structural_folder
for k in arguments.keys():
  arguments[k] = subject_folder + arguments[k]

#all arguments were checked
bet_input_file = structural_folder + find_co_file(os.listdir(structural_folder))
#running bet
bet_output_file = structural_folder + "brain.nii.gz"

print("Segmentating: " + subject_folder)

#extracting the brain from the skull
os.system("bet " + bet_input_file + " " + bet_output_file + " -f 0.28 -R -B")

convert_folder = subject_folder + "convert/"
os.system("mkdir " + convert_folder)

subject_folder_name = subject_folder
subject_folder_name = subject_folder_name[:len(subject_folder_name) - 1]
subject_folder_name = subject_folder_name[subject_folder_name.rfind("/") + 1 : ]

fast_input_file = bet_output_file
fast_output_file = convert_folder + subject_folder_name + "_seg"

#extracting the csf, white and grey matter from the brain
os.system("fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 " + " -o "+ fast_output_file + " " + fast_input_file)
#print("cmd: " + "fast -t 1 -n 3 -H 0.1 -I 4 -l 20.0 " + fast_input_file + " -o "+ fast_output_file)
#visualizing the results (optional). For quality checking purposes
os.system("fslview "+ bet_input_file + " " + fast_output_file + "_pve_0 -l Blue-Lightblue " + fast_output_file + "_pve_1 -l Red " + fast_output_file + "_pve_2 -l Yellow &")
#print("cmd: " + "fslview "+ bet_input_file + " " + fast_output_file + "_pve_0 -l Blue-Lightblue " + fast_output_file + "_pve_1 -l Red " + fast_output_file + "_pve_2 -l Yellow &")
#print("Segmentation for " + subject_folder + " finished!")
