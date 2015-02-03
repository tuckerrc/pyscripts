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


import csv, os, glob # Imports already written code to be used in the file.  This is what makes python awesome!
# These modules can be used with this syntax.  "csvfile, dialect='excel')"  "csv" tells python to check for the csv module for a "reader()" function.


# This section defines all the functions that do stuff to the csv files.
def read_file(file, fN):
	""" 
		Reads the file and parses the data from the large into single station files.
		params:
			file: the name of the file including extension (ie. test.csv)
			fN: the file name without extension (ie. test)
	"""
	with open(file, 'rb') as q:
		# Creates the reader.  This is from the csv module included with python. https://docs.python.org/2/library/csv.html
		# q is the variable object the file is stored in.
		# "rb" tells python to open the file in read only mode
		
		reader = csv.reader(q,delimiter=",",quotechar = "\"") # Creates a csv reader object. csv.reader(q is the file we just opened, delimiter is a comma, quotechar is a quotation)
		
		for row in reader: # A loop that iterates through each row in the reader.  This checks the 22 cell in the row for the site name.
			# If a file already has that name it adds the row to the end.  If the file does not it creates a new file and adds the header row and the first row.
			
			if row[21] == 'MonitoringLocationIdentifier': # We use == to check if strings are the same
				header = row # Creates the header row object.
			
			elif os.path.isfile(fN+'/'+row[21]+'.csv'):
				# Adds the row to the end of the file
				with open(fN+"/"+ row[21] +'.csv','ab') as f: # Opens the file in "ab" mode (append) as f (the file object). 
					writer = csv.writer(f) # creates the csv writer object.  csv.writer(f is the file object we just created.)
					writer.writerow(row) 
				# Closes the file when done writing to it.
				f.close() # Closes f.
			
			else:
				with open(fN+"/"+ row[21] +'.csv','wb') as f: # Creates the file in "wb" mode (write) as f (the file object).
					print "Writing " + row[21] + '.csv' # Writes this to the console so we can se what the script is up to.  This isn't actually neccessary but it's helpful to see the script working.
					writer = csv.writer(f) # creates the csv writer object.  csv.writer(f is the file object we just created.)
					writer.writerow(header) # Writes the header row with the writer object
				f.close() # Closes f
				with open(fN+"/"+row[21]+'.csv','ab')as f: # Opens the file in "ab" mode (append) as f (the file object). 
					writer = csv.writer(f) # creates the csv writer object.  csv.writer(f is the file object we just created.)
					writer.writerow(row) # Writes the row with the writer object
				f.close() # Closes f
	return # This tells python that this function is complete and can continue running the rest of the script. Basically it sends it back.

# The end of defining functions.
	
# This is where the scripting starts.
path = os.path.dirname(os.path.realpath(__file__)) # This calls the os module to get the path and directory name.  (Basically tells python where we are on the computer)
os.chdir(path) # This changes the directory to where we are so the script can find the csv files.
fileName = raw_input("Enter the file name (without extension ie \"test\" not \"test.csv\"): ") # This is what gets the filename from the user and adds it to a filename object.
#fileName = "Result-2"  # Used for testing purposes.
for f in glob.glob(fileName + ".csv"): # This is a for loop that checks each file in the directory to see if it matches the filename object.
	if not os.path.exists(fileName): # Checks if the directory already exists. I need to add a check to make sure the script only runs once (not sure how to do that yet).
		os.makedirs(fileName) # Makes a new directory if it doesn't.
	print "Processing: " + f # This outputs the filename so we know what the script is doing.  It's not neccessary but it is helpful.
	read_file(f, fileName) # this calls the read_file() function we defined on line 20 (or somewhere around there) to do the things to the csv file.
	
	
