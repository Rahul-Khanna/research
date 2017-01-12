# Script to evaluate the windowdiff score of the segmentation
# http://www.nltk.org/howto/metrics.html
# Author : Rahul Khanna
from nltk import windowdiff as wd
import pickle

train=[]
test=[]

with open("taggedReviews/trainingData","rb") as f:
	temp=pickle.load(f)
	for obj in temp:
		tup=("".join(str(e) for e in obj.realTags),"".join(str(e) for e in obj.predictedTags))
		train.append(tup)


with open("taggedReviews/testingData","rb") as f:
	temp=pickle.load(f)
	for obj in temp:
		tup=("".join(str(e) for e in obj.realTags),"".join(str(e) for e in obj.predictedTags))
		test.append(tup)


score=0.0
for tup in train:
	score+=wd(tup[0],tup[1],3)

print len(train)
print score
print (score/float(len(train)))

print "\n"

score=0.0
for tup in test:
	score+=wd(tup[0],tup[1],3)

print len(test)
print score
print (score/float(len(test)))


