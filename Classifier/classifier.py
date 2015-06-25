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
print "\n"+len(all_words)


print "Calculating Frequency Distribution"
print "Selecting top 5000 Words"
all_words = nltk.FreqDist(w.lower() for w in all_words)
all_words= list(all_words)[:5000]



