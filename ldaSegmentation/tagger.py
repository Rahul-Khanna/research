# A command line tagging interface that allows a user to tag sentences of text
# Every sentence of every docuement can be assigned a label and the resulting tuple is stored
# Author: Rahul Khanna
from reviewModules import *
from functions import *
import spacy
import re
import os
import pdb

# the english model from spacy
en_nlp=spacy.load('en')

# checking the number of tagged reviews, assuming per document read a new document will be used to write to
count=-1
with open("taggedReviews/usefulTaggedReviews1","r") as f:
	if os.stat("taggedReviews/usefulTaggedReviews1").st_size>0:
		lines=f.read()
		lines=lines.split("\n")

		# -1 because of split, -1 because you want k>count and k starts at zero
		count=len(lines)-2
		print "Count"
		print count

# reading the reviews to be tagged and stored
# to allow for the pausing of the tagging process, each review that is tagged is appeneded to the file
with open("taggedReviews/usefulTaggedReviews1","a") as f1:
	with open("../inputs/random20.txt") as f:
		reviews=f.read()
		reviews=reviews.split("\n\n")
		k=0
		for review in reviews:
			# skipping all reviews that have been tagged in previous sessions
			if k>count:
				response=int(input("Continue, 1 or 0?"))
				if response:
					text=eval(review)[1]
					tags=[]
					# creates a spacy document
					text=en_nlp(unicode(cleanText(text)))
					sentences=[]
					for sent in text.sents:
						# getting rid of most punctuation
						strippedSentence=re.sub(r'[^a-zA-Z0-9 .\']',' ',str(sent))
						strippedSentence=' '.join(strippedSentence.split()).strip()
						# creating an array of sentences
						sen=str(strippedSentence).split(".")
						# more than one sentence in what spacy thought was one sentence
						if len(sen)>1:
							for s in sen:
								# making sure the sentence is not some silly parsing issue
								if len(s)>0 and s!=" " and s!="\n":
									# splitting the sentence into words
									temp=s.split()
									if len(temp)<2:
										# trying to rectify split by "." number problem, 3.* would be spilt into 3 and *
										if len(temp)==1:
											stringToAppend="."+temp[0]

									# if the number of words is greater than 1, consider a sentence
									else:
										sentences.append(s)

						else:
							# checking to see if the sentence has more than 1 word
							temp=sen[0].split()
							if len(temp)>1:
								sentences.append(sen[0])

					# one last check to ensure no faulty sentences got through
					sentences[:] = [x for x in sentences if x != ""]

					# the first sentence has to have the tag 1 in this usecase, but can be easily removed
					tags.append(1)
					# providing context for the next sentence
					print "here is the one before: "+str(sentences[0])+"\n"
					# going from the 2nd sentence to the 2nd last one
					for i in range(1,len(sentences)-1):
						valid= False
						while not valid:
							try:
								print "here is the one after: "+str(sentences[i+1])+"\n"
								tag=int(input("Please tag this sentence - "+str(sentences[i])+" : \n"))
								# ensuring the tags are valid
								if tag!=1 and tag!=0:
									print "Try again"
								else:
									valid=True
									tags.append(tag)
							except Exception as e:
								print e
								print "Try again"

					# last sentence in the document
					print "LAST\n"
					valid= False
					while not valid:
						try:
							print "here is the one before: "+str(sentences[len(sentences)-2])+"\n"
							tag=int(input("Please tag this sentence - "+str(sentences[len(sentences)-1])+" : \n"))

							if tag!=1 and tag!=0:
								print "Try again"
							else:
								valid=True
								tags.append(tag)
						except Exception as e:
							print e
							print "Try again"

					# creating a reviews object
					tR=Review(text,tags,sentences)
					# writing the object
					f1.write(str(tR))
					f1.write("\n")
				else:
					break
			k=k+1
