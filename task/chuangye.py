#!/usr/bin/python
#coding=utf-8
from __init__ import *

def crawl(conn):
	headers = {'Accept-Encoding': 'gzip, deflate','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Cookie':'SINAGLOBAL=7874049197247.797.1502333817538; un=cow007hunter@qq.com; YF-Page-G0=d52660735d1ea4ed313e0beb68c05fc5; SCF=ApIQCfW9rlKHFtvGhj-PhaLtpzDP0ukQq0XLPmoQ0WGPTHPz5D9Miy2HTPjoi4vrOKtRuKgV3LjRVi9l713QXjY.; SUHB=0IIkRpYUgjwSIB; YF-V5-G0=2a21d421b35f7075ad5265885eabb1e4; _s_tentry=-; Apache=5109424248483.634.1502349040776; ULV=1502349040812:2:2:2:5109424248483.634.1502349040776:1502333817615; YF-Ugrow-G0=8751d9166f7676afdce9885c6d31cd61; SUB=_2AkMu0Z54dcPxrAJYmPwdzWzqaY1H-jydBPeOAn7uJhMyAxgv7m0rqSU4BuMNqJd6jT2JEr2ZNlHumYlTWA..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFw70a09s3D8YxTSfd6Ph2M5JpV2cSaU057ScyfdrxLM.WpMC4odcXt; login_sid_t=5c75d66067400727a3fb26588c5d7849; UOR=,,login.sina.com.cn; WBStorage=0c663978e8e51f06|undefined'}
	videoUrl = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=101&lid=1196&num=300&versionNumber=1.2.8&page=1&encode=utf-8'
	req = requests.get(videoUrl, headers=headers)
	req.encoding = 'utf-8'
	html = req.content
	jsonStr = json.loads(html)
	tags = jsonStr['result']['data']
	cardType = 1

	for tag in tags:
		url = tag['wapurl']
		if tag.has_key('images') and len(tag['images'])>0:
			imgs = []
			for img in tag['images']:
				imgs.append(img['u'])
			thumbnail = json.dumps(imgs)
		else:
			thumbnail = json.dumps([tag['img']['u']])
		title = tag['title']
		desc = tag['summary']
		curTime = tag['intime']

		try:
			cur = conn.cursor()
			cur.execute("SET NAMES utf8");
			sql = "insert into dis_entrepreneurship (type, title, description, thumbnail, url, date) select %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_entrepreneurship WHERE url = %s)";
			cur.execute(sql,(cardType, title, desc, thumbnail, url, curTime, url))
		except Exception as err:
			print(err)
		finally:
			cur.close()
	conn.commit()
	conn.close()

