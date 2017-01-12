# A script that breaks down text into segments by splitting annoted text
# The script does so by splitting on a sequence of characters "segmenter"
# The starting sentence of each segment is labled as 1, the rest are labled as 0
# Author: Rahul Khanna
from reviewModules import *
from functions import *
import spacy
import re
import os
import pdb
import sys

segmenter="*|*|* "

# unicode to ascii issues
reload(sys)
sys.setdefaultencoding('utf8')

# the english spacy model
en_nlp=spacy.load('en')

# an array to store all tagged reviews
taggedReviews=[]

# an array to store all reviews that need to be tagged
reviewsToBeTagged=[]

# reading in the reviews that need to be tagged
with open("../inputs/random20_edit1_Rahul2.txt") as f1:
	reviews=f1.read()
	reviews=reviews.split("\n\n")
	for review in reviews:
		if review:
			reviewsToBeTagged.append(unicode(review))

# reading in the reviews that need to be tagged
with open("../inputs/random20_edit2_Rahul2.txt") as f1:
	reviews=f1.read()
	reviews=reviews.split("\n\n")
	for review in reviews:
		if review:
			reviewsToBeTagged.append(unicode(review))

# an id to be assigned to the review object
k=0
for review in reviewsToBeTagged:
	text=eval(review)[1]
	textParts=text.split(segmenter)
	tags=[]
	sentences=[]
	for part in textParts:
		# an array to store each segment's sentences
		tempSentences=[]
		# creates a spacy document
		part=en_nlp(unicode(cleanText(part)))
		for sent in part.sents:
			# getting rid of most punctuation
			strippedSentence=re.sub(r'[^a-zA-Z0-9 .\']',' ',str(sent))
			strippedSentence=' '.join(strippedSentence.split()).strip()
			sen=str(strippedSentence).split(".")
			# more than one sentence in what spacy thought was one sentence
			if len(sen)>1:
				for s in sen:
					# making sure the sentence is not some silly parsing issue
					if len(s)>0 and s!=" " and s!="\n":
						# splitting the sentence into words
						temp=s.split()
						if len(temp)<2:
							# trying to rectify split by "." problem
							if len(temp)>0:
								if len(sentences)>0 and len(tempSentences)>0:
									stringToAppend="."+temp[0]
									sentences[len(sentences)-1]+=stringToAppend
									tempSentences[len(tempSentences)-1]+=stringToAppend
						# if the number of words is greater that 1 keep it
						else:
							sentences.append(s)
							tempSentences.append(s)

			else:
				# checking to see if the sentence has more than 1 word
				temp=sen[0].split()
				if len(temp)>1:
					sentences.append(sen[0])
					tempSentences.append(sen[0])

		sentences[:] = [x for x in sentences if x != ""]
		tempSentences[:] =[x for x in tempSentences if x != ""]
		tags.append(1)
		for i in range(1,len(tempSentences)):
			tags.append(0)

	# creating a reviews object
	tR=Review(k,text,tags,sentences)
	k+=1
	taggedReviews.append(tR)

# writting out the tagged reviews
with open("taggedReviews/allReviews2","w") as f:
	for review in taggedReviews:
		f.write(str(review))
		f.write("\n")






