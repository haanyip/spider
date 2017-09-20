#!/usr/bin/python
#coding=utf-8

import sys
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
import threadpool

# 数据库相关配置
DB_HOST = '127.0.0.1'
DB_PORT     = 3306
DB_DATABASE = 'discovery'
DB_USER     = 'root'
DB_PASSWORD = ''

RETRY_TIMES = 5
SLEEP_TIME = 1

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

def updateUrl(url):
    conn = get_conn()
    cur = conn.cursor()
    try:
        url_md5 = md5.md5(url).hexdigest()
        update_sql = "update dis_article set url_md5 = %s where url = %s"
        cur.execute(update_sql, (url_md5, url))
        print 'update %s successfully!' % (url)
    except Exception, e:
        print(e)
    finally:
        cur.close()
        conn.commit()
        conn.close()

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    conn = get_conn()
    cur = conn.cursor()
    aa = cur.execute("select url from dis_article where url_md5=''")
    info = cur.fetchmany(aa)
    cur.close()
    conn.close()

    urls = []
    for ii in info:
        url = ii[0]
        if url:
            urls.append(url)

    pool = threadpool.ThreadPool(8)
    reqs = threadpool.makeRequests(updateUrl, urls)
    [pool.putRequest(req) for req in reqs]
    pool.wait()