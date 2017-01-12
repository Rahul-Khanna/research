# Module file used for Review Segmentation, graph Approach
# Author : Rahul Khanna

# The graph object used by all scripts in graphApproach
class Graph():
	def __init__(self,id,review,sentences,realTags,nodeDictionary=None,edgeDictionary=None,k=None,predictedTags=None,words=None,realTagsWordLevel=None,wordToSentence=None):
		self.id=id
		self.review=review
		self.realTags=realTags
		self.sentences=sentences

		if not nodeDictionary:
			self.nodeDictionary={}
		else:
			self.nodeDictionary=nodeDictionary

		if not edgeDictionary:
			self.edgeDictionary={}
		else:
			self.edgeDictionary=edgeDictionary

		if not k:
			self.k=-1
		else:
			self.k=k

		if  not predictedTags:
			self.predictedTags=[]
		else:
			self.predictedTags=predictedTags

		if not words:
			self.words=[]
		else:
			self.words=words

		if not realTagsWordLevel:
			self.realTagsWordLevel=[]
		else:
			self.realTagsWordLevel=realTagsWordLevel

		if not wordToSentence:
			self.wordToSentence={}
		else:
			self.wordToSentence=wordToSentence

	def __repr__(self):
		output={
			"id": self.id,
			"review": str(self.review),
			"realTags": self.realTags,
			"sentences": self.sentences,
			"nodeDictionary": self.nodeDictionary,
			"edgeDictionary": self.edgeDictionary,
			"k": self.k,
			"predictedTags": self.predictedTags,
			"words": self.words,
			"realTagsWordLevel": self.realTagsWordLevel,
			"wordToSentence": self.wordToSentence
		}

		return str(output)

	def __str__(self):
		output={
			"id": self.id,
			"review": str(self.review),
			"realTags": self.realTags,
			"sentences": self.sentences,
			"nodeDictionary": self.nodeDictionary,
			"edgeDictionary": self.edgeDictionary,
			"k": self.k,
			"predictedTags": self.predictedTags,
			"words": self.words,
			"realTagsWordLevel": self.realTagsWordLevel,
			"wordToSentence": self.wordToSentence
		}

		return str(output)



