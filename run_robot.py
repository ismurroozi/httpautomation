# This script is used to run cases under test cases directory
# Test cases are categorised based on the service
# In each service directory, files are categorised based on API

# You can run this script by typing py .\run_robot.py <directory> in terminal
# <directory> will help the script to identify all the files inside the directory
# for example: python3 .\run_robot.py .\test_cases\
# Once you run, logs will be created and stored in logs directory


# Pre-Requisite:
# - python
# - robotframework
# - pip

import sys
import os
import subprocess


dir_path = sys.argv[1]
command = "robot --outputdir .\logs --timestampoutputs "+dir_path
print("will run cases under directory", dir_path)
print("command to run: ",command)
os.system('cmd /c '+command)