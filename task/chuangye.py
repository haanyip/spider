#!/usr/bin/python
#coding=utf-8
from __init__ import *

def crawl(conn):
	headers = {'Accept-Encoding': 'gzip, deflate',
			   'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
			   'Cookie': 'SINAGLOBAL=7874049197247.797.1502333817538; un=cow007hunter@qq.com; YF-Page-G0=d52660735d1ea4ed313e0beb68c05fc5; SCF=ApIQCfW9rlKHFtvGhj-PhaLtpzDP0ukQq0XLPmoQ0WGPTHPz5D9Miy2HTPjoi4vrOKtRuKgV3LjRVi9l713QXjY.; SUHB=0IIkRpYUgjwSIB; YF-V5-G0=2a21d421b35f7075ad5265885eabb1e4; _s_tentry=-; Apache=5109424248483.634.1502349040776; ULV=1502349040812:2:2:2:5109424248483.634.1502349040776:1502333817615; YF-Ugrow-G0=8751d9166f7676afdce9885c6d31cd61; SUB=_2AkMu0Z54dcPxrAJYmPwdzWzqaY1H-jydBPeOAn7uJhMyAxgv7m0rqSU4BuMNqJd6jT2JEr2ZNlHumYlTWA..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFw70a09s3D8YxTSfd6Ph2M5JpV2cSaU057ScyfdrxLM.WpMC4odcXt; login_sid_t=5c75d66067400727a3fb26588c5d7849; UOR=,,login.sina.com.cn; WBStorage=0c663978e8e51f06|undefined'}

	videoUrl = 'http://feed.mix.sina.com.cn/api/roll/get?pageid=101&lid=1196&num=300&versionNumber=1.2.8&page=1&encode=utf-8'
	req = requests.get(videoUrl, headers=headers)
	req.encoding = 'utf-8'
	html = req.content
	jsonStr = json.loads(html)
	tags = jsonStr['result']['data']
	cardType = 1

	for tag in tags:
		url = tag['wapurl']
		thumbnail = ''
		if tag.has_key('images') and len(tag['images']) > 0:
			imgs = []
			for img in tag['images']:
				imgs.append(img['u'])
			thumbnail = json.dumps(imgs)
		else:
			thumbnail = json.dumps([tag['img']['u']])
		title = tag['title']
		desc = tag['summary']
		curTime = tag['intime']

		content = requests.get(url, headers=headers).content
		soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
		html = soup.find('article', 'art_box')
		# 图片补上http:前缀
		tags = html.find_all('img')
		for tag in tags:
			if (tag.get('data-src') is None):
				src = tag['src']
				tag['src'] = 'http:%s' % (src)
			else:
				src = tag['data-src']
				tag['data-src'] = 'http:%s' % (src)
		scripts = html.find_all('script')
		# 删掉javascript标签
		for script in scripts:
			script.extract()

		# 删掉关注的section
		sections = html.find_all('section')
		for section in sections:
			section.extract()

		html = cgi.escape(str(html), True)
		# print html
		# continue

		try:
			cur = conn.cursor()
			cur.execute("SET NAMES utf8");
			sql = "insert into dis_entrepreneurship (type, title, description, thumbnail, url, html, date) select %s, %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_entrepreneurship WHERE url = %s)";
			cur.execute(sql, (cardType, title, desc, thumbnail, url, html, curTime, url))
		except Exception as err:
			print(err)
		finally:
			cur.close()
	conn.commit()
	conn.close()

