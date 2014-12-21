#! /usr/bin/env python 
import csv, os, glob

def get_location_rows(file):
	""" Returns list of all locations """
	locations = []
	with open(file, 'rb') as f:
		reader = csv.reader(f,delimiter=",",quotechar = "\"")
		for row in reader:
			if row[21] not in locations and row[21] != 'MonitoringLocationIdentifier':
				locations.append(row[21])
	print locations
	f.close()
	return locations
	
def create_csv_list(location,file):
	""" Creates csv of location """
	file_name = str(location)
	finalrows = []
	with open(file, 'rb') as f:
		reader = csv.reader(f,delimiter=",",quotechar = "\"")
		for row in reader:
			i = 0
			if (row[21] == file_name or row[21] == "MonitoringLocationIdentifier"):
				finalrows.append(row)
				i = 1
			elif i ==1:
				f.close()
				return finalrows
	f.close()
	return finalrows

def write_csv(rows, location,fN):
	file_name = str(location)
	print "Writing " + file_name + ".csv"
	with open(fN+"/"+file_name +'.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerows(rows)
	f.close()
		

	
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
fileName = raw_input("Enter the file name (without extension ie \"test\" not \"test.csv\"): ")
for f in glob.glob(fileName + ".csv"):
	if not os.path.exists(fileName):
		os.makedirs(fileName)
	print "Processing: " + f
	loc = get_location_rows(f)
	for l in loc:
		loc_spec_list = create_csv_list(l,f)
		write_csv(loc_spec_list, l, fileName)
	