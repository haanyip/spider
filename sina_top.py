#!/usr/bin/python
#coding=utf-8

import sys
from bs4 import BeautifulSoup
import requests
import MySQLdb
import json
import time
import re

reload(sys)
sys.setdefaultencoding('utf-8')
conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='',
        db ='discovery',
        )

headers = {'Cookie':'SINAGLOBAL=7874049197247.797.1502333817538; _s_tentry=-; Apache=5109424248483.634.1502349040776; ULV=1502349040812:2:2:2:5109424248483.634.1502349040776:1502333817615; YF-Page-G0=734c07cbfd1a4edf254d8b9173a162eb; login_sid_t=5c75d66067400727a3fb26588c5d7849; UOR=,,cuiqingcai.com; SCF=ApIQCfW9rlKHFtvGhj-PhaLtpzDP0ukQq0XLPmoQ0WGP5XNXTl4biLcJmpMXzWdubPMTm3t7jxAyWiw4q9QOIiQ.; SUB=_2A250ii4kDeRhGedH61YZ8SnEzjyIHXVX_hjsrDV8PUNbmtBeLRXhkW8JHmy4ErXQ-HJWnxrmfOXzGTcWyQ..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFw70a09s3D8YxTSfd6Ph2M5JpX5K2hUgL.Fo24ehBReKMRSK52dJLoI7Uzqg8Vg-LB; SUHB=0nlfp6Ymcqmghy; ALF=1503107319; SSOLoginState=1502502516; un=cow007hunter@qq.com; wvr=6', 'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Referer':'http://d.weibo.com/623751_0'}

topUrl = 'http://d.weibo.com/623751_0?ajaxpagelet=1&__ref=/623751_0&_t=FM_150251840107928'
html = requests.get(topUrl, headers = headers).content
soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
scriptStr = str(soup.find(text=re.compile("text_cut")))
jsonStr = scriptStr[15:-1]
"""print jsonStr"""
j = json.loads(jsonStr)
cardType = 2
bloggerId = 2
curTime = int(time.time())

s = BeautifulSoup(j['html'], 'html.parser', from_encoding='utf-8')
tags = s.find('div', 'm_wrap').ul.find_all('li', 'pt_li')

for tag in tags:
	if(hasattr(tag.find('div', 'pic_mul'),'ul')):
		a = tag.find('div', 'text_box').div.a
		desc = str(a.text)
		url = 'http:' + a['href']
		pic = ''
		lis = tag.find('div', 'pic_mul').ul.find_all('li')
		imgs = []
		for li in lis:
			imgs.append(li.img['src'])

		thumbnail = json.dumps(imgs)
        	try:
                	cur = conn.cursor()
                	cur.execute("SET NAMES utf8");
                	sql = "insert into dis_article (type, blogger_id, content, thumbnail, url, date) select %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_article WHERE url = '"+url+"')";
                	cur.execute(sql,(cardType, bloggerId, desc, thumbnail, url, curTime))
        	except Exception as err:
                	print(err)
        	finally:
                	cur.close()
conn.commit()
conn.close()

		








