# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import hashlib

class BaiduNewsPipeline(object):
    def process_item(self, item, spider):
        # conn = pymysql.connect(host="192.168.3.76", user="root", passwd="123456", db="recommend")
        conn = pymysql.connect(host="192.168.3.76", user="root", passwd="123456", db="ai_intelligence")
        cursor = conn.cursor()
        TITLE = self.replace_str(('').join(item['TITLE']))
        # AUTHOR = self.replace_str(('').join(item['AUTHOR']))
        PUBTIME = ('').join(item['PUBTIME'])
        BRIEF = self.replace_str(('').join(item['BRIEF']))
        URL = ('').join(item['URL'])
        IMG_URL = (';').join(item['IMG_URL'])
        CONTENT = self.replace_str(('').join(item['CONTENT']))
        SOURCE = self.replace_str(('').join(item['SOURCE']))
        Language = 'cn'
        MD5 = self.get_md5(TITLE, SOURCE)
        htmlContent = self.replace_str(('').join(item['htmlContent']))
        INSERTTIME = self.replace_str(item['INSERTTIME'])
        SEARCH_KEYWORD = self.replace_str(item['SEARCH_KEYWORD'])
        print("baidu新闻存储测试。。。。。。。", TITLE)
        sql = """insert into datasource_new(TITLE,BRIEF,PUBTIME,URL,SEARCH_KEYWORD,CONTENT,IMG_URL,SOURCE,MD5,Language,htmlContent,INSERTTIME) 
                                                                                          values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') ON duplicate KEY UPDATE MD5 = MD5""" % (
            TITLE, BRIEF, PUBTIME, URL, SEARCH_KEYWORD, CONTENT, IMG_URL, SOURCE, MD5, Language, htmlContent, INSERTTIME)
        print("baidu新闻数据正在存入数据库。。。。。。。。。。。。")
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return item

    def get_md5(self, title, source):
        str = title + source
        hl = hashlib.md5()
        hl.update(str.encode(encoding='utf-8'))
        return hl.hexdigest()

    def replace_str(self, strs):
        strs = strs.replace("'", "\\\'")
        strs = strs.replace("''", "\\\'")
        strs = strs.replace('"', '\\"')
        strs = strs.replace(">", "\>")
        strs = strs.replace("“", "\\”")
        strs = strs.replace("\\\'", "")
        # strs = strs.replace("\\", "")
        return strs

