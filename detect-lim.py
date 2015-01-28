#! /usr/bin/env python

""" 
 ---- Version 1.0 ----
 Changelog
	
 
 -- To Fix --
	Currently it will rewrite all the rows to the new file if it has been run once before... Not sure how to stop it.
"""

import csv, os, glob

def read_file(file, fN):
	"""
		Function for opening the file removing the '<' and dividing by 2. 
		Passes new values to write_row() function to write new file.
	"""
	with open(file, 'rb') as q:
		reader = csv.reader(q,delimiter=",",quotechar = "\"")
		for row in reader:
			copy = list(row)
			i = 0
			for cell in copy:
				if cell.find('<') != -1:
					x = float(cell[1:])/2
					copy[i] = x
				i = i + 1
			write_row(copy, fN)
						
def write_row(row, fN):
	"""
		Function for writing the new detection limit corrected values to a new file
	"""
	file = fN + '-lc.csv' # create new file with -lc (limit corrected)
	with open(file, 'ab') as q:
		writer = csv.writer(q,delimiter=",", quotechar = "\"")
		writer.writerow(row)

# Get the file location	
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

# Take input from the user to get desired file
fileName = raw_input("File Name: ")
for file in glob.glob(fileName + ".csv"):
	spanList = read_file(file, fileName)