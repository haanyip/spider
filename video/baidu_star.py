#!/usr/bin/python
#coding=utf-8

import sys
from bs4 import BeautifulSoup
import urllib2
from urllib import unquote
import MySQLdb
import json
import time
import chardet
import StringIO
import gzip
import requests
import md5
import _mysql

# 数据库相关配置
DB_HOST = '127.0.0.1'
DB_PORT     = 3306
DB_DATABASE = 'discovery'
DB_USER     = 'root'
DB_PASSWORD = ''

RETRY_TIMES = 5


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



if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	headers = {}
	page = 1
	
	while True:
		print page
		amuseUrl = 'http://v.baidu.com/channel/star?format=json&pn=%s' % (page)
		page = page + 1
		req = requests.get(amuseUrl, headers=headers)
		req.encoding = 'utf-8'
		html = req.content
		jsonDict = json.loads(html)
		if(jsonDict.has_key('data') and jsonDict['data'].has_key('videos')):
			videos = jsonDict['data']['videos']
			cateId = 2

			for video in videos:
				title = video['title']
				img = video['imgv_url']
				url = video['url']
				duration = video['duration']
				html = requests.get(url, headers=headers).content
				pos = html.find('&video=')
				end = html.find('重置')
				video_url = html[pos+7:end-13]
				video_url = unquote(video_url)
				url_md5 = md5.md5(url).hexdigest()
			
				timeArray = time.strptime(video['update_time'], "%Y-%m-%d %H:%M:%S")
				timestamp = time.mktime(timeArray)

				"""
				print title
				print img
				print url
				print url_md5
				print video_url
				"""
				
				try:
					con = get_conn()
					cur = con.cursor()
					cur.execute("SET NAMES utf8");
					sql = "insert into dis_video (title, url_md5, thumbnail, time,  url, video_url, category_id, date) values (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE video_url = %s"
					cur.execute(sql, (title, url_md5, img, duration, url, video_url, cateId, timestamp, video_url))
				except Exception, e:
					print e
				finally:
					cur.close()
					con.commit()
					con.close()


