"""
Demonstrates how to use the gevent compatible scheduler to schedule a job that executes on 3 second
intervals.
"""
import sys
import configparser
import os
import time
import MySQLdb
from datetime import datetime
from apscheduler.schedulers.gevent import GeventScheduler


import task.sina_video as sina_video
import task.smzdm as smzdm
import task.kr36 as kr36
import task.sina_top as sina_top
import task.zhihu_daily as zhihu_daily
import task.chuangye as chuangye
import task.douban as douban
import task.qiushibaike as qiushibaike
import task.study163 as study163
import task.news as news
import task.video.baidu_amuse as baidu_amuse
import task.video.baidu_beauty as baidu_beauty
import task.video.baidu_history as baidu_history
import task.video.baidu_music as baidu_music
import task.video.baidu_society as baidu_society
import task.video.baidu_spoof as baidu_spoof
import task.video.baidu_star as baidu_star
import task.video.baidu_xiaopin as baidu_xiaopin


def get_conn(config):
    """
    create db connection
    """
    host = config.get('mysql', 'host')
    database = config.get('mysql', 'database')
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    port = int(config.get('mysql', 'port'))
    connect_timeout = int(config.get('mysql', 'connect_timeout'))
    charset = config.get('mysql', 'charset')
    retry_times = int(config.get('mysql', 'retry_times'))
    sleep_time = float(config.get('mysql', 'sleep_time'))
    con = ''
    for i in range(retry_times):
        try:
            con = MySQLdb.connect(
                host=host,
                db=database,
                user=user,
                passwd=password,
                port=port,
                connect_timeout=connect_timeout,
                charset=charset
            )
            break
        except Exception, e:
            time.sleep(sleep_time)
    if not con:
        # write_log('connect db failed')
        raise Exception(
            '[create_db] Database connection fails: a null connection is returned, ' + getTraceStackMsg() + ', error_msg: ' + str(
                e))

    return con


def tick():
    print('Tick! The time is: %s' % datetime.now())


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    config = configparser.ConfigParser()
    config.read("config.ini")

    scheduler = GeventScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(sina_video.crawl(get_conn(config)), 'interval', seconds=7200)
    scheduler.add_job(smzdm.crawl(get_conn(config)), 'interval', seconds=7200)
    scheduler.add_job(kr36.crawl(get_conn(config)), 'interval', seconds=7200)
    scheduler.add_job(sina_top.crawl(get_conn(config)), 'interval', seconds=600)
    scheduler.add_job(zhihu_daily.crawl(get_conn(config)), 'interval', seconds=86400)
    scheduler.add_job(chuangye.crawl(get_conn(config)), 'interval', seconds=86400)
    scheduler.add_job(douban.crawl(get_conn(config)), 'interval', seconds=86400)
    scheduler.add_job(qiushibaike.crawl(get_conn(config)), 'interval', seconds=86400)
    scheduler.add_job(study163.crawl(get_conn(config)), 'interval', seconds=600)
    scheduler.add_job(news.crawl(get_conn(config)), 'interval', seconds=600)

    scheduler.add_job(baidu_amuse.crawl(get_conn(config)), 'interval', seconds=3600)
    scheduler.add_job(baidu_beauty.crawl(get_conn(config)), 'interval', seconds=3600)
    scheduler.add_job(baidu_history.crawl(get_conn(config)), 'interval', seconds=3600)
    scheduler.add_job(baidu_music.crawl(get_conn(config)), 'interval', seconds=3600)
    scheduler.add_job(baidu_society.crawl(get_conn(config)), 'interval', seconds=3600)
    scheduler.add_job(baidu_spoof.crawl(get_conn(config)), 'interval', seconds=3600)
    scheduler.add_job(baidu_star.crawl(get_conn(config)), 'interval', seconds=3600)
    scheduler.add_job(baidu_xiaopin.crawl(get_conn(config)), 'interval', seconds=3600)

    g = scheduler.start()  # g is the greenlet that runs the scheduler loop
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        g.join()
    except (KeyboardInterrupt, SystemExit):
        pass
