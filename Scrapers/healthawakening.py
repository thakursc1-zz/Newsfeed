from bs4 import BeautifulSoup
import requests
import urlparse
import sqlite3
conn = sqlite3.connect('healthawakening.db')
c=conn.cursor()

"""
c.execute('''CREATE TABLE articles (
type TEXT,
title TEXT PRIMARY KEY,
content TEXT)''')
"""

url="http://www.naturalawakeningsmag.com/"
topics = ["Yoga"]
for topic in topics:
    m=0
    for p in range(1,6):
        print "entered in ",p
        r = requests.get("http://www.naturalawakeningsmag.com/Search/index.php?cp_searchresults={0}&displayorder_ops_article=1&mod=CoreSearch&pid=93&query={1}&searchables=ops_article%2Cops_calendarevent%2Cops_geobasedata%2Ccore_page%2Cops_galleryitem%2Cops_customdata&si_searchresults={2}&sortby=RELEVANCY+DESC".format(p,topic,m))
        res = r.text
        soup = BeautifulSoup(res)
        #print soup.prettify()
        res = soup.find('table',{"class":"table table-striped"})
        res = res.findAll('a')
        m = m+20
        for i in res:
            try:
                article_url = i["href"]
                article_url = urlparse.urljoin(url,article_url)
                art = requests.get(article_url)
                art = art.text
                artsoup = BeautifulSoup(art)
                title = artsoup.find("h1",{"class":"article-title"}).get_text()
                title = title.encode('ascii','ignore')
                print "Title: ",title,"\n"
                #print "*"*50
                #print "\n"*2
                #print "ARTICLE-------->","\n"
                article = artsoup.find("article",{"class":"article page-content"})           
                article = article.findAll("p")
                article2=""
                for arti in article:
                    arti = arti.get_text().encode('ascii','ignore')
                    article2 = article2 + " " +arti
                #print article2
                dbinsert = tuple(("%s"%topic,title,article2))
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
