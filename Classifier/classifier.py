import nltk
from nltk import word_tokenize
import sqlite3
from nltk.corpus import stopwords

conn = sqlite3.connect("classifier.db")
c = conn.cursor()


print "Removing stop words\n"
articles = []
count = 0
for row in c.execute("SELECT * from words"):
    count = count+1
    if(count%40==0):
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

all_words = []

print "Collecting all words"
count=0
for article in articles:
    count = count+1
    if(count%40==0):
        print ".",
    for word in article[0]:
        all_words.append(word)
print "\n",len(all_words)


print "Calculating Frequency Distribution"
print "Selecting top 5000 Words"
all_words = nltk.FreqDist(w.lower() for w in all_words)
word_features = list(all_words)[:5000]
print len(word_features)



#############Feature Extractor function##################
def article_features(article):
    print ".",
    article_words = set(article[0])
    features ={}
    for word in word_features:
        features['contains({})'.format(word)] = (word in article)
    return features
##########################################################


print "\n\nExtracting Features of all 1500 articles....."
print "\n"
print "Type(articles)",type(articles[0])
feature_sets = [(article_features(article),topic) for (article,topic) in articles]

print "Featuresets are complete"
print "Distributing them as:"
print "Test set                : 500 aricles\n"
print "Train developer test set: 100 article\n"
print "Train set primary       : 900 articles\n"

test_set = feature_sets[:500]
train_set , train_test_set = feature_sets[500:601],feature_sets[601:1500]

print "Distribution Complete"

print "type(train_set[0][0])",type(train_set[0][0])






