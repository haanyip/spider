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
import md5
import requests
from urllib import unquote
import random

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

headers = {'Accept-Encoding': 'gzip, deflate','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Cookie':'SINAGLOBAL=7874049197247.797.1502333817538; un=cow007hunter@qq.com; YF-Page-G0=d52660735d1ea4ed313e0beb68c05fc5; SCF=ApIQCfW9rlKHFtvGhj-PhaLtpzDP0ukQq0XLPmoQ0WGPTHPz5D9Miy2HTPjoi4vrOKtRuKgV3LjRVi9l713QXjY.; SUHB=0IIkRpYUgjwSIB; YF-V5-G0=2a21d421b35f7075ad5265885eabb1e4; _s_tentry=-; Apache=5109424248483.634.1502349040776; ULV=1502349040812:2:2:2:5109424248483.634.1502349040776:1502333817615; YF-Ugrow-G0=8751d9166f7676afdce9885c6d31cd61; SUB=_2AkMu0Z54dcPxrAJYmPwdzWzqaY1H-jydBPeOAn7uJhMyAxgv7m0rqSU4BuMNqJd6jT2JEr2ZNlHumYlTWA..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFw70a09s3D8YxTSfd6Ph2M5JpV2cSaU057ScyfdrxLM.WpMC4odcXt; login_sid_t=5c75d66067400727a3fb26588c5d7849; UOR=,,login.sina.com.cn; WBStorage=0c663978e8e51f06|undefined'}

#response = urllib2.urlopen('http://weibo.com/tv')
#buf = StringIO.StringIO(response.read())
#f = gzip.GzipFile(fileobj=buf)
#html = f.read()

videoUrl = 'http://weibo.com/tv'
req = requests.get(videoUrl, headers=headers)
req.encoding = 'utf-8'
html = req.content
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
div = soup.find('div', 'weibo_tv_top')
tags = div.find_all('a')
start = int(time.time())
end = start - 7200
cardType = 1
bloggerId = 1

for tag in tags:
	url = 'https://weibo.com' + tag['href']
	url_md5 = md5.md5(url).hexdigest()
	img = tag.find('img', 'piccut')
	imgSrc = 'http:' +  img['src']
	thumbnail = json.dumps([imgSrc])
	desc = tag.li.find('div','txt_cut').contents
	desc = str(desc[0]).encode('utf-8')
	"""print desc"""
	"""print chardet.detect(desc)"""

	req = requests.get(url, headers=headers)
	html = req.content
	soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
	video = soup.find('div', attrs={"node-type":"common_video_player"})
	data = video['action-data']
	items = data.split("&")
	video_url = ''
	for item in items:
		if 'video_src' in item:
			video_url = item[10:]
	video_url = 'http:%s' % (unquote(video_url))
	curTime = random.randrange(end, start, 200)

	try:
		cur = conn.cursor()
		cur.execute("SET NAMES utf8");
		sql = "insert into dis_article (type, blogger_id, content, thumbnail, url, url_md5, video_url, date) select %s, %s, %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_article WHERE url = '"+url+"')";
		cur.execute(sql,(cardType, bloggerId, desc, thumbnail, url, url_md5, video_url, curTime))
	except Exception as err:
		print(err)
	finally:
		cur.close()
conn.commit()
conn.close()

