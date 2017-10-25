#!/usr/bin/python
# coding=utf-8
from __init__ import *

def crawl(conn):
    ip = ['121.31.159.197', '175.30.238.78', '124.202.247.110']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    videoUrl = 'http://daily.zhihu.com/'
    req = requests.get(videoUrl, headers=headers)
    req.encoding = 'utf-8'
    html = req.content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    tags = soup.find_all('div', 'col-lg-4')
    curTime = int(time.time())
    cardType = 2
    bloggerId = 3

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    today = today.strftime('%Y-%m-%d')
    tomorrow = tomorrow.strftime('%Y-%m-%d')

    t = time.strptime(today, "%Y-%m-%d")
    start = int(time.mktime(t))
    t = time.strptime(tomorrow, "%Y-%m-%d")
    end = int(time.mktime(t))

    for tag in tags:
        aTags = tag.find_all('a', 'link-button')
        for aTag in aTags:
            url = 'http://daily.zhihu.com' + aTag['href']
            print url
            img = aTag.img['src']
            thumbnail = json.dumps([img])
            desc = aTag.span.contents
            curTime = random.randint(start, end)
            url_md5 = md5.md5(url).hexdigest()

            req = requests.get(url, headers=headers)
            req.encoding = 'utf-8'
            html = req.content
            # print html
            soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
            div = soup.find('div', 'main-wrap content-wrap')
            # 删掉没用的div
            more = div.find('div', 'view-more')
            more.extract()
            qr = div.find('div', 'qr')
            qr.extract()
            qs = div.find_all('div', 'question')
            for q in qs:
                if (str(q).find('客官，这篇文章有意思吗') > 0):
                    q.extract()
            html = cgi.escape(str(div), True)

            try:
                cur = conn.cursor()
                cur.execute("SET NAMES utf8");
                sql = "insert into dis_article (type, blogger_id, content, thumbnail, url, url_md5, html, date) select %s, %s, %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_article WHERE url = '" + url + "')";
                cur.execute(sql, (cardType, bloggerId, desc, thumbnail, url, url_md5, html, curTime))
            except Exception as err:
                print(err)
            finally:
                cur.close()
    conn.commit()
    conn.close()
