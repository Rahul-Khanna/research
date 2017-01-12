# Script that was used for exploratory purposes of picking good features
# Namely used to determine which distance measure was best to use
# Author : Rahul Khanna
import pickle
import scipy.spatial.distance
import sys

option=int(sys.argv[1])

def getDifference(option,firstVector,secondVector):
	diff=0.0
	if option==1:
		diff=scipy.spatial.distance.euclidean(firstVector,secondVector)

	if option==2:
		diff=scipy.spatial.distance.cityblock(firstVector,secondVector)

	if option==3:
		diff=scipy.spatial.distance.cosine(firstVector,secondVector)

	return diff



data=[]

with open("taggedReviews/trainingData","rb") as f:
	temp=pickle.load(f)
	for obj in temp:
		data.append(obj)

with open("taggedReviews/testingData","rb") as f:
	temp=pickle.load(f)
	for obj in temp:
		data.append(obj)


option2=int(sys.argv[2])

# Looking at values when the label is 1 (sentence starts new segment)
segmentDistances=[]
segmentScore=0.0
segmentCount=0.0

# Looking at values when the label is 0 (sentence continues current segment)
continuationDistances=[]
continuationScore=0.0
continuationCount=0.0

for obj in data:

	tagList=obj.realTags
	ldaFeatures=obj.features

	if option2:
		start=0
		end=len(tagList)-1
	else:
		start=1
		end=len(tagList)

	for i in range(start,end):
		if option2:
			difference=getDifference(option,ldaFeatures[i][-1],ldaFeatures[i+1][-1])
			if tagList[i+1]==1:
				segmentDistances.append(difference)
				segmentScore+=difference
				segmentCount+=1

			else:
				continuationDistances.append(difference)
				continuationScore+=difference
				continuationCount+=1
		else:

			difference=getDifference(option,ldaFeatures[i][-1],ldaFeatures[i-1][-1])

			if tagList[i-1]==1:
				segmentDistances.append(difference)
				segmentScore+=difference
				segmentCount+=1

			else:
				continuationDistances.append(difference)
				continuationScore+=difference
				continuationCount+=1

segmentAverage=segmentScore/segmentCount

continuationAverage=continuationScore/continuationCount

sdSegment=0.0
sdContinuation=0.0


for i in range(0,len(segmentDistances)):
	sdSegment+=(segmentDistances[i]-segmentAverage)**2

if len(segmentDistances)>1:
	sdSegment=sdSegment/(len(segmentDistances)-1)

sdSegment=sdSegment**0.5


for i in range(0,len(continuationDistances)):
	sdContinuation+=(continuationDistances[i]-continuationAverage)**2

if len(continuationDistances)>1:
	sdContinuation=sdContinuation/(len(continuationDistances)-1)

sdContinuation=sdContinuation**0.5


print segmentCount
print segmentScore
print segmentAverage
print sdSegment

print continuationCount
print continuationScore
print continuationAverage
print sdContinuation
