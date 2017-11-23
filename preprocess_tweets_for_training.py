import re
import string
import csv



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
	tweet = re.sub('[!@#$.,:?"''"-;~=&*{}^()_/\/]', '', tweet)
	#trim
	tweet = tweet.strip('\'"')
	#Remove additional white spaces
	tweet = re.sub('[\s]+', ' ', tweet)
	return tweet
#end



raw_file = '/home/nikhil/data/main_data_raw.csv'
clean_file = 'clean_data.csv'

#Let us make all the tweets neat and clean and insert them into another csv
raw_tweets = csv.reader(open(raw_file, 'rb'), delimiter=',')

# take only 100 tweets
num_tweets = 10000

# take all the data and insert it into the new csv
i = 0

csv_writer = open(clean_file, 'w')
writer = csv.writer(csv_writer)

for row in raw_tweets:
	i += 1
	row_new = []
	row_new.append(processTweet(row[0]))
	row_new.append(row[1])
	writer.writerow(row_new)
	# to exit when the amount of test cases have been reached
	if i==num_tweets:
		break

# Thats it! your data cleaned!