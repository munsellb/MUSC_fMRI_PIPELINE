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
arguments = {}

import sys
import os

#in python 3.x  -> 
#from tkinter import *
#filename = askopenfilename()

#in python 2.x
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from tkMessageBox import *
## GUI stuff ##
def getFile(i, file):
	entries[i].delete(0, END)
	if file == True:
	  entries[i].insert(0,askopenfilename())
	else:
	  entries[i].insert(0,askdirectory())

def getInputs(event):
  for i in range(0,8):
    if entries[i].get() == "":
      showwarning('Warning', 'One or more fields are empty!')
      return
  arguments["OutputFolder"] = entries[0].get()
  arguments["SubjectFolder"] = entries[1].get()
  arguments["SubjectList"] = entries[2].get()
  arguments["PreprocessTemplate"] = entries[3].get()
  arguments["RegressTemplate"] = entries[4].get()
  arguments["BrainTemplate"] = entries[5].get()
  arguments["ROIFolder"] = entries[6].get()
  arguments["MatlabFolder"] = entries[7].get()
  arguments["CorrType"] = v.get()
  print arguments
  createConfigFile( ".fMRI_GUI_CONFIG.txt", arguments )
  super_master.destroy()

  
def createConfigFile(filename, parameters):
  f = open(filename, "wt")
  
  for k in parameters.keys():
    f.write(k+":"+parameters[k]+"\n")
  f.close()
  
def loadConfigFile():
  if ( os.path.exists( ".fMRI_GUI_CONFIG.txt" ) ):
    f = open(".fMRI_GUI_CONFIG.txt", "r")
    lines = f.readlines()
    for i in range(0, len(lines)):
      tokens = lines[i].rstrip().split(":")
      arguments[tokens[0]] = tokens[1]
	
    entries[0].insert(0, arguments["OutputFolder"])
    entries[1].insert(0, arguments["SubjectFolder"] )
    entries[2].insert(0, arguments["SubjectList"] )
    entries[3].insert(0, arguments["PreprocessTemplate"] )
    entries[4].insert(0, arguments["RegressTemplate"] )
    entries[5].insert(0, arguments["BrainTemplate"] )
    entries[6].insert(0, arguments["ROIFolder"] )
    entries[7].insert(0, arguments["MatlabFolder"] )
    v.set( arguments["CorrType"] )
  
super_master = Tk()
master = Frame(super_master)
master.pack()
master2 = Frame(super_master)
master2.pack()
master3 = Frame(super_master)
master3.pack()
Label(master, text="OutputFolder:").grid(row=0)
Label(master, text="SubjectFolder:").grid(row=1)
Label(master, text="SubjectList:").grid(row=2)
Label(master, text="PreprocessTemplate:").grid(row=3)
Label(master, text="RegressTemplate:").grid(row=4)
Label(master, text="BrainTemplate:").grid(row=5)
Label(master, text="ROIFolder:").grid(row=6)
Label(master, text="MatlabFolder:").grid(row=7)
Label(master2, text="CorrType:").grid(row=0)
b1 = Button(master, text="...", fg="black")
b2 = Button(master, text="...", fg="black")
b3 = Button(master, text="...", fg="black")
b4 = Button(master, text="...", fg="black")
b5 = Button(master, text="...", fg="black")
b6 = Button(master, text="...", fg="black")
b7 = Button(master, text="...", fg="black")
b8 = Button(master, text="...", fg="black")

b1.grid(row=0, column=2)
b2.grid(row=1, column=2)
b3.grid(row=2, column=2)
b4.grid(row=3, column=2)
b5.grid(row=4, column=2)
b6.grid(row=5, column=2)
b7.grid(row=6, column=2)
b8.grid(row=7, column=2)

b1.bind('<Button-1>', lambda event, i=0 : getFile(i, False))
b2.bind('<Button-1>', lambda event, i=1 : getFile(i, False))
b3.bind('<Button-1>', lambda event, i=2 : getFile(i, True))
b4.bind('<Button-1>', lambda event, i=3 : getFile(i, True))
b5.bind('<Button-1>', lambda event, i=4 : getFile(i, True))
b6.bind('<Button-1>', lambda event, i=5 : getFile(i, True))
b7.bind('<Button-1>', lambda event, i=6 : getFile(i, False))
b8.bind('<Button-1>', lambda event, i=7 : getFile(i, False))

entries = []
for i in range(0,8):
  entries.append(Entry(master, width=50))
  entries[i].grid(row=i, column=1)

v = StringVar()
v.set("pearson")

r1 = Radiobutton(master2, text="Pearson", variable=v, value="pearson")

r2 = Radiobutton(master2, text="Partial", variable=v, value="partial")

r3 = Radiobutton(master2, text="Kendall", variable=v, value="kendall")

r4 = Radiobutton(master2, text="Spearman", variable=v, value="spearman")

r1.grid(row=0, column=1)
r2.grid(row=0, column=2)
r3.grid(row=0, column=3)
r4.grid(row=0, column=4)

ok_button = Button(master3, text="Run", fg="black")
ok_button.bind('<Button-1>',getInputs)
ok_button.pack()

loadConfigFile()

super_master.mainloop()

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

try:

  subject_folder = arguments["SubjectFolder"]

except:
  
  exit(0)
  
  
print subject_folder + "++++++++++++"
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
  
