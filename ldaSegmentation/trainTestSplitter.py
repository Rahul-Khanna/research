# A script that splits tagged data into test and training data sets
# Author: Rahul Khanna
from sklearn.cross_validation import train_test_split
import pdb
from reviewModules import *
from functions import *
import pickle


data=[]
testData=[]
trainData=[]

with open("taggedReviews/allReviews2") as f:
	for line in f:
		temp=eval(line)
		review=convertToReview(temp)
		review.realTags[0]=0
		data.append(review)


trainData,testData=train_test_split(data,test_size=0.15,random_state=1)

with open("taggedReviews/trainingData","wb") as f:
	pickle.dump(trainData,f)

with open("taggedReviews/testingData","wb") as f:
	pickle.dump(testData,f)

# just to view the actual reviews
with open("taggedReviews/visualTrainingData","w") as f:
	for i in range(0,10):
		f.write(str(trainData[i]))
		f.write("\n")



