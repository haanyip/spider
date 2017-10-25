#!/usr/bin/python
#coding=utf-8

from __init__ import *
headers = {}

def crawl(conn):
	for i in range(1, 34):
		skillUrl = 'https://ke.qq.com/course/list?mt=1004&st=2044&price_max=0&price_min=0&task_filter=0000000&page=' + str(i)
		req = requests.get(skillUrl, headers=headers)
		req.encoding = 'utf-8'
		html = req.content
		soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
		ul = soup.find('ul', 'course-card-list')
		curTime = int(time.time())
		cardType = 2
		tags = ul.find_all('li')
		for tag in tags:
			title = str(tag.h4.text).encode('utf-8');
			img = 'http:' + tag.img['src']
			thumbnail = json.dumps([img])
			url = 'http:' + tag.h4.a['href']

			try:
				cur = conn.cursor()
				cur.execute("SET NAMES utf8");
				sql = "insert into dis_skill (type, title, thumbnail, url, date) select %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_skill WHERE url =%s)";
				cur.execute(sql,(cardType, title, thumbnail, url, curTime, url))
			except Exception as err:
				print(err)
			finally:
				cur.close()
		conn.commit()
		conn.close()


