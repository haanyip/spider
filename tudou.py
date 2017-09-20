#!/usr/bin/python
#coding=utf-8

import sys
import urllib2
import MySQLdb
import json
import time
import chardet
import StringIO
import datetime
import gzip
import md5
import requests
from bs4 import BeautifulSoup

# 数据库相关配置
DB_HOST = '127.0.0.1'
DB_PORT     = 3306
DB_DATABASE = 'discovery'
DB_USER     = 'root'
DB_PASSWORD = ''
RETRY_TIMES = 5
SLEEP_TIME = 1

global start
today = datetime.date.today()
today = today.strftime('%Y-%m-%d')
t = time.strptime(today, "%Y-%m-%d")
start = int(time.mktime(t))


def get_conn():
    """
    create db connection
    """
    for i in range(RETRY_TIMES):
        try:
            con = MySQLdb.connect(host=DB_HOST, db=DB_DATABASE, user=DB_USER, passwd=DB_PASSWORD, port=DB_PORT, connect_timeout=20, charset="utf8")
            break
        except Exception, e:
            time.sleep(SLEEP_TIME)
    if not con:
        write_log('connect db failed')
        raise Exception('[create_db] Database connection fails: a null connection is returned, ' + getTraceStackMsg() + ', error_msg: ' + str(e))

    return con


def getVideo(csrf_token, page, date):
	bloggerId = 7
	headers['X-CSRF-TOKEN'] = csrf_token
	headers['X-Requested-With'] = 'XMLHttpRequest'
	headers['Referer'] = videoUrl
	headers['Cookie'] = '_zpdtk=%s' % (csrf_token)
	moreUrl = 'http://new.tudou.com/sec/list?secCateId=10275&pl=24&pn=%s' % (page)

	req = requests.get(moreUrl, headers=headers)
	token = ''
	s = json.loads(req.content)
	if s.has_key('html'):
		conn = get_conn()
		cur = conn.cursor()
		token = req.cookies['_zpdtk']
		html = s['html']
		soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
		divs = soup.find_all('div', 'td-col')
		for div in divs:
			date = date + 600
			thumb = div.find('div', 'v-thumb')
			url = 'http:%s' % (thumb.find('a')['href'])
			url_md5 = md5.md5(url).hexdigest()
			img = thumb.find('img')['src']
			thumbnail = json.dumps([img])
			title = thumb.find('img')['alt']

			print title
			print url
			print thumbnail
			print date

			sql = "INSERT INTO dis_article (type, blogger_id, content, thumbnail, url, url_md5, date) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE video_url = ''";
			cur.execute(sql, (1, bloggerId, title, thumbnail, url, url_md5, date))
		cur.close()
		conn.commit()
		conn.close()
	else:
		print "page %s no more video!" % (page)

	return token



if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
	videoUrl = 'http://new.tudou.com/sec/%E6%8E%A8%E8%8D%90'
	req = requests.get(videoUrl, headers=headers)
	req.encoding = 'utf-8'
	token = req.cookies['_zpdtk']

	today = datetime.date.today()
	today = today.strftime('%Y-%m-%d')
	t = time.strptime(today, "%Y-%m-%d")
	start = int(time.mktime(t))

	for i in range(1, 9999):
		start = start + 14400
		if token == '':
			break
		else:
			token = getVideo(token, i, start)
			time.sleep(1)







