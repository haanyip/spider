#!/usr/bin/python
# coding=utf-8
from __init__ import *

def crawl(conn):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    categorys = ['news_society', 'news_entertainment', '__all__', 'news_fashion', 'news_sports', 'news_history',
                 'news_car', 'news_military', 'news_travel']

    for cat in categorys:
        newsUrl = 'http://www.toutiao.com/api/pc/feed/?category=%s&utm_source=toutiao' % (cat)
        req = requests.get(newsUrl, headers=headers)
        req.encoding = 'utf-8'
        html = req.content
        jsonDict = json.loads(html)
        tags = jsonDict['data']

        for tag in tags:
            title = tag['title']
            url = 'http://www.toutiao.com' + tag['source_url']
            imgs = []
            if tag.has_key('image_list'):
                for img in tag['image_list']:
                    imgs.append('http:' + img['url'])
            else:
                if (tag.has_key('image_url')):
                    imgs.append('http:' + tag['image_url'])
                else:
                    continue
            thumbnail = json.dumps(imgs)
            if False == tag.has_key('chinese_tag'):
                continue
            category = tag['chinese_tag']
            date = tag['behot_time']

            content = requests.get(url, headers=headers).content
            start = content.find('articleInfo')
            if (start == -1):
                continue
            content = content[start:-1]
            start = content.find('content')
            content = content[start + 10:-1]
            end = content.find("'")
            htmlStr = content[0:end]

            html_parser = HTMLParser.HTMLParser()
            htmlStr = html_parser.unescape(htmlStr)
            soup = BeautifulSoup(htmlStr, 'html.parser', from_encoding='utf-8')
            ads = soup.find_all('div', 'pgc-card')
            for ad in ads:
                ad.extract()
            html = cgi.escape(str(soup), True)

            print title

            try:
                conn = get_conn()
                cur = conn.cursor()
                cur.execute("SET NAMES utf8");
                sql = "insert into dis_news (category, title, thumbnail, url, html, date) select %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_news WHERE url =%s)";
                cur.execute(sql, (category, title, thumbnail, url, html, date, url))
            except Exception as err:
                print(err)
            finally:
                cur.close()
                conn.commit()
                conn.close()
