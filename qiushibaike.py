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


for i in range(1, 13):
	conn= MySQLdb.connect(
        	host='localhost',
        	port = 3306,
        	user='root',
        	passwd='',
        	db ='discovery',
        	charset="utf8"
        )
	qiuUrl = 'https://www.qiushibaike.com/8hr/page' + str(i) 
	req = requests.get(qiuUrl, headers=headers)
	req.encoding = 'utf-8'
	html = req.content
	soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
	#maindiv = soup.find('div', 'main')
	#div = maindiv.find('div', 'col1')
	tags = soup.find_all('div', 'block')
	curTime = int(time.time())
	cardType = 1

	for tag in tags:
		url = 'https://www.qiushibaike.com' + tag.find('a', 'contentHerf')['href']
		spans = tag.find('a', 'contentHerf').find_all('span')
		desc = spans[0].text
		thumbnail = []
		thumb = tag.find('div', 'thumb')
		if thumb is not None:
			thumb = 'http:' + thumb.find('img')['src']
			thumbnail.append(thumb)
		thumbnail = json.dumps(thumbnail)
		try:
			cur = conn.cursor()
			cur.execute("SET NAMES utf8");
			sql = "insert into dis_entertainment (type, description, thumbnail, url, date) select %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_entertainment WHERE url =%s)";
			cur.execute(sql,(cardType, desc, thumbnail, url, curTime, url))
		except Exception as err:
			print(err)
		finally:
			cur.close()
	conn.commit()
	conn.close()

