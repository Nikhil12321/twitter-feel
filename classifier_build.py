import csv
import math
import string
import re
from sklearn.svm import LinearSVC

def getFeatureVector(tweet, stopwords, featureList, idf):
	featureVector = []
	# split tweet into words
	words = tweet.split()
	for w in words:
		# strip punctuation
		table = string.maketrans("", "")  # import string
		w = w.translate(table, string.punctuation)     

		# check if the word stats with an alphabet
		val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
		# ignore if it is a stop word
		if(w in stopwords or val is None or len(w) < 3):
			continue
		else:
			featureVector.append(w)

	# Since we only need unique elements in feature lists,
	# we do like this
	set_feature_vector = set(featureVector)
	for element in set_feature_vector:
		featureList.add(element)
		try:
			idf[element] += 1
		except:
			idf[element] = 1

	return featureVector


def calculateWeight(feature_vector, featureList, idf, all_weight_vectors, num_tweets):
	# We first make a list with all zeros of the size of the featureList
	size = len(featureList)
	weight_dict = {}
	weight = []
	feature_set = set(feature_vector)

	# Calculate the number of times each feature occurs in the document itself
	# This is used for calculation of tf
	for feature in feature_set:
		count = 0
		for f in feature_vector:
			if f == feature:
				count += 1
		weight_dict[feature] = count

	# Calculation of actual weights begins now
	# Check out that you have to explicitly make everything float
	# as python does not do that.
	size_of_feature_vector = len(feature_vector)*1.0
	for feature in featureList:
		value = 0
		if feature in weight_dict:
			value = weight_dict[feature]/size_of_feature_vector
			value = value*math.log(1.0*num_tweets/idf[feature])
		weight.append(value)

	all_weight_vectors.append(weight)


#Let us create a set of stopwords, basically a hashtable
stopwords = set()
stopwords_file = open('stopwords.txt', 'r')
for word in stopwords_file:
	stopwords.add(word.strip())

# We now make the feature vector for all the tweets
# We also make a feature list: which is basically a set of all features
# Also the idf dictionary is created. All this is created in the getFeatureVector
# function.

all_feature_vectors = []
all_sentiments = []
featureList = set()
idf = {}
clean_tweets = csv.reader(open('clean_data.csv' ,'rb'), delimiter=',')
for row in clean_tweets:
	tweet = row[0]
	sentiment = row[1]
	featureVector = getFeatureVector(tweet, stopwords, featureList, idf)
	all_feature_vectors.append(featureVector)
	all_sentiments.append(int(sentiment))


# Now, we calculate all the weights
all_weight_vectors = []
num_tweets = 10000
for vector in all_feature_vectors:
	calculateWeight(vector, featureList, idf, all_weight_vectors, num_tweets)


# KUDOS! Let us build the classifer now. I will be using sklearn's LinearSVC

clf = LinearSVC(random_state = 0)
clf.fit(all_weight_vectors, all_sentiments)

