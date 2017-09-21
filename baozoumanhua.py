#!/usr/bin/python
#coding=utf-8

import sys
from bs4 import BeautifulSoup
import urllib2
import MySQLdb
import json
import time
import chardet
import StringIO
import gzip
import requests

reload(sys)
sys.setdefaultencoding('utf-8')

headers = {}


for i in range(82, 1000):
	print i
	conn= MySQLdb.connect(
        	host='localhost',
        	port = 3306,
        	user='root',
        	passwd='',
        	db ='discovery',
        	charset="utf8"
        )
	bmUrl = 'http://baozoumanhua.com/catalogs/duanpian?page=%s&sv=1504235702' % (i)
	req = requests.get(bmUrl, headers=headers)
	req.encoding = 'utf-8'
	html = req.content
	
	soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
	tags = soup.find_all('div', 'article')
	curTime = int(time.time())
	cardType = 1
	authorId = 2

	for tag in tags:
		try:
			img = tag.find('img', 'lazy-img')['data-original']
			thumbnail = json.dumps([img])
			desc = tag.find('h2', 'newpost-title').a.text
			url = 'http://baozoumanhua.com' + tag.find('h2', 'newpost-title').a['href']
		
			print desc	
			print thumbnail		
			print url

			try:
				cur = conn.cursor()
				cur.execute("SET NAMES utf8");
				sql = "insert into dis_entertainment (type, author_id, description, thumbnail, url, date) select %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_entertainment WHERE url =%s)";
				cur.execute(sql,(cardType, authorId, desc, thumbnail, url, curTime, url))
			except Exception as err:
				print(err)
			finally:
				cur.close()
		except Exception as err:
			print(err)
			continue
	conn.commit()
	conn.close()

