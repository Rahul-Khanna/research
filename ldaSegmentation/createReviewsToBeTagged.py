# Script that reads in amazon review data and creates the various datasets to be used
# Filters reviews by helpfulness score
# helpfulness = #ofPeopleWhoFoundThisReviewHelpful / #ofPeopleWhoHaveVotedOnThisReview
# Author: Rahul Khanna

import json
import random
from nltk.tokenize import RegexpTokenizer

def process(text):
	# tokenizer = RegexpTokenizer(r'\w+')
	# words = tokenizer.tokenize(text)
	# return " ".join(words).lower()
	return text


helpful=[]
unhelpful=[]
allReviews=[]

bad=0
medium=0
good=0

filenames = ["../data/laptopReviews.txt"]

# scoring reviews and creating the needed dataset
for filename in filenames:
	with open(filename) as f:
		for line in f:
			data=json.loads(line)
			# not enough votes on the review
			if (data["helpful"][1] <= 9):
					continue
			# scoring
			helpfulness = (data["helpful"][0] / float(data["helpful"][1]))

			# criteria for unhelpful reviews
			if (helpfulness <= 0.2 and data["helpful"][1] >=10):
				unhelpful.append((helpfulness,data["reviewText"]));
				bad+=1

			# criteria for helpful reviews
			if (helpfulness >= 0.90 and data["helpful"][1] >=30):
				helpful.append((helpfulness,data["reviewText"]))
				good+=1

			# medium reviews, no dataset made out of these
			if (helpfulness >=.25 and helpfulness <.75 and data["helpful"][1] >=10):
				medium+=1

			allReviews.append((helpfulness,data["reviewText"]))

	print (".....new file loaded: " + filename +".....")
	print ("Number of bad reviews (helpfulness<=0.2, #OfReviews>=10): "+ str(bad))
	print ("Number of good reviews (helpfulness>=0.9, #OfReviews>=30): "+ str(good))
	print ("Number of medium reviews (0.25<=helpfulness<=0.75, #OfReviews>=10): "+str(medium))

# sorting all reviews, greatest to smallest
allReviews.sort(key=lambda tup: tup[0], reverse=True)
# sorting the helpful reviews, greatest to smallest
helpful.sort(key=lambda tup: tup[0], reverse=True)

# writing out the various datasets
file = open("../inputs/allReviewsScored.txt", "w")
i=0
for review in allReviews:
	file.write(str(i)+"|*|*|*|"+str((review[0],process(review[1])))+"\n")
	i=i+1
file.close()

file = open("../inputs/allHelpfulScored.txt", "w")
i=0
for review in helpful:
	file.write(str(i)+"|*|*|*|"+str((review[0],process(review[1])))+"\n")
	i=i+1
file.close()

top20=int(round(0.2*len(helpful)))
file = open("../inputs/top20Scored.txt","w")
for i in range(0,top20):
	file.write(str(i)+"|*|*|*|"+str((helpful[i][0],process(helpful[i][1])))+"\n")
file.close()

# wanted to look only at helpful reviews under 4000 characters
shorterHelpful=[]
for i in range(0,len(helpful)):
	if len(helpful[i][1])<4000:
		shorterHelpful.append(helpful[i])

with open("../inputs/shorterHelpful.txt","w") as f:
	for review in shorterHelpful:
		f.write(review[1]+"\n\n")

# pick out 10 and 20 reviews randomly from the top 20% of reviews of the shorter helpful ones
top20=int(round(0.2*len(shorterHelpful)))
random10=random.sample([shorterHelpful[i] for i in range(0,top20)], 10)
random20=random.sample([shorterHelpful[i] for i in range(0,top20)], 20)

# writing out the random 10 and 20 reviews
file = open("../inputs/random10.txt", "w")
for review in random10:
	file.write(str((review[0],review[1].replace("\\","")))+"\n\n")
file.close()

file = open("../inputs/random20.txt", "w")
for review in random20:
	file.write(str((review[0],review[1].replace("\\","")))+"\n\n")
file.close()