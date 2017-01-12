# Script used to vidsualize features for each sentence in each review
# Generates visualTextLda.html that is styled originalText.css
# Author : Rahul Khanna

import pdb
tuples=[]
with open("../ldaText") as f:
	for line in f:
		tuples.append(eval(line))

with open("visualTextLda.html","w") as f:
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
	f.write("</tr>")
	for tup in tuples:
		f.write("<tr>")
		f.write("<td>")
		f.write("<p>")
		f.write(str(tup[0]))
		f.write("</p>")
		f.write("<p>")
		f.write(str(tup[1]))
		f.write("</p>")
		f.write("</td>")
		f.write("</tr>")
	f.write("</div>")
	f.write("</body>")
	f.write("</html>")