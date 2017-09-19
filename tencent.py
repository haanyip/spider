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
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='discovery',
	charset="utf8"
        )

headers = {}

studyUrl = 'https://ke.qq.com/webcourse/index.html#course_id=144946&term_id=100164203&taid=721378412213810&vid=c1411sb0hg9'
req = requests.get(studyUrl, headers=headers)
req.encoding = 'utf-8'
html = req.content
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
div = soup.find_all('txpdiv')
print len(div)

exit()




curTime = int(time.time())

jsonDict = json.loads(html)

tags = jsonDict['results']['personalizedDataList']

for tag in tags:
	title = tag['title']
	desc = tag['desc']
	url = tag['wapUrl']
	t = 1;
	if tag['resourceType'] == 4:
		t = 2;
	imgs = []
	for img in tag['imgUrlList']:
		imgs.append(img)
	thumbnail = json.dumps(imgs)

	"""
	print t
	print title
	print desc
	print thumbnail
	print url
	print curTime
	"""

	try:
		cur = conn.cursor()
		cur.execute("SET NAMES utf8");
		sql = "insert into dis_study (type, title, description, thumbnail, url, date) select %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_study WHERE url =%s)";
		cur.execute(sql,(t, title, desc, thumbnail, url, curTime, url))
	except Exception as err:
		print(err)
	finally:
		cur.close()
conn.commit()
conn.close()

