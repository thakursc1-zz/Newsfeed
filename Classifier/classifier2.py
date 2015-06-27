import nltk
from nltk import word_tokenize
import sqlite3
from nltk.corpus import stopwords
from collections import Counter

conn = sqlite3.connect("classifier2.db")
c = conn.cursor()


print "Removing stop words\n"
articles = []
count = 0
for row in c.execute("SELECT * from words"):
    count = count+1
    if(count%20==0):
        print ".",
    intial = row[1].split()
    #print len(intial)
    stop_words = stopwords.words('english')
    final = [i for i in intial if i not in stop_words]
    #print len(final)
    articles.append((final,row[0]))


print "\n"

import random
random.shuffle(articles)
print len(articles)

all_words = []

print "Collecting all words"
count=0

for article in articles:
    count = count+1
    if(count%20==0):
        print ".",
    for word in article[0]:
        all_words.append(word)
print "\n",len(all_words)


print "Calculating Frequency Distribution"
print "Selecting top 1000 Words"
all_words = nltk.FreqDist(w.lower() for w in all_words)
word_features = [l for (l,m) in list(all_words.most_common(800))]
print word_features,"\n",len(word_features)



#############Feature Extractor function##################

def article_features(article):
    features ={}
    print ".",
    wordCount = Counter(article)
    for word in word_features:
        features['contains({})'.format(word)] = (word in article)
        features['count({})'.format(word)]    =  wordCount["%s"%word] 
    return features

##########################################################


print "\nExtracting Features of all 500 articles....."
print "\n"

feature_sets = [(article_features(article),topic) for (article,topic) in articles]

print "Featuresets are complete"
print "Distributing them as:"
print "Test set                : 300 aricles\n"
print "Train developer test set: 100 article\n"
print "Train set primary       : 100 articles\n"

train_set , train_test_set = feature_sets[:301],feature_sets[301:401]
test_set = feature_sets[401:]

print "Distribution Complete"

classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, train_test_set))
print(nltk.classify.accuracy(classifier, test_set))


