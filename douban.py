#!/usr/bin/python
#coding=utf-8

import sys
from bs4 import BeautifulSoup
import urllib2
import MySQLdb
import json
import time
import requests
import md5

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

headers = {'Cookie':'bid=CsGyT_pW-o0; __yadk_uid=eNufLoUDBxR559J1SkgwqVKoOyrzt2lr; ll="118282"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1502527848%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DaAM8yWpnwY2ebH_tLgEMqwALb3MmZd8VDk2RstslOy3%26wd%3D%26eqid%3Db753cdcb0002310700000006598ec164%22%5D; __utmt=1; _pk_id.100001.8cb4=927d34a87f4268d5.1502438774.3.1502527918.1502441429.; _pk_ses.100001.8cb4=*; __utma=30149280.2018316912.1502438775.1502441432.1502527850.3; __utmb=30149280.4.10.1502527850; __utmc=30149280; __utmz=30149280.1502527850.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap=1', 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

videoUrl = 'https://www.douban.com/explore/'
req = requests.get(videoUrl, headers=headers)
req.encoding = 'utf-8'
html = req.content
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
cardType = 2
bloggerId = 4

divs = soup.find_all('div', 'item')
for div in divs:
	imgA = div.find('a', 'cover')
	if hasattr(imgA, 'href'):
		url = imgA['href']
		url_md5 = md5.md5(url).hexdigest()
		img = str(imgA['style'])
		img = img[21:-1]
		img = img.split("?")
		img = img[0]
		thumbnail = json.dumps([img])
		desc = div.find('p').a.contents

		html = requests.get(url, headers=headers).content
		s = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
		d = s.find('div', 'note-header-container')
		curTime = d.span.text	
		tuple = time.strptime(curTime, "%Y-%m-%d %H:%M:%S")
		curTime = int(time.mktime(tuple))

		#print url
		#print thumbnail
		#print desc

		try:
			cur = conn.cursor()
			cur.execute("SET NAMES utf8");
			sql = "insert into dis_article (type, blogger_id, content, thumbnail, url, url_md5, date) select %s, %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_article WHERE url = '" + url + "')";
			cur.execute(sql,(cardType, bloggerId, desc, thumbnail, url, url_md5, curTime))
		except Exception as err:
			print(err)
		finally:
			cur.close()
conn.commit()
conn.close()

