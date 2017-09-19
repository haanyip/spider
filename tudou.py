#!/usr/bin/python
#coding=utf-8

import sys
import urllib2
import MySQLdb
import json
import time
import chardet
import StringIO
import gzip
import requests
from bs4 import BeautifulSoup

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

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

videoUrl = 'http://new.tudou.com/sec/%E6%8E%A8%E8%8D%90'
req = requests.get(videoUrl, headers=headers)
req.encoding = 'utf-8'
cookie = req.cookies['_zpdtk']


headers['X-CSRF-TOKEN'] = cookie
headers['X-Requested-With'] = 'XMLHttpRequest'
headers['Referer'] = videoUrl
headers['Cookie'] = '_zpdtk=%s' % (cookie)
moreUrl = 'http://new.tudou.com/sec/list?secCateId=10275&pl=24&pn=1'

req = requests.get(moreUrl, headers=headers)
s = json.loads(req.content)
if s.has_key('html'):
	html = s['html']
	soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
	divs = soup.find_all('div', 'td-col')
	for div in divs:
		thumb = div.find('div', 'v-thumb')
		url = 'http:%s' % (thumb.find('a')['href'])
		img = thumb.find('img')['src']
		title = thumb.find('img')['alt']
		print title
		print url
		print img
else:
	print 'no more video!'
	exit()



exit()
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

