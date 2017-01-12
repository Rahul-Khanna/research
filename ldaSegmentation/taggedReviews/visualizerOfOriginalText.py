# Script used to generate an html file that is used to visualize the results of the segmentation against ground truth
# Generates visualOfOrigianlText.html that is styled originalText.css
# Author: Rahul Khanna
import sys
import pdb
import pickle

def createSegments(sentences,tags):
	segments=[]
	temp=""
	for i in range(0,len(sentences)):
		temp+=sentences[i]
		temp+=". "
		if i<len(sentences)-1:
			if tags[i+1]==1:
				temp.strip()
				segments.append(temp)
				temp=""
		else:
			temp.strip()
			segments.append(temp)

	return segments


reviews={}

with open("trainingData","rb") as f:
	temp=pickle.load(f)
	for obj in temp:
		reviews[obj.id]={}

		segments=createSegments(obj.sentences,obj.predictedTags)
		reviews[obj.id]["predictedSegments"]=segments

		segments=createSegments(obj.sentences,obj.realTags)
		reviews[obj.id]["realSegments"]=segments

with open("testingData","rb") as f:
	temp=pickle.load(f)
	for obj in temp:
		reviews[obj.id]={}

		segments=createSegments(obj.sentences,obj.predictedTags)
		reviews[obj.id]["predictedSegments"]=segments

		segments=createSegments(obj.sentences,obj.realTags)
		reviews[obj.id]["realSegments"]=segments


with open("visualOfOriginalText.html","w") as f:
	f.write("<!DOCTYPE html>\n")
	f.write("<html>\n")
	f.write("<head>\n")
	f.write("<link rel=\"stylesheet\" type=\"text/css\" href=\"originalText.css\"")
	f.write("</head>")
	f.write("<body>\n")
	f.write("<div id=\"header\">")
	f.write("<h1>Broken Up Reviews:</h1>")
	f.write("</div>")
	f.write("<p></p>")
	f.write("<div id=\"body\">")
	f.write("<table style=\"width:100%\">")
	f.write("<tr>")
	f.write("<th>These are the marked segments: </th>")
	f.write("<th>These are the predicted segments: </th>")
	f.write("</tr>")
	for key in reviews:
		f.write("<tr>")
		f.write("<td>")
		for segment in reviews[key]["realSegments"]:
			f.write("<p>")
			f.write(segment.encode("utf8"))
			f.write("</p>")
			f.write("<p>")
			f.write("</p>")
		f.write("</td>")
		f.write("<td>")
		for segment in reviews[key]["predictedSegments"]:
			f.write("<p>")
			f.write(segment.encode("utf8"))
			f.write("</p>")
			f.write("<p>")
			f.write("</p>")
		f.write("</td>")
		f.write("</tr>")
	f.write("</div>")
	f.write("</body>")
	f.write("</html>")

