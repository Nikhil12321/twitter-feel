Analyzing positive and negative comments about anything on twitter through machine learning
Code has different files which do things independently of one another and DO NOT interact with each other

# How does it work

## Let's make the classifier
**preprocess_tweets_for_training.py** : Quite a nice tool to clean up tweets. Takes tweet in the form of a csv file where there are 2 columns
First column represents the tweet and the second the sentiment (1-positive, 2-negative). Processes the tweets, removes the crap and saves it
in the clean_data file

**Classifer_build.py** : takes the clean_data.csv and makes a classifier out of it. Since we are dealing with text here and I am using
**Linear SVC** classifer. It is slow on i3 machines. You can go upto 2000-3000 training tweets in an i5 I think. More on the i7. The reason for slowness is of course, the large feature vector of each tweet.
I have saved the created classifier in classifier_1k file. Meaning that it is made of a thousand training tweets.

**Fetch_and_classify.py** : here we fetch the tweet using Twitter API and classify the tweet. I am using tf-idf for making the feature vector hence I had to save the featureList and idf somewhere (made during the classifier making process in classifier_build.py). They are saved in .pickle files (thank god for python)
So this basically fetches only 100 tweets at once from the API (Limit of free twitter API) and classifies them as positive or negative sentiment and finds the percentage of sentiment.


## But I just want to use it for my college project

Don't worry. 

1. Just clone the repo. Open fetch_and_classify.py. Go to the line with
*results = api.GetSearch(term = "fukrey", since="2017-12-06", until="2017-12-17", count=100, lang="en");*
2. Replace term's value with the keyword of your search and *since* and *until* with a recent date combination (remember recemt. It will not fetch any tweets for older dates since it is a free API).
3. Run fetch_and_classify.py.

Hope it helps someone in need. Feel free to ask anything.
Thanks
