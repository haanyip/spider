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

newsUrl = 'http://www.toutiao.com/api/pc/feed/?category=__all__&utm_source=toutiao&widen=1&tadrequire=false&as=A1C5994A6143029&cp=59A1A36012293E1'
req = requests.get(newsUrl, headers=headers)
req.encoding = 'utf-8'
html = req.content

jsonDict = json.loads(html)

tags = jsonDict['data']

for tag in tags:
	title = tag['title']
	url = 'http://www.toutiao.com' + tag['source_url']
	imgs = []
	if tag.has_key('image_list'):
		for img in tag['image_list']:
			imgs.append('http:' + img['url'])
	else:
		imgs.append('http:' + tag['image_url'])
	thumbnail = json.dumps(imgs)
	category = tag['chinese_tag']
	date = tag['behot_time']

	try:
		cur = conn.cursor()
		cur.execute("SET NAMES utf8");
		sql = "insert into dis_news (category, title, thumbnail, url, date) select %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_news WHERE url =%s)";
		cur.execute(sql,(category, title, thumbnail, url, date, url))
	except Exception as err:
		print(err)
	finally:
		cur.close()
conn.commit()
conn.close()

