#! /usr/bin/env python 

""" 
 ---- Version 1.0 ----
 Changelog
	Changed the way the program workes making it magnitudes faster.
 
 -- To Fix --
	Check if the program has been run on the current file. (Don't run again as it doubles to data)
	Create GUI interface so it is not so intimitading.
	Write Documentation on how to use the file
"""


import csv, os, glob

def read_file(file, fN):
	with open(file, 'rb') as q:
		reader = csv.reader(q,delimiter=",",quotechar = "\"")
		for row in reader:
			if row[21] == 'MonitoringLocationIdentifier':
				header = row
			elif os.path.isfile(fN+'/'+row[21]+'.csv'):
				with open(fN+"/"+ row[21] +'.csv','ab') as f:
					writer = csv.writer(f)
					writer.writerow(row)
				f.close()
			else:
				with open(fN+"/"+ row[21] +'.csv','wb') as f:
					print "Writing " + row[21] + '.csv'
					writer = csv.writer(f)
					writer.writerow(header)
				f.close()
				with open(fN+"/"+row[21]+'.csv','ab')as f:
					writer = csv.writer(f)
					writer.writerow(row)
				f.close()
	return

def get_location_rows(file):
	""" Returns list of all locations """
	# No longer needed
	locations = []
	with open(file, 'rb') as f:
		reader = csv.reader(f,delimiter=",",quotechar = "\"")
		for row in reader:
			if row[21] not in locations and row[21] != 'MonitoringLocationIdentifier':
				locations.append(row[21])
	f.close()
	return locations
	
def create_csv_list(location,file):
	""" Creates csv of location """
	# No longer needed
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
	# No longer needed
	file_name = str(location)
	print "Writing " + file_name + ".csv"
	with open(fN+"/"+file_name +'.csv','wb') as f:
		writer = csv.writer(f)
		writer.writerows(rows)
	f.close()

path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)
fileName = raw_input("Enter the file name (without extension ie \"test\" not \"test.csv\"): ")
#fileName = "Result-2"
for f in glob.glob(fileName + ".csv"):
	if not os.path.exists(fileName):
		os.makedirs(fileName)
	print "Processing: " + f
	read_file(f, fileName)
#	loc = get_location_rows(f)
#	for l in loc:
#		loc_spec_list = create_csv_list(l,f)
#		write_csv(loc_spec_list, l, fileName)
	
