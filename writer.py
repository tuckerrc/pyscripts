#! /usr/bin/env python

""" 
	Version 1.0
	Changelog
	  1.0
	    Stop plotting data for sample types with less than 10 values
	Changelog 
	  0.9
	    Added check for missing month/day/year values
		if missing set to 1/1/1900
	
"""
import csv, os, glob, logging
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from pylab import *
from matplotlib.dates import rrulewrapper, RRuleLocator

# Get the filelocation	
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

def get_sam_types(file):
	# Procedure to get all sample types
	# @return array of all sample types and number of samples
	# opens the file and counts the sample times to print
	results = {}
	with open(file, 'rb') as f:
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
	with open(file, 'rb') as f:
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
	unit_list = []
	for u in array:
		item = u[34]	
		item = " ".join(item.split())
		if item != 'ResultMeasure/MeasureUnitCode' and item not in unit_list and item != 'None':
			unit_list.append(item)
	units = str(unit_list)
	units = units.replace("[","")
	units = units.replace("]","")
	units = units.replace("'","")
	units = units.replace(" ,",",")
	#print units
	return units

def get_type(array):
	samType = array[1][31]
	
	return samType

def plot(dates,samples,units,samType,graphdir):
	i = 0

	for d in dates:
		if d.find('/')==-1:
			first = d.find('-')
			second = d.rfind('-')
			# Check for missing month/day/year values in the file
			try:
				year = int(d[0:first])
			except ValueError:
				year = 1900
			try:
				month = int(d[first+1:second])
			except ValueError:
				month = 1
			try:
				day = int(d[second+1:])
			except ValueError:
				day = 1
			if(first == -1 and second == -1):
				day = 1
				month = 1
				
			dates[i] = datetime.date(year,month,day)
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
	rule = rrulewrapper(YEARLY)
	loc = RRuleLocator(rule)
	formatter = DateFormatter('%Y')
	#sample_range = (float(max(float(i) for i in samples)) - float(min(float(i) for i in samples)))
	#sample_range = sample_range/25
	
	fig, ax = plt.subplots()

	#if (sample_range != 0):
	#	minorLocator = MultipleLocator(sample_range)
	#	ax.yaxis.set_minor_locator(minorLocator)
	
	plt.plot_date(dates, samples)
	ax.xaxis.set_major_locator(loc)
	ax.xaxis.set_major_formatter(formatter)
	labels = ax.get_xticklabels()
	plt.title(samType)
	plt.ylabel(units)
	plt.setp(labels, rotation=30, fontsize=12)
	plt.savefig(graphdir+'/'+samType+'.png',bbox_inches='tight')
	plt.close()

#def get_
# Take input from the user to get desired file
def main():
	fileName = '*'
	fileName = raw_input("Enter the file name '*' for all (without extension ie \"test\" not \"test.csv\"): ")
	print 'Please wait...'
	currentFile = ''
	for f in glob.glob(fileName + ".csv"):
		print 'Processing: ' + f
		currentFile = f
		resultList = get_sam_types(f)
		sampleTypes = showSamples(f,resultList)
		csvdirName = f + ' csv'
		graphdirName = f + ' graphs'	
		if not os.path.exists(csvdirName):
			os.makedirs(csvdirName)
		if not os.path.exists(graphdirName):
			os.makedirs(graphdirName)
		
		for l in sampleTypes:		
			p = get_rows(f,l, sampleTypes)
			sampleDates = get_dates(p)		
			#print p
			if (len(p[1:])):
				if p[1][31].find('/') == -1 and p[1][31].find('[') == -1 :
					csvWriter(p,p[1][31],csvdirName)
					sampleDates = get_dates(p)
					sampleData = get_data(p)
					sampleUnits = get_units(p)
					sampleT	= get_type(p)
					print '	Sample Type: ' + sampleT
					if sampleT != 'Turbidity severity' and len(sampleData) > 10:
						plot(sampleDates,sampleData,sampleUnits,sampleT,graphdirName)
						
logging.basicConfig(level=logging.DEBUG, filename='error.log')

try:
	main()		
except:
	logging.exception("")
	
logging.shutdown()
if os.stat('error.log')[6]==0:
	os.remove('error.log')
	
#make the plots using plot_date()


