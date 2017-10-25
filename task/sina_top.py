#!/usr/bin/python
# coding=utf-8
from __init__ import *

def crawl(conn):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Referer': 'http://d.weibo.com/623751_0'}
    headers[
        'Cookie'] = 'SINAGLOBAL=850798024487.8599.1503730488759; YF-V5-G0=a9b587b1791ab233f24db4e09dad383c; login_sid_t=83a9aab9b5ca474960e4019c6687bc0f; cross_origin_proto=SSL; YF-Ugrow-G0=56862bac2f6bf97368b95873bc687eef; _s_tentry=passport.weibo.com; Apache=4361455687243.6895.1505871438176; ULV=1505871438183:1:1:1:4361455687243.6895.1505871438176:; YF-Page-G0=fc0a6021b784ae1aaff2d0aa4c9d1f17; SSOLoginState=1506756944; UOR=,,baike.baidu.com; WBStorage=569d22359a08e178|undefined; wb_cusLike_0=N; WBtopGlobal_register_version=015f00677046c229; SCF=ArBzyfBlpZsBETU1LRzngb_-mtG_XGiXTBHIIwT4Q4laVN7Ynblfm5Ep5mogegWyVhqYeZkQ6aCFxqrHYPM_epw.; SUB=_2A2505F9tDeRhGedH61YZ8SnEzjyIHXVXkDelrDV8PUNbmtBeLWfckW8epdTXdkWg2IVGjOFujWkOvEYmuw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFw70a09s3D8YxTSfd6Ph2M5JpX5K2hUgL.Fo24ehBReKMRSK52dJLoI7Uzqg8Vg-LB; SUHB=0HTQtzU2SaDOj6; ALF=1508469181; un=cow007hunter@qq.com; httpsupgrade_ab=SSL; wb_cusLike_1904817850=N; wb_cmtLike_1904817850=1; wvr=6'

    topUrl = 'http://d.weibo.com/623751_0?ajaxpagelet=1&__ref=/623751_0&_t=FM_150251840107928'
    html = requests.get(topUrl, headers=headers).content
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    scriptStr = str(soup.find(text=re.compile("text_cut")))
    jsonStr = scriptStr[15:-1]
    """print jsonStr"""
    j = json.loads(jsonStr)
    cardType = 2
    bloggerId = 2
    # curTime = int(time.time())

    s = BeautifulSoup(j['html'], 'html.parser', from_encoding='utf-8')
    tags = s.find('div', 'm_wrap').ul.find_all('li', 'pt_li')

    for tag in tags:
        if (hasattr(tag.find('div', 'pic_mul'), 'ul')):
            a = tag.find('div', 'text_box').div.a
            desc = str(a.text)
            url = 'https:' + a['href']
            urlHtml = requests.get(url, headers=headers).content

            s = BeautifulSoup(urlHtml, 'html.parser', from_encoding='utf-8')
            curTime = s.find('span', 'time').text
            tuple = time.strptime(curTime, "%Y-%m-%d %H:%M:%S")
            curTime = int(time.mktime(tuple))
            url_md5 = md5.md5(url).hexdigest()

            pic = ''
            lis = tag.find('div', 'pic_mul').ul.find_all('li')
            imgs = []
            for li in lis:
                imgs.append(li.img['src'])

            thumbnail = json.dumps(imgs)
            try:
                cur = conn.cursor()
                cur.execute("SET NAMES utf8");
                sql = "insert into dis_article (type, blogger_id, content, thumbnail, url, url_md5, date) select %s, %s, %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS(SELECT url FROM dis_article WHERE url = '" + url + "')";
                cur.execute(sql, (cardType, bloggerId, desc, thumbnail, url, url_md5, curTime))
            except Exception as err:
                logging.debug(err)
            finally:
                cur.close()
    conn.commit()
    conn.close()
