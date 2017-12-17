import twitter
import json
import re
import pickle
import cPickle

#start process_tweet
def processTweet(tweet):
	# process the tweets

	#Convert to lower case
	tweet = tweet.lower()
	#Convert www.* or https?://* to URL
	tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet)
	#remove any hashtag
	tweet = re.sub('#[A-Za-z0-9]+', '',tweet)
	#Convert @username to AT_USER
	tweet = re.sub('@[^\s]+','',tweet)
	#Replace #word with word
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
	#remove numbers
	tweet = re.sub('[0-9]+', '', tweet)
	#remove alphabets occuring more than twice in a word. For example, woohhhoooo
	#is replaced by woohhoo
	expr = r'(.)\1{3,}'
	replace_by = r'\1\1'
	tweet = re.sub(expr, replace_by, tweet)
	#strip of punctuation
	tweet = re.sub('[|!@#$.,:?"''"-;~=&*{}^()_/\/]', '', tweet)
	#trim
	tweet = tweet.strip('\'"')
	#Remove additional white spaces
	tweet = re.sub('[\s]+', ' ', tweet)
	return tweet
#end


def getFeatureVector(tweet, stopwords):
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

# These are just strings to fetch the auth codes from the json file
consumer_key_string = 'consumer_key'
consumer_secret_string = 'consumer_secret'
access_token_string = 'access_token'
access_token_secret_string = 'access_token_secret'

auth_codes_file = open('auth_codes.json')
parsed_auth_codes_file = json.load(auth_codes_file)

# Fetch the strings from the parsed json
consumer_key = parsed_auth_codes_file[consumer_key_string]
consumer_secret = parsed_auth_codes_file[consumer_secret_string]
access_token = parsed_auth_codes_file[access_token_string]
access_token_secret = parsed_auth_codes_file[access_token_secret_string]

api = twitter.Api(consumer_key, consumer_secret, 
				access_token, access_token_secret)


# Search query
results = api.GetSearch(term = "fukrey", since="2017-12-06", until="2017-12-17", count=100, lang="en");


cleaned_tweets = []

for r in results:
	#print r.text
	clean_tweet = processTweet(r.text)
	#clean_tweet = removeStopWords(clean_tweet)
	cleaned_tweets.append(clean_tweet)
	print clean_tweet, '\n'





##############################################################################
# NOW WE BEGIN CLASSIFYING SHIT. SET THE NUMBER OF TWEETS AS IT IS IMPORTANT #
##############################################################################
num_tweets = 1000

# load the stopwords file and create feature vector
#Let us create a set of stopwords, basically a hashtable
stopwords = set()
stopwords_file = open('stopwords.txt', 'r')
#this loop is just for removing the trailing newline character at the end of each stopword
for word in stopwords_file:
	stopwords.add(word.strip())

# Fetch the featurelist and the idf from the dumped pickles
file_featurelist = open('featureList.pickle', 'r')
featureList = pickle.load(file_featurelist)

file_idf = open('idf.pickle', 'r')
idf = pickle.load(file_idf)

# Now, we create feature vector and classify
all_feature_vectors = []
for tweet in cleaned_tweets:
	feature_vector = getFeatureVector(tweet, stopwords)
	all_feature_vectors.append(feature_vector)

all_weight_vectors = []
for vector in all_feature_vectors:
	calculateWeight(vector, featureList, idf, all_weight_vectors, num_tweets)


##############################################################################
# Somewhere here, we also load the classifier if we are ever able to make it #
##############################################################################
# load it again
with open('classifier1k.pkl', 'rb') as fid:
    clf_loaded = cPickle.load(fid)
print cleaner_tweets[0]
print clf_loaded.predict(all_weight_vectors[0])
