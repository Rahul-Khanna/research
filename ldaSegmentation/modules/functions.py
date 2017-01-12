# Module file with useful function
# Author : Rahul Khanna
from reviewModules import Review
from graphModules import Graph
import re

# function that removes some of strange grammer of the interent
def cleanText(text):
	text=text.replace("\\\'","\'")
	text=re.sub(r"(\.){2,}"," ",text)
	text=re.sub(r'(\-){2,}'," ",text)
	text=re.sub(r'(!){2,}'," ",text)
	text=re.sub(r'(\?){2,}'," ",text)
	text=re.sub(r'(/){2,}'," ",text)
	text=re.sub(r'(>){2,}'," ",text)
	text=text.replace("&"," and ")
	text=" ".join(text.split())
	text=text.strip()

	return text

# give a vocabulary a function that counts the numebr of times a vocabularly words appear
# in an arry of sentences
def countKeyWordsInSentences(sentences,vocab):
	count=0
	for sent in sentences:
		strippedLine=re.sub(r'[^a-zA-Z0-9 ]','',str(sent))
		strippedLine=' '.join(strippedLine.split()).strip()
		strippedLine=strippedLine.split()
		for i in range(0,len(strippedLine)):
			word=str(strippedLine[i].lower())
			if word in vocab:
				count+=1
	return count

# converts a dictionary object to a review object, defined in reviewModules.py
def convertToReview(dic):
	temp=Review(dic["id"],dic['review'],dic['realTags'],dic['sentences'])
	if "features" in dic:
		temp.features=dic["features"]
	if "predictedTags" in dic:
		temp.predictedTags=dic["predictedTags"]
	if "predictedLDASentenceTags" in dic:
		temp.predictedLDASentenceTags=dic["predictedLDASentenceTags"]
	if "k" in dic:
		temp.k=dic["k"]

	return temp

# converts a dictionary object to a graph object, defined in graphModules.py
def convertToGraph(dic):
	temp=Graph(dic["id"],dic['review'],dic['sentences'],dic['realTags'])
	if "edgeDictionary" in dic:
		temp.edgeDictionary=dic["edgeDictionary"]
	if "nodeDictionary" in dic:
		temp.nodeDictionary=dic["nodeDictionary"]
	if "predictedTags" in dic:
		temp.predictedTags=dic["predictedTags"]
	if "k" in dic:
		temp.k=dic["k"]
	if "words" in dic:
		temp.words=dic["words"]
	if "realTagsWordLevel" in dic:
		temp.realTagsWordLevel=dic["realTagsWordLevel"]
	if "wordToSentence" in dic:
		temp.wordToSentence=dic["wordToSentence"]

	return temp

