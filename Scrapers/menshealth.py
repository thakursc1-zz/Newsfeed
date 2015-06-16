from bs4 import BeautifulSoup
import requests
import urlparse
import sqlite3
conn = sqlite3.connect('menshealth.db')
c=conn.cursor()
"""
c.execute('''CREATE TABLE articles (
type TEXT,
title TEXT PRIMARY KEY,
content TEXT)''')
"""

url="http://www.menshealth.com/"
topics = ["Health and Lifestyle","Diet and Fitness","Workout and muscles","Cardio","Yoga"]
for topic in topics:
    for p in range(0,10):
        print "entered in ",p
        r = requests.get("http://www.menshealth.com/search/mh-frontend/mh-prod/%s articles?page=%s"%(topic,p))
        res = r.text
        soup = BeautifulSoup(res)
        #print soup.prettify()
        res = soup.findAll('dt',{"class":"title"})
        #print res
        for i in res:
            try:
                article_url = i.a["href"]
                #article_url = urlparse.urljoin(url,article_url)
                #print article_url
                art = requests.get(article_url)
                art = art.text
                artsoup = BeautifulSoup(art)
                title = artsoup.find(id="page-title").get_text()
                title = title.encode('ascii','ignore')
                print "Title: ",title,"\n"
                #print "*"*50
                #print "\n"*2
                #print "ARTICLE-------->","\n"
                article = artsoup.find("div",{"class":"content_article"}
)
                tags = article.find("div",{"class":"article_keyword"}).get_text().encode('ascii','ignore')
                #print tags
                article = article.get_text().encode('ascii','ignore')
                strip = article.find("RELATED VIDEO:")
                article = article[:strip]
                strip = article.find("TAGS:")
                article = article[:strip]
                #print article
                dbinsert = tuple(("%s"%topic,title,article))
                c.execute("Insert into articles values (?,?,?)",dbinsert)
                conn.commit()
            except AttributeError:
                print"Skipped \n"
            except sqlite3.IntegrityError:
                c.execute("UPDATE articles SET type=? WHERE title=?" , [topic,title])
                print "*"*100
                print title ," changed to %s"%topic
                conn.commit()
conn.close()
