# A script that creates a feature vector for each sentence in each sentence
# An updated version of the scoringForSegmentation.py
# Script logic starts at line 148
# Author: Rahul Khanna
import pickle
import pdb
from gensim import corpora, models, similarities, matutils
from reviewModules import *
from functions import *
import scipy.spatial.distance
import math

# loading the corpus for the LDA model
filename="../data/laptopReviews.txt"
stopwords = "../data/stop_words.txt"
reviewc = MyCorpus(filename, stopwords, 20000)

# a place to store all text and their actual LDA scores
textAndLdaScore=[]

# loading the LDA model with 18 topics
K=18
lda = models.ldamodel.LdaModel.load("../lda_states/ldapy"+str(K))

# feature function that returns the length of a sentence
def lengthOfSentenceScore(sentence):
	return len(sentence)

# constructs an array of size 18 with lda scores
def getLDAScores(text):
	scores=[]
	scores2=[]
	for i in range(0,K):
		scores.append(0)
		scores2.append(0)
	array=lda[reviewc.dictionary.doc2bow(reviewc.proc(text))]
	for entry in array:
		# trying to accentuate the differences between the likelihoods of a sentence
		# belonging to a certain topic
		score=math.exp(entry[1]*10)
		scores[entry[0]]=score
		scores2[entry[0]]=entry[1]

	textAndLdaScore.append((text,scores2))
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
	text=text.strip()
	return text

# constructs an LDA vector for a variable number (k) of sentences strung together
def constructLDAVector(arrayOfSentences,k):
	secondVector=joinSentences(arrayOfSentences,k)
	secondVector=getLDAScores(secondVector)
	return secondVector


# constructs the feature vector for each sentence
def constructFeatureVector(forwardThree,backThree):
	vector=[]
	# getting the LDA distribution for the current sentence and the next one (if possible)
	# called the forward sentence
	ldaSentenceVectorF=[]
	if len(forwardThree)>2:
		ldaSentenceVectorF=constructLDAVector(forwardThree,3)
	elif len(forwardThree)>1:
		ldaSentenceVectorF=constructLDAVector(forwardThree,2)
	else:
		ldaSentenceVectorF=constructLDAVector(forwardThree,1)
	# adding each topic distribution for the forward sentence to the feature vector
	for entry in ldaSentenceVectorF:
		vector.append(entry)

	# getting the LDA distribution for the current sentence and the previous one (if possible)
	# called the backward sentence
	ldaSentenceVectorB=[]
	if len(backThree)>2:
		ldaSentenceVectorB=constructLDAVector(backThree,3)
	elif len(backThree)>1:
		ldaSentenceVectorB=constructLDAVector(backThree,2)
	else:
		ldaSentenceVectorB=constructLDAVector(backThree,1)

	# adding each topic distribution for the backward sentence to the feature vector
	for entry in ldaSentenceVectorB:
		vector.append(entry)

	# adding the cosine difference between the "forward" and "backward" sentence to the feature vector
	vector.append(getCosineDifference(ldaSentenceVectorF,ldaSentenceVectorB))

	# adding the lengths of the two sentences to the feature vector
	vector.append(lengthOfSentenceScore(ldaSentenceVectorF))
	vector.append(lengthOfSentenceScore(ldaSentenceVectorB))

	return vector

# constructs the feature vector for each sentence
def createFeaturesForData(data):
	for reveiw in data:
		sentences=reveiw.sentences
		ldaSentenceTags=[]
		features=[]
		# for each sentence we create a feature vector
		for i in range(0,len(sentences)):
			forwardThree=[]
			backThree=[]

			# using one sentence isn't good enough for LDA to identify the topic distribution
			for j in range(i,min(len(sentences),i+3)):
				forwardThree.append(sentences[j])

			# same comment as above
			for j in range(max(0,(i-2)),i+1):
				backThree.append(sentences[j])

			# create feature
			features.append(constructFeatureVector(forwardThree,backThree))

			# for later usage, ignore for now
			doc_lda=lda[reviewc.dictionary.doc2bow(reviewc.proc(sentences[i]))]
			ldaTopic=[]
			maxProp=-1
			for entry in doc_lda:
				if entry[1]>maxProp:
					maxProp=entry[1]
					ldaTopic=[]
					ldaTopic.append(entry[0])
				elif entry[1]==maxProp:
					ldaTopic.append(entry[0])

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

createFeaturesForData(trainingData)
createFeaturesForData(testingData)

print len(testingData[0].features[0])

# write reviews here
# didn't want this to be a pickle file, so that I can visually see the features
with open("data/scoredReviewsAllFeaturesTrainingWithCosine","w") as f:
	for review in trainingData:
		f.write(str(review))
		f.write("\n")

with open("data/scoredReviewsAllFeaturesTestingWithCosine","w") as f:
	for review in testingData:
		f.write(str(review))
		f.write("\n")


with open("ldaText","w") as f:
	for entry in textAndLdaScore:
		f.write(str(entry))
		f.write("\n")


