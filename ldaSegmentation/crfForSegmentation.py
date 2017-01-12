# Script that actually trains a CRF Model off of the reviews data created in previous scripts
# Reads in testing and training data and evaluates the preformance of a Chain Crf model given the data
# Uses the pystruct package, https://pystruct.github.io/
# Author: Rahul Khanna

from pystruct.models import ChainCRF
from pystruct.learners import OneSlackSSVM
import numpy as np
from reviewModules import *
from functions import *
import pickle
import pdb

# training the crf:

listOfReviewFeatures=[]
listOfReviewTags=[]
listOfReviews=[]
with open("scoredReviewsAllFeaturesTrainingWithCosine") as f:
	for dic in f:
		temp=eval(dic)
		rows=len(temp['realTags'])

		# all possible features
		# features=np.zeros([rows,62],dtype=float)

		features=np.zeros([rows,39],dtype=float)
		tags=np.zeros([rows,], dtype=int)
		for i in range(0,rows):
			features[i]=np.array(list(temp['features'][i]))
			tags[i]=int(temp['realTags'][i])
		tags[0]=0
		listOfReviewFeatures.append(features)
		listOfReviewTags.append(tags)
		listOfReviews.append(convertToReview(temp))

X_train=np.array(listOfReviewFeatures)
Y_train=np.array(listOfReviewTags)

model=ChainCRF(n_states=2)
ssvm = OneSlackSSVM(model=model, C=0.1, max_iter=1000)

ssvm.fit(X_train, Y_train)
print len(ssvm.w)
print "Train Score: \n"
print(ssvm.score(X_train, Y_train))

zeroCount=0
totalCount=0.0
for tags in listOfReviewTags:
	for tag in tags:
		if tag==0:
			zeroCount+=1
	totalCount+=len(tags)

print zeroCount/totalCount

predictions=ssvm.predict(X_train)
for i in range(0,len(listOfReviews)):
	listOfReviews[i].predictedTags=predictions[i]


# testing
listOfReviewFeatures2=[]
listOfReviewTags2=[]
listOfReviews2=[]
with open("scoredReviewsAllFeaturesTestingWithCosine") as f:
	for dic in f:
		temp=eval(dic)
		rows=len(temp['realTags'])

		# all possible features
		# features=np.zeros([rows,62],dtype=float)

		features=np.zeros([rows,39],dtype=float)
		tags=np.zeros([rows,], dtype=int)
		for i in range(0,rows):
			features[i]=np.array(list(temp['features'][i]))
			tags[i]=int(temp['realTags'][i])
		tags[0]=0
		listOfReviewFeatures2.append(features)
		listOfReviewTags2.append(tags)
		listOfReviews2.append(convertToReview(temp))

X_test=np.array(listOfReviewFeatures2)
Y_test=np.array(listOfReviewTags2)

print "Test Score: \n"
print(ssvm.score(X_test, Y_test))

predictions=ssvm.predict(X_test)

for i in range(0,len(listOfReviews2)):
	listOfReviews2[i].predictedTags=predictions[i]


# store the results of crf for review:
# example:

with open("taggedReviews/trainingData","wb") as f:
	pickle.dump(listOfReviews,f)

with open("taggedReviews/testingData","wb") as f:
	pickle.dump(listOfReviews2,f)

with open("taggedReviews/visualTrainingData","w") as f:
	for i in range(0,10):
		f.write(str(listOfReviews[i]))
		f.write("\n")


