#!/usr/bin/python
# coding=utf-8

def crawl(conn):
    headers = {
        'Cookie': 'q_c1=5e7d6fa129664721857f1a03a709b3d1|1502332594000|1502332594000; r_cap_id="Y2FiZTJlYWVlZDI3NGE4YmFiYzNkY2JmZGRhZjRiYjU=|1502332594|15ae49f0ae41d8f6a3e880e1d5a74633cdaeebcd"; cap_id="YTFjZGVjYTg1MzJmNDQxNmE5MzdkZjFhYTkyZDYzNzg=|1502332594|9ba4a0124462758d54c3f64ce037cfe734474d19"; d_c0="ACDCFraTMgyPTgSwANrW-OfSBR_qiCcLXWE=|1502332595"; _zap=910872b2-3374-4fa4-bf69-254faf6c1d63; z_c0=Mi4wQUJES3dQUHU0QWdBSU1JV3RwTXlEQmNBQUFCaEFsVk52MU96V1FBbXdyMW5MNWJHSTg1dUFadVBjcXQ3WmNpQjVR|1502332607|1e35a27454a67ff14332d6b1650a22e00b16ff58; _xsrf=652ea4e7-98a3-48f0-bf74-cd4fa0b998b5; __utma=51854390.1295841042.1502332597.1502332597.1502524413.2; __utmb=51854390.0.10.1502524413; __utmc=51854390; __utmz=51854390.1502524413.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.100-1|2=registration_date=20151020=1^3=entry_date=20151020=1; aliyungf_tc=AQAAAF/ZuUCQ2wcAosUnt9GpKrZsfopy; _gat=1; _ga=GA1.2.1295841042.1502332597; _gid=GA1.2.1235647149.1502524725',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    videoUrl = 'http://daily.zhihu.com/'
    req = requests.get(videoUrl, headers=headers)
    req.encoding = 'utf-8'
    html = req.content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    tags = soup.find_all('div', 'col-lg-4')
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
            img = aTag.img['src']
            thumbnail = json.dumps([img])
            desc = aTag.span.contents
            curTime = random.randint(start, end)
            url_md5 = md5.md5(url).hexdigest()

            try:
                cur = conn.cursor()
                cur.execute("SET NAMES utf8");
                sql = "insert into dis_article (type, blogger_id, content, thumbnail, url, url_md5, date) select %s, %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_article WHERE url = '" + url + "')";
                cur.execute(sql, (cardType, bloggerId, desc, thumbnail, url, url_md5, curTime))
            except Exception as err:
                print(err)
            finally:
                cur.close()
    conn.commit()
    conn.close()
