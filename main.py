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
import logging
import logging.config
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
import task.video.baidu_cbeauty as baidu_beauty
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


def tick(param):
    source = eval(param)
    logger = logging.getLogger(param)
    logger.info('Starting task %s' % (param))
    conn = get_conn(config)
    source.crawl(conn)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    config = configparser.ConfigParser()
    config.read("config.ini")
    logging.config.fileConfig("logger.conf")

    scheduler = GeventScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(tick, 'interval', ['sina_video'], seconds=7200)
    scheduler.add_job(tick, 'interval', ['smzdm'], seconds=7200)
    scheduler.add_job(tick, 'interval', ['kr36'], seconds=7200)
    scheduler.add_job(tick, 'interval', ['sina_top'], seconds=600)
    scheduler.add_job(tick, 'interval', ['zhihu_daily'], seconds=86400)
    scheduler.add_job(tick, 'interval', ['chuangye'], seconds=86400)
    scheduler.add_job(tick, 'interval', ['douban'], seconds=86400)
    scheduler.add_job(tick, 'interval', ['qiushibaike'], seconds=86400)
    scheduler.add_job(tick, 'interval', ['study163'], seconds=600)
    scheduler.add_job(tick, 'interval', ['news'], seconds=600)

    scheduler.add_job(tick, 'interval', ['baidu_amuse'], seconds=3600)
    scheduler.add_job(tick, 'interval', ['baidu_beauty'], seconds=3600)
    scheduler.add_job(tick, 'interval', ['baidu_history'], seconds=3600)
    scheduler.add_job(tick, 'interval', ['baidu_music'], seconds=3600)
    scheduler.add_job(tick, 'interval', ['baidu_society'], seconds=3600)
    scheduler.add_job(tick, 'interval', ['baidu_spoof'], seconds=3600)
    scheduler.add_job(tick, 'interval', ['baidu_star'], seconds=3600)
    scheduler.add_job(tick, 'interval', ['baidu_xiaopin'], seconds=3600)

    g = scheduler.start()  # g is the greenlet that runs the scheduler loop
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        g.join()
    except (KeyboardInterrupt, SystemExit):
        pass
