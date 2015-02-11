#! /usr/bin/env python 
import csv, os, glob, re

def stationReader(fN):
	spans = []
	with open(fN, 'rb') as f:
		reader = csv.reader(f, delimiter=",", quotechar="\"")
		i = 0
		for row in reader:
			if i != 0:
				htmlClass = row[4]
				htmlClass = re.sub('[^0-9a-zA-Z]+', ' ', htmlClass)
				sp = "<div class='" + htmlClass + "'>"
				sp = sp+"<h1>"+row[2]+"</h1>"
				sp = sp+"<strong>Organization: </strong> "+row[1]+"<br/>"
				sp = sp+"<strong>Location Name: </strong> "+row[3]+"<br/>"
				sp = sp+"<strong>Type: </strong>"+row[4]+"<br>"
				sp = sp+"<strong>Latitude: </strong>"+row[11]+"<br/><strong> Longitude: </strong>"+row[12]+"<br/>"
				sp = sp+"<strong>Description: </strong><br/>"+row[5]+"</div>"	
				spans.append(sp)
			i = i+1
	f.close()	  	
	return spans
def htmlWriter(array):
	start = "<html><head><style>html,body{height:100%;width: 100%;margin: 0px;}div{display:inline-block;padding:30px;width:300px;margin:10px;border:2px solid black; overflow:hidden;} h1{margin:0px;font-size:18px;} .Stream,.River.Stream{border-color: blue;} .Spring{border-color:green;}.Well{border-color:brown;} .Ditch{border-color:aqua;} .Lake.Reservoir{border-color:orange;} .Lake{border-color:darkblue;}.Atmosphere{border-color:skyblue;} .key{position: fixed;bottom: 0px;right: 0px;padding: 0px; color:white; width: 125px; border:none; opacity: 0.9;} .key div{padding: 5px; margin: 1px; width: 100px; background:gray; color:white;}</style></head><body>"
	end = "<div class='key'><div class='Stream'>Stream/River</div><div class='Spring'>Spring</div><div class='Lake'>Lake</div><div class='Well'>Well</div><div class='Ditch'>Ditch</div><div class='Lake Reservoir'>Lake Reservoir</div><div class='Atmosphere'>Atmosphere</div></div></body></html>"
	string = ""
	for i in array:
		string = string + i
	html = start + string + end
	htmlFile = open("Stations.html","wb")
	htmlFile.write(html)
	htmlFile.close()

# Get the filelocation	
path = os.path.dirname(os.path.realpath(__file__))
os.chdir(path)

# Take input from the user to get desired file
fileName = 'Station'
for files in glob.glob(fileName + ".csv"):
	spanList = stationReader(files)
	htmlWriter(spanList)
