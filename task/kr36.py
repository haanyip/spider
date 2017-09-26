#!/usr/bin/python
# coding=utf-8
from __init__ import *

def crawl(conn):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36', 'Referer':'http://d.weibo.com/623751_0'}
    headers['Cookie'] = "SINAGLOBAL=850798024487.8599.1503730488759; _s_tentry=baike.baidu.com; Apache=5612558624424.093.1504660628383; ULV=1504660629276:5:2:2:5612558624424.093.1504660628383:1504434385004; UOR=baike.baidu.com,widget.weibo.com,api.atkj6666.cn; YF-Page-G0=fc0a6021b784ae1aaff2d0aa4c9d1f17; login_sid_t=295608409916127c76c479c6a6987ef4; SSOLoginState=1504754252; SCF=ArBzyfBlpZsBETU1LRzngb_-mtG_XGiXTBHIIwT4Q4lab3CcQA2NSTXxvWS2fvEVyPNdjIYF721mxOqBY0_r4cg.; SUB=_2A250tMocDeRhGedH61YZ8SnEzjyIHXVXw7zUrDV8PUNbmtBeLU7ckW8yiJdgezYjuFUhum1dHJsfczbt6Q..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFw70a09s3D8YxTSfd6Ph2M5JpX5K2hUgL.Fo24ehBReKMRSK52dJLoI7Uzqg8Vg-LB; SUHB=0C1z1-rfwg4j2C; ALF=1536290251; un=cow007hunter@qq.com; wvr=6; wb_cusLike_1904817850=N";

    topUrl = 'http://36kr.com/api/info-flow/main_site/posts?per_page=10'
    html = requests.get(topUrl, headers = headers).content
    j = json.loads(html)
    cardType = 2
    bloggerId = 5
    tags = j['data']['items']

    for tag in tags:
        desc = tag['summary'].encode('utf-8')
        thumbnail = json.dumps([tag['cover']])
        url = 'http://36kr.com/p/%s.html' % (tag['id'])
        url_md5 = md5.md5(url).hexdigest()
        curTime = tag['published_at']
        t = time.strptime(curTime, "%Y-%m-%d %H:%M:%S")
        curTime = int(time.mktime(t))

        #print thumbnail
        #print url
        #print desc
        #print curTime
        #continue

        try:
            cur = conn.cursor()
            cur.execute("SET NAMES utf8");
            sql = "insert into dis_article (type, blogger_id, content, thumbnail, url, url_md5, date) select %s, %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_article WHERE url = '"+url+"')";
            cur.execute(sql,(cardType, bloggerId, desc, thumbnail, url, url_md5, curTime))
        except Exception as err:
            print(err)
        finally:
            cur.close()
    conn.commit()
    conn.close()

		








