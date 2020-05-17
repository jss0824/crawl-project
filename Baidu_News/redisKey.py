# -*- coding: utf-8 -*-
import redis
from Baidu_News.get_keyword import get_keyword
# 将start_url 存储到redis中的redis_key中，让爬虫去爬取
def get_redis_url():
    redis_Host = "127.0.0.1"
    redis_key = 'baidunews:start_urls'

    # 创建redis数据库连接
    rediscli = redis.Redis(host = redis_Host, port = 6379,db="0")

    # 先将redis中的requests全部清空
    flushdbRes = rediscli.flushdb()
    print(f"flushdbRes = {flushdbRes}")
    keywords = get_keyword()
    for i in keywords:
        i = ('').join(i)
        url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd={}'.format(i)
        rediscli.lpush(redis_key, url)
    return url
