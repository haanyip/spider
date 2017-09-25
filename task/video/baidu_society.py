#!/usr/bin/python
# coding=utf-8

def crawl(conn):
    headers = {}
    page = 1

    while True:
        print page
        amuseUrl = 'http://v.baidu.com/channel/society?format=json&pn=%s' % (page)
        page = page + 1
        req = requests.get(amuseUrl, headers=headers)
        req.encoding = 'utf-8'
        html = req.content
        jsonDict = json.loads(html)
        if (jsonDict.has_key('data') and jsonDict['data'].has_key('videos')):
            videos = jsonDict['data']['videos']
            cateId = 5

            for video in videos:
                title = video['title']
                img = video['imgv_url']
                url = video['url']
                duration = video['duration']
                html = requests.get(url, headers=headers).content
                pos = html.find('&video=')
                end = html.find('重置')
                video_url = html[pos + 7:end - 13]
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
                    cur = conn.cursor()
                    cur.execute("SET NAMES utf8");
                    sql = "insert into dis_video (title, url_md5, thumbnail, time,  url, video_url, category_id, date) values (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE video_url = %s"
                    cur.execute(sql, (title, url_md5, img, duration, url, video_url, cateId, timestamp, video_url))
                except Exception, e:
                    print e
                finally:
                    cur.close()
                    conn.commit()
                    conn.close()
