#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  fmri_pipeline.py
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
# 


NUM_ARGUMENTS = 1
NUM_PARAMETERS = 9		
slash = "/"
import sys
import os
arguments = {}

# This function creates a configuration file by giving the name of the file, and its parameters
# paramaters -> a dictionary containing all the keys (parameters names) and values (locations) 
def createConfigFile(filename, parameters):
  f = open(filename, "wt")
  
  for k in parameters.keys():
    f.write(k+":"+parameters[k]+"\n")
  f.close()


# Checking if he user entered the correct parameters in order to run the script
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

# Displaying the help option to the user
if len(sys.argv) > 1 and sys.argv[1] == "--help":
	print ""
	print "------This is the main script of the pipeline------"
	print "Syntax to run this script: python niral_dti_system.py -config config_global_system.txt "
	print ""
	print "The config file requires the following format:"
	print "ATLAS:location of the ATLAS file"
	print "T1:location of the T1 file"
	print "T2:location of the T2 file"
	print "SubjectFolder:SubjectFolder_Directory"
	print "SubjectList:SubjectList file location"
	print ""
	exit(0)

		
print "Num of arguments passed:",len(sys.argv) -1

# Error message in case of using wrong numbers of parameters
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


# This is the dictionary. These names, except for 'config', must be in the config file
arguments_names = ["config", "OutputFolder", "SubjectFolder", "SubjectList", "PreprocessTemplate", "RegressTemplate", "BrainTemplate", "ROIFolder", "MatlabFolder", "CorrType"]

checkParameters(arguments, arguments_names)

subject_folder = arguments["SubjectFolder"]

# checking if the slash exists
if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"

f = open(arguments["SubjectList"])


# This loop runs according to the number of Subjects the user wants to process
for subject in f.readlines():
  print "Running the following subject: ", subject.rstrip()
  
  current_subject_folder = subject_folder + subject.rstrip()
  
  if current_subject_folder[len(current_subject_folder)-1] != '/':
    current_subject_folder=current_subject_folder + "/"
  
  if arguments["OutputFolder"][len(arguments["OutputFolder"])-1] != '/':
    arguments["OutputFolder"]=arguments["OutputFolder"] + "/"
  os.system("mkdir "+arguments["OutputFolder"])
  os.system("mkdir "+current_subject_folder + "config/")
  # Calling the script that transforms the DWI in the DTI space
  createConfigFile(current_subject_folder+"config/config_segmentation.txt", {"SubjectFolder":current_subject_folder})
  print "Running Segmentation script:"
  
  if os.system("python segmentation.py -config "+current_subject_folder+"config/config_segmentation.txt") != 0:
    exit(-1)
  
  # Applying the registration to the Subject 
  createConfigFile(current_subject_folder+"config/config_registration.txt", {"PreprocessTemplate":arguments["PreprocessTemplate"],"SubjectFolder":current_subject_folder})
  print "Running Registration script:"
  os.system("python registration.py -config "+current_subject_folder+"config/config_registration.txt")
  
  
  createConfigFile(current_subject_folder+"config/config_regression.txt", {"PreprocessTemplate":arguments["RegressTemplate"], "SubjectFolder":current_subject_folder})
  print "Running Regression script:"
  os.system("python regression.py -config "+current_subject_folder+"config/config_regression.txt")
  
  
  print "Running Filtering script:"
  createConfigFile(current_subject_folder+"config/config_filtering.txt", {"BrainTemplate":arguments["BrainTemplate"], "SubjectFolder":current_subject_folder})
  os.system("python filtering.py -config "+current_subject_folder+"config/config_filtering.txt")
   
  
  print "Extracting time series:"
  createConfigFile(current_subject_folder+"config/config_extract_ts.txt", {"SubjectFolder":current_subject_folder, "ROIFolder":arguments["ROIFolder"]})
  os.system("python extract_ts.py -config "+current_subject_folder+"config/config_extract_ts.txt")
    
  
  print "Running Scrubbing:"
  createConfigFile(current_subject_folder+"config/config_scrubbing.txt", { "SubjectFolder":current_subject_folder })
  os.system("python scrubbing.py -config "+current_subject_folder+"config/config_scrubbing.txt")
  
  print "Packing everything in the path: " + arguments["OutputFolder"] + subject.rstrip() + "_ts"
  output_folder = arguments["OutputFolder"] + subject.rstrip() + "_ts"
  
  createConfigFile(current_subject_folder+"config/config_pack_it.txt", { "OutputFolder":arguments["OutputFolder"] , "SubjectFolder":current_subject_folder })
  os.system("python pack_it.py -config "+current_subject_folder+"config/config_pack_it.txt")
  
  print "Extracting connectome and its graph measures:"
  createConfigFile(current_subject_folder+"config/config_extract_connectome.txt", { "MatlabFolder":arguments["MatlabFolder"] , "CorrType":arguments["CorrType"] , "SubjectFolder":output_folder })
  os.system("python extract_connectome.py -config "+current_subject_folder+"config/config_extract_connectome.txt")
  
