# -*- coding: utf-8 -*-
import scrapy
import datetime
from Baidu_News.items import BaiduNewsItem
from scrapy.http import Request,FormRequest
import requests
from lxml import etree
import re
from urllib import parse
from Baidu_News.rec_news import rec_news
from Baidu_News.get_keyword import get_keyword
from scrapy_redis.spiders import RedisSpider
import redis
from scrapy import cmdline
import time as t
from Baidu_News.redisKey import get_redis_url
from Baidu_News.userAgents import get_random_agent
class BaidunewsSpider(RedisSpider):
    name = 'baidunews'
    # allowed_domains = ['https://www.baidu.com/s?tn=news']
    # start_urls = ['https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB']
    # redis_Host = "127.0.0.1"
    # redis_key = 'baidunews:start_urls'
    #
    # # 创建redis数据库连接
    # rediscli = redis.Redis(host=redis_Host, port=6379, db="0")
    #
    # # 先将redis中的requests全部清空
    # flushdbRes = rediscli.flushdb()
    # print(f"flushdbRes = {flushdbRes}")
    # keywords = get_keyword()
    # for i in keywords:
    #     i = ('').join(i)
    #     url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd={}'.format(i)
    #     rediscli.lpush(redis_key, url)
    get_redis_url()
    redis_key = 'baidunews:start_urls'

    # def parse(self,response):
    #     keywords = get_keyword()
    #     print(len(keywords))
    #     for k in keywords:
    #         # i = ('').join(i)
    #         # url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd={}'.format(i)
    #         SEARCH_KEYWORD = k
    #         # print('关键词：',SEARCH_KEYWORD)
    #         yield Request(url=response.url, callback=self.parsecond, meta={"SEARCH_KEYWORD": SEARCH_KEYWORD})
    #
    def parse(self,response):
        keywords = get_keyword()
        print(len(keywords))

        yield Request(url=response.url, callback=self.parsecond)


    def parsecond(self, response):
        print('lianjie:',response.url)
        item = BaiduNewsItem()
        searchword = re.compile('wd=(.*)')
        SEARCH_KEYWORD = ('').join(searchword.findall(response.url))
        SEARCH_KEYWORD = parse.unquote(SEARCH_KEYWORD)
        print('关键字：',SEARCH_KEYWORD)
        # url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd=%E8%AF%AD%E9%9F%B3%E8%AF%86%E5%88%AB'
        # url = response.meta['url']
        random_agent = '"' + get_random_agent() + '"'
        headers = {
            "User-Agent": random_agent
        }
        res = requests.get(response.url, headers=headers, verify=False)
        res.encoding = 'utf-8'
        selector = etree.HTML(res.text)
        # selector = Selector(response)
        infos = selector.xpath('//*[@id="content_left"]/div[3]')
        for info in infos:
            article_list = info.xpath('//*[@id="content_left"]/div[3]/div')
            for i in article_list:
                TITLE_list = ('').join(i.xpath('./h3/a//text()'))
                title =re.compile('\s+(.*)')
                TITLE_list = title.findall(TITLE_list)
                TITLE = TITLE_list[0]
                print('标题：',TITLE)
                URL = ('').join(i.xpath('./h3/a/@href'))
                print('链接：',URL)
                if i.xpath('./div/div[2]/p/text()'):
                     SOURCE_and_Time = ('').join(i.xpath('./div/div[2]/p/text()'))
                     source = re.compile('\S.*\w')
                     SOURCE_list = source.findall(SOURCE_and_Time)
                     SOURCE = SOURCE_list[0]
                     print('来源：',SOURCE)
                     time = ('').join(SOURCE_list[1])
                     print(time)
                     if len(time) < 10:                                     #处理时间
                         if '分钟' in time:
                             Get_timenumber = re.compile('\d+')
                             timenumber = ('').join(Get_timenumber.findall(time))
                             PUBTIME_list = datetime.datetime.now() + datetime.timedelta(minutes= -int(timenumber))
                             PUBTIME = PUBTIME_list.strftime("%Y-%m-%d %H:%M:%S")
                             print('发布时间：',PUBTIME)
                         elif '小时' in time:
                             Get_timenumber = re.compile('\d+')
                             timenumber = ('').join(Get_timenumber.findall(time))
                             PUBTIME_list = datetime.datetime.now() + datetime.timedelta(hours= -int(timenumber))
                             PUBTIME = PUBTIME_list.strftime("%Y-%m-%d %H:%M:%S")
                             print('发布时间：',PUBTIME)
                     else:
                         PUBTIME = time.replace('年','-').replace('月','-').replace('日','')
                         print('发布时间：',PUBTIME)

                else:
                    SOURCE_and_Time = ('').join(i.xpath('./div/p/text()'))
                    source = re.compile('\S.*\w')
                    SOURCE_list = source.findall(SOURCE_and_Time)
                    SOURCE = SOURCE_list[0]
                    print('来源：',SOURCE)
                    time = ('').join(SOURCE_list[1])
                    print(time)
                    if len(time) < 10:
                        if '分钟' in time:
                            Get_timenumber = re.compile('\d+')
                            timenumber = ('').join(Get_timenumber.findall(time))
                            PUBTIME_list = datetime.datetime.now() + datetime.timedelta(minutes= -int(timenumber))
                            PUBTIME = PUBTIME_list.strftime("%Y-%m-%d %H:%M:%S")
                            print('发布时间：',PUBTIME)
                        elif '小时' in time:
                            Get_timenumber = re.compile('\d+')
                            timenumber = ('').join(Get_timenumber.findall(time))
                            PUBTIME_list = datetime.datetime.now() + datetime.timedelta(hours=-int(timenumber))
                            PUBTIME = PUBTIME_list.strftime("%Y-%m-%d %H:%M:%S")
                            print('发布时间：',PUBTIME)
                    else:
                        PUBTIME = time.replace('年','-').replace('月','-').replace('日','')
                        print('发布时间：',PUBTIME)



                if i.xpath('./div/div[2]//text()'):                         #简介
                    BRIEF_list = ('').join(i.xpath('./div/div[2]//text()'))
                    # print(BRIEF_list)
                    if '前' in time:
                        brief = re.compile('前\s+(.*)')
                        BRIEF = ('').join(brief.findall(BRIEF_list))
                        print('简介：',BRIEF)
                    else:
                        brief = re.compile(':\d+\s+(.*)')
                        BRIEF = ('').join(brief.findall(BRIEF_list))
                        print('简介：',BRIEF)

                else:
                    BRIEF_list = ('').join(i.xpath('./div//text()'))
                    # print(BRIEF_list)
                    if '前' in time:
                        brief = re.compile('前\s+(.*)')
                        BRIEF = ('').join(brief.findall(BRIEF_list))
                        print('简介：',BRIEF)
                    else:
                        brief = re.compile(':\d+\s+(.*)')
                        BRIEF = ('').join(brief.findall(BRIEF_list))
                        print('简介：', BRIEF)

                # yield Request(URL, callback=self.parse_detail, meta={"TITLE":TITLE, "URL":URL, "SOURCE":SOURCE, "PUBTIME":PUBTIME, "BRIEF":BRIEF, "SEARCH_KEYWORD":SEARCH_KEYWORD}, dont_filter=True)
                yield Request(URL, callback=self.parse_detail,meta={"TITLE": TITLE, "URL": URL, "SOURCE": SOURCE, "PUBTIME": PUBTIME,"BRIEF": BRIEF, "SEARCH_KEYWORD": SEARCH_KEYWORD})


    def parse_detail(self, response):
        item = BaiduNewsItem()
        URL = response.meta['URL']
        TITLE = response.meta['TITLE']
        SOURCE = response.meta['SOURCE']
        PUBTIME = response.meta['PUBTIME']
        BRIEF = response.meta['BRIEF']
        SEARCH_KEYWORD = response.meta['SEARCH_KEYWORD']
        a = rec_news(response)
        htmlContent = a['body']
        # print(htmlContent)
        CONTENT = a['content']
        IMG_URL = a['img']
        print('图片链接：', IMG_URL)
        # print(CONTENT)
        INSERTTIME = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['TITLE'] = TITLE
        item['BRIEF'] = BRIEF
        item['URL'] = URL
        item['htmlContent'] = htmlContent
        item['CONTENT'] = CONTENT
        item['PUBTIME'] = PUBTIME
        item['INSERTTIME'] = INSERTTIME
        item['SOURCE'] = SOURCE
        item['SEARCH_KEYWORD'] = SEARCH_KEYWORD
        item['IMG_URL'] = IMG_URL
        yield item

















