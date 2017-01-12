# A script to create the feature vectors for each sentence in each review
# A little too over engineered in terms of features, a simpler version exists in scoringForSegmentation2.py
# Script logic really starts at line 208
# Author: Rahul Khanna

import pickle
import pdb
from gensim import corpora, models, similarities, matutils
from reviewModules import *
from functions import *
import scipy.spatial.distance
import math

# loading the corpus for the LDA model
filename="../inputs/segments/all_segments.txt"
stopwords = "../data/stop_words.txt"
reviewc = MyCorpus(filename, stopwords, 20000)

# loading the LDA model with 18 topics
K=18
lda = models.ldamodel.LdaModel.load("../lda_states/ldapy"+str(K))

# feature function that returns the length of a sentence
def lengthOfSentenceScore(sentence):
	return len(sentence)

# constructs array of size 18 with lda scores
# each score represents the likelihood of the text belonging to that topic
def getLDAScores(text):
	scores=[]
	for i in range(0,K):
		scores.append(0)

	array=lda[reviewc.dictionary.doc2bow(reviewc.proc(text))]
	for entry in array:
		scores[entry[0]]=entry[1]

	return scores

# gets cosine similarity between two vectors
def getCosineDifference(firstVector,secondVector):
	diff=scipy.spatial.distance.cosine(firstVector,secondVector)
	return diff

# takes in an array of sentences and strings k of them together
def joinSentences(arrayOfSentences,k):
	text=""
	for i in range(0,k):
		text+=(arrayOfSentences[i])
		text+=(". ")
	text.strip()
	return text

# constructs an LDA vector for a variable number (k) of sentences strung together
def constructLDAVector(arrayOfSentences,k):
	secondVector=joinSentences(arrayOfSentences,k)
	secondVector=getLDAScores(secondVector)
	return secondVector

# constructs feature vector for each sentence to be used in the crf model
def constructFeatureVector(forwardTwo,backTwo,nextThreeArray,lastThreeArray):
	vector=[]
	# getting the LDA distribution for the current sentence and the next one (if possible)
	# called the forward sentence
	ldaSentenceVectorF=[]
	if len(forwardTwo)>1:
		ldaSentenceVectorF=constructLDAVector(forwardTwo,2)
	else:
		ldaSentenceVectorF=constructLDAVector(forwardTwo,1)
	# adding each topic distribution for the forward sentence to the feature vector
	for entry in ldaSentenceVectorF:
		vector.append(entry)

	# getting the LDA distribution for the current sentence and the previous one (if possible)
	# called the backward sentence
	ldaSentenceVectorB=[]
	if len(backTwo)>1:
		ldaSentenceVectorB=constructLDAVector(backTwo,2)
	else:
		ldaSentenceVectorB=constructLDAVector(backTwo,1)
	# adding each entry to the feature vector
	for entry in ldaSentenceVectorB:
		vector.append(entry)

	# adding the cosine difference between the "forward" and "backward" sentence to the feature vector
	vector.append(getCosineDifference(ldaSentenceVectorF,ldaSentenceVectorB))

	# adding the lengths of the two sentences to the feature vector
	vector.append(lengthOfSentenceScore(ldaSentenceVectorF))
	vector.append(lengthOfSentenceScore(ldaSentenceVectorB))


	# adding cosine similarity scores of different groupings of the three next sentences with the backward sentence
	if nextThreeArray:
		# next sentence
		vector.append(getCosineDifference(ldaSentenceVectorB,constructLDAVector(nextThreeArray,1)))

		if len(nextThreeArray)>1:
			# next 2 sentences
			vector.append(getCosineDifference(ldaSentenceVectorB,constructLDAVector(nextThreeArray,2)))

		else:
			vector.append(0)

		if len(nextThreeArray)>2:
			# next 3 sentences
			vector.append(getCosineDifference(ldaSentenceVectorB,constructLDAVector(nextThreeArray,3)))

		else:
			vector.append(0)

	else:
		vector.append(0)
		vector.append(0)
		vector.append(0)

	# similarly for the previous 3 sentences and the forward sentence
	if lastThreeArray:

		vector.append(getCosineDifference(ldaSentenceVectorF,constructLDAVector(lastThreeArray,1)))

		if len(lastThreeArray)>1:

			vector.append(getCosineDifference(ldaSentenceVectorF,constructLDAVector(lastThreeArray,2)))
		else:
			vector.append(0)

		if len(lastThreeArray)>2:
			vector.append(getCosineDifference(ldaSentenceVectorF,constructLDAVector(lastThreeArray,3)))
		else:
			vector.append(0)

	else:
		vector.append(0)
		vector.append(0)
		vector.append(0)

	# similarly done for various combos of the last three sentences and the next three sentences
	if lastThreeArray and nextThreeArray:
		vector.append(getCosineDifference(constructLDAVector(lastThreeArray,1),constructLDAVector(nextThreeArray,1)))

		if len(lastThreeArray)>1 and len(nextThreeArray)>1:
			vector.append(getCosineDifference(constructLDAVector(lastThreeArray,2),constructLDAVector(nextThreeArray,2)))
		else:
			vector.append(0)

		if len(lastThreeArray)>2 and len(nextThreeArray)>2:
			vector.append(getCosineDifference(constructLDAVector(lastThreeArray,3),constructLDAVector(nextThreeArray,3)))
		else:
			vector.append(0)
	else:
		vector.append(0)
		vector.append(0)
		vector.append(0)

	return vector

