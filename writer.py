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
	f.close()
	return results

def showSamples(f, r):
	# shows a list of counted sample types to choose from
	samTypes = []
	i = 0
	for row in r:
		#print '(' + str(i) + ') ' + row + ' ---- ' + str(r[row])
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
	f.close()
	return finalrows

def csvWriter(rows, fN, dN):
	# writes the final csv file with all rows of target sample type
	with open(dN +'/' +fN + '.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerows(rows)
	f.close()

def get_dates(array):
	dates = []
	for i in array[1:]:
		dates.append(i[6])
	#print dates	
	return dates

def get_data(array):
	data = []
	for i in array[1:]:
		data.append(i[33])
	#print data	
	return data

def get_units(array):
	unit = array[1][34]
	return unit

def get_type(array):
	samType = array[1][31]
	return samType

def plot(dates,samples,units,samType,graphdir):
	i = 0

	for d in dates:
		if d.find('/')==-1:
			first = d.find('-')
			second = d.rfind('-')
			dates[i] = datetime.date(int(d[0:first]),int(d[first+1:second]),int(d[second+1:]))
			i = i+1		
		else:		
			first = d.find('/')
			second = d.rfind('/')
			dates[i] = datetime.date(int(d[second+1:]),int(d[0:first]),int(d[first+1:second]))
			i = i+1
	c = 0
	for s in samples:
		if s == '':
			samples[c]  = '0.0'
		c = c+1

	formatter = DateFormatter('%Y')

	fig, ax = plt.subplots()

	plt.plot_date(dates, samples)
	ax.xaxis.set_major_formatter(formatter)
	labels = ax.get_xticklabels()
	plt.title(samType)
	plt.ylabel(units)
	plt.setp(labels, rotation=30, fontsize=12)
	plt.savefig(graphdir+'/'+samType+'.png',bbox_inches='tight')
	plt.close()

#def get_
# Take input from the user to get desired file
fileName = '*'
fileName = raw_input("Enter the file name '*' for all (without extension ie \"test\" not \"test.csv\"): ")
print 'Please wait...'
for files in glob.glob(fileName + ".csv"):
	print 'Processing: ' + files
	resultList = get_sam_types(files)
	sampleTypes = showSamples(files,resultList)
	csvdirName = files + ' csv'
	graphdirName = files + ' graphs'	
	if not os.path.exists(csvdirName):
		os.makedirs(csvdirName)
	if not os.path.exists(graphdirName):
		os.makedirs(graphdirName)
	
	for l in sampleTypes:		
		p = get_rows(files,l, sampleTypes)
		sampleDates = get_dates(p)		
		#print p
		if (len(p[1:])):
			csvWriter(p,p[1][31],csvdirName)
			sampleDates = get_dates(p)
			sampleData = get_data(p)
			sampleUnits = get_units(p)
			sampleT	= get_type(p)
			plot(sampleDates,sampleData,sampleUnits,sampleT,graphdirName)


#make the plots using plot_date()


