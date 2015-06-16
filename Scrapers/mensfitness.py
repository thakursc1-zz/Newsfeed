from bs4 import BeautifulSoup
import requests
import urlparse
import sqlite3
conn = sqlite3.connect('mensfitness.com.db')
c=conn.cursor()
"""
c.execute('''CREATE TABLE articles (
type TEXT,
title TEXT PRIMARY KEY,
content TEXT)''')

"""

url="http://www.mensfitness.com/"


topics = ["Health and Lifestyle","Diet and Fitness","Workout and muscles","Cardio","Yoga"]
for topic in topics:
    for p in range(0,8):
        print "entered in ",p
        r = requests.get("http://www.mensfitness.com/search/site/%s articles?page=%s"%(topic,p))
        res = r.text
        soup = BeautifulSoup(res)
        #print soup.prettify()
        res = soup.findAll("li",{"class":"search-result"})
        for i in res:
            try:
               article_url = i.strong.a["href"]
               article_url = urlparse.urljoin(url,article_url)
               art = requests.get(article_url)
               art = art.text
               artsoup = BeautifulSoup(art)
               title = artsoup.find("h1",{"class":"node-title"}).get_text()
               title = title.encode('ascii','ignore')
               print "Title: ",title,"\n"*2
               #print "ARTICLE-------->"
               article = artsoup.find("div",{"class":"field-item even","property":"content:encoded"})
               try:
                   rems= article.findAll("em")
                   article = article.get_text().encode('ascii','ignore')
                   for rem in rems:
                       rem = rem.get_text().encode('ascii','ignore')
                       article = article.replace(rem,"")
               except AttributeError:
                   article = article.get_text().encode('ascii','ignore')
               #print article
               #print "/"*100
               dbinsert = tuple(("%s"%topic,title,article))
               c.execute("Insert into articles values (?,?,?)",dbinsert)
               conn.commit()
            except AttributeError:
                print"Skipped","\n"
            except sqlite3.IntegrityError:
                c.execute("UPDATE articles SET type=? WHERE title=?" , [topic,title])
                print "*"*50
                print title ," changed to %s"%topic
                conn.commit()
conn.close()
