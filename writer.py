#! /usr/bin/env python
import csv, os, glob
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from pylab import *

# Get the filelocation	
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

def get_sam_types(file):
	# Procedure to get all sample types
	# @return array of all sample types and number of samples
	# opens the file and counts the sample times to print
	results = {}
	with open(files, 'rb') as f:
		reader = csv.reader(f, delimiter=",", quotechar = "\"")
		for row in reader:
			# checks if row has the target sample type
			if row[31] not in results:
				results[row[31]] = 0
			for x in results:
				if row[31] == x:
					results[x] = results[x] + 1
	return results

def showSamples(f, r):
	# shows a list of counted sample types to choose from
	samTypes = []
	i = 0
	for row in r:
		print '(' + str(i) + ') ' + row + ' ---- ' + str(r[row])
		samTypes.append(row)
		i = i + 1
	return samTypes

def get_rows(file, sT, samTypes): # f is file, sT is the sample type
	# prepares row to be added to final csv file
	finalrows = []
	with open(files, 'rb') as f:
		reader = csv.reader(f, delimiter=",", quotechar = "\"")
		for row in reader:
			if (row[31] == sT or row[31] == "CharacteristicName"):
				finalrows.append(row)
	return finalrows

#def get_
# Take input from the user to get desired file
fileName = '*'
fileName = raw_input("Enter the file name (without extension ie \"test\" not \"test.csv\"): ")
for files in glob.glob(fileName + ".csv"):
	resultList = get_sam_types(files)
	sampleTypes = showSamples(files,resultList)
	if not os.path.exists(files + ' csv'):
		os.makedirs(files + ' csv')
	if not os.path.exists(files + ' graphs'):
		os.makedirs(files + ' graphs')
	for l in sampleTypes:
		p = get_rows(files,l, sampleTypes)
		print p
		print p[1][31]

#make the plots using plot_date()


