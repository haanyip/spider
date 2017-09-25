#!/usr/bin/python
# coding=utf-8

def crawl(conn):
    headers = {}
    studyUrl = 'https://study.163.com/mob/recommend/dataList/v1'
    req = requests.post(studyUrl, headers=headers)
    req.encoding = 'utf-8'
    html = req.content
    curTime = int(time.time())
    cardType = 1
    bloggerId = 1

    jsonDict = json.loads(html)

    tags = jsonDict['results']['personalizedDataList']

    for tag in tags:
        title = tag['title']
        desc = tag['desc']
        url = tag['wapUrl']
        t = 1;
        if tag['resourceType'] == 4:
            t = 2;
        imgs = []
        for img in tag['imgUrlList']:
            imgs.append(img)
        thumbnail = json.dumps(imgs)

        """
        print t
        print title
        print desc
        print thumbnail
        print url
        print curTime
        """

        try:
            cur = conn.cursor()
            cur.execute("SET NAMES utf8");
            sql = "insert into dis_study (type, title, description, thumbnail, url, date) select %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_study WHERE url =%s)";
            cur.execute(sql, (t, title, desc, thumbnail, url, curTime, url))
        except Exception as err:
            print(err)
        finally:
            cur.close()
    conn.commit()
    conn.close()
