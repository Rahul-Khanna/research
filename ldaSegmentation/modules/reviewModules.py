# Module file used for Review Segmentation
# Author : Rahul Khanna
import re
from gensim import corpora, models, similarities, matutils
import json

# The review object used by all scripts not in graphApproach
class Review():
	def __init__(self,id,review,realTags,sentences=None,features=None,predictedTags=None, predictedLDASentenceTags=None,k=None):
		self.id=id
		self.review=review
		self.realTags=realTags
		if not sentences:
			self.sentences=[]
		else:
			self.sentences=sentences
		if not features:
			self.features=[]
		else:
			self.features=features
		if not predictedTags:
			self.predictedTags=[]
		else:
			self.predictedTags=predictedTags
		if not predictedLDASentenceTags:
			self.predictedLDASentenceTags=[]
		else:
			self.predictedLDASentenceTags=predictedLDASentenceTags
		if not k:
			self.k=-1
		else:
			self.k=k


	def __repr__(self):
		output={
			"id": self.id,
			"review": str(self.review),
			"realTags": self.realTags,
			"sentences": self.sentences,
			"features": self.features,
			"predictedTags":self.predictedTags,
			"predictedLDASentenceTags":self.predictedLDASentenceTags,
			"k":self.k
		}
		return str(output)
	def __str__(self):
		output={
			"id": self.id,
			"review": str(self.review),
			"realTags": self.realTags,
			"sentences": self.sentences,
			"features": self.features,
			"predictedTags":self.predictedTags,
			"predictedLDASentenceTags":self.predictedLDASentenceTags,
			"k":self.k
		}
		return str(output)

# MyCorpus object used for loading the LDA model
# Written by Hamed Nilforoshan
class MyCorpus(object):
	def __init__(self, fname, stopf = None, V = None):
		self.fname = fname;
		self.file = open(fname,"r");
		stoplist = [];
		if stopf:
			with open(stopf,"r") as f:
				stoplist = map(lambda x: x.strip().lower(),f.readlines());
		self.dictionary = self.make_dict(stoplist, V);
	def rest(self):
		self.file.seek(0);
	def proc(self,line):
		return filter(lambda x: len(x) > 4, map(lambda x: x.strip(), re.sub(r'[0-9]+|\W',' ',line.strip().lower()).split()));
	def make_dict(self, stoplist = [], V = None):
		#self.reset();
		#for line in self.read_file():
			#print(self.proc(line))
		dictionary = corpora.Dictionary(self.proc(line) for line in self.read_file());
		stop_ids = [dictionary.token2id[sw] for sw in stoplist if sw in dictionary.token2id];
		dictionary.filter_tokens(stop_ids);
		dictionary.filter_extremes(5, .55);
		return dictionary;
	def read_file(self):
		with open(self.fname,"r") as f:
			for line in f:
				t = json.loads(line)["reviewText"]
				if (len(t.strip())> 10):
					yield t.strip();
	def __iter__(self):
		#self.reset();
		for line in self.read_file():
			bow = self.dictionary.doc2bow(self.proc(line));
			yield bow;
