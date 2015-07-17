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
		
slash = "/"
import sys
import os
import subprocess

def getfolder( path , separator):
  return path[ path.rfind( separator ) : ]

subjects_folder = sys.argv[1]
if subjects_folder[len(subjects_folder)-1] != '/':
  subjects_folder=subjects_folder + "/"

subjects = subprocess.check_output("ls "+subjects_folder, shell=True)
subjects = subjects.rstrip()
subjects = subjects.split("\n")

print subjects

for s in subjects:
  os.system("mv " + subjects_folder+s + "/MPRAGE" + " " + subjects_folder+s + "/structural")
  os.system("mv " + subjects_folder+s + "/Resting_State_fMRI" + " " + subjects_folder+s + "/rsfMRI")
  
  structural_folder = subjects_folder+s + "/structural/"
  functional_folder = subjects_folder+s + "/rsfMRI/"
  
  structurals = subprocess.check_output("ls "+structural_folder+"*/* | grep .dcm", shell=True)
  structurals = structurals.rstrip()
  structurals = structurals.split("\n")
  inside1 = subprocess.check_output("ls "+structural_folder, shell=True)
  inside1 = inside1.rstrip()
  inside1 = inside1.split("\n")
  inside1 = inside1[0]
  inside2 =  subprocess.check_output("ls "+structural_folder+inside1, shell=True)
  inside2 = inside2.rstrip()
  inside2 = inside2.split("\n")
  inside2 = inside2[0]
  
  print structurals
  i = 1
  for img in structurals:
    os.system("mv " + structural_folder+inside1+"/"+inside2+"/"+img + " " + structural_folder + str(i))
    i = i + 1
  os.system("dcm2nii " + structural_folder + "1")
  os.system("find " + structural_folder + " ! -name *.nii.gz -delete")
  
  functionals = subprocess.check_output("ls "+functional_folder+"*/* | grep .dcm", shell=True)
  functionals = functionals.rstrip()
  functionals = functionals.split("\n")
  inside1 = subprocess.check_output("ls "+functional_folder, shell=True)
  inside1 = inside1.rstrip()
  inside1 = inside1.split("\n")
  inside1 = inside1[0]
  inside2 =  subprocess.check_output("ls "+functional_folder+inside1, shell=True)
  inside2 = inside2.rstrip()
  inside2 = inside2.split("\n")
  inside2 = inside2[0]
  i = 1
  for img in functionals:
    os.system("mv " + functional_folder+inside1+"/"+inside2+"/"+img + " " + functional_folder + str(i))
    i = i + 1
  os.system("dcm2nii " + functional_folder + "1")
  os.system("find " + functional_folder + " ! -name *.nii.gz -delete")
  