# constructs the feature vector for each sentence
def createFeaturesForData(data):
	for reveiw in data:
		sentences=reveiw.sentences
		ldaSentenceTags=[]
		features=[]
		# for each sentence we create a feature vector
		for i in range(0,len(sentences)):
			nextThreeArray=[]
			lastThreeArray=[]
			forwardTwo=[]
			backTwo=[]

			# using one sentence isn't good enough for LDA to identify the topic distribution
			for j in range(i,min(len(sentences),i+2)):
				forwardTwo.append(sentences[j])

			# same comment as above
			for j in range(max(0,(i-1)),i+1):
				backTwo.append(sentences[j])

			# seeing if there are next sentences
			for j in range(i+1,min(len(sentences),(i+4))):
				nextThreeArray.append(sentences[j])

			# seeing if there are previous sentences
			for j in range(max(0,(i-3)),i):
				lastThreeArray.append(sentences[j])

			# create feature
			features.append(constructFeatureVector(forwardTwo,backTwo,nextThreeArray,lastThreeArray))

			# for later usage, ignore for now
			doc_lda=lda[reviewc.dictionary.doc2bow(reviewc.proc(sentences[i]))]
			ldaTopic=[]
			maxProb=-1
			for entry in doc_lda:
				if entry[1]>maxProb:
					maxProb=entry[1]
					ldaTopic=[]
					ldaTopic.append(entry[0])
				elif entry[1]==maxProb:
					ldaTopic.append(entry[0])
			# print doc_lda
			# print ldaTopic
			ldaSentenceTags.append(ldaTopic)
		# adding features to review objects
		reveiw.predictedLDASentenceTags=ldaSentenceTags
		reveiw.k=K
		reveiw.features=features

# logic starts here
trainingData=[]
testingData=[]

# reading in the data
with open("data/trainingData","rb") as f:
	temp=pickle.load(f)
	for obj in temp:
		trainingData.append(obj)

with open("data/testingData","rb") as f:
	temp=pickle.load(f)
	for obj in temp:
		testingData.append(obj)

# creating feature vectors for training and testing data
createFeaturesForData(trainingData)
createFeaturesForData(testingData)

print len(testingData[0].features[0])

# writing reviews here
# didn't want this to be a pickle file, so that I can visually see the features
with open("data/scoredReviewsAllFeaturesTrainingWithCosine","w") as f:
	for review in trainingData:
		f.write(str(review))
		f.write("\n")

with open("data/scoredReviewsAllFeaturesTestingWithCosine","w") as f:
	for review in testingData:
		f.write(str(review))
		f.write("\n")
