import pymysql


def get_keyword():
    db = pymysql.connect(host="192.168.3.76", user="root", passwd="123456", db="ai_intelligence")
    cursor = db.cursor()
    cursor.execute("SELECT cnKeyword from datacrawl_searchkeyword where (typeId LIKE '7;%' OR typeId LIKE '%;7;%' OR typeId LIKE '%;7' OR typeId = '7') AND priority!=1")
    keyword_tuple = list(cursor.fetchall())
    keyword = []
    for i in keyword_tuple:
        keyword_str = str(i)
        keyword.append(keyword_str[2:-3])
    db.close()
    return keyword

# a = get_keyword()
# for i in a:
#     i = ('').join(i)
#     url =('').join('https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd={}'.format(i))
#     print(url)

# db = pymysql.connect(host="192.168.3.76", user="root", passwd="123456", db="ai_intelligence")
# cursor = db.cursor()
# cursor.execute("SELECT cnKeyword from datacrawl_searchkeyword where (typeId LIKE '7;%' OR typeId LIKE '%;7;%' OR typeId LIKE '%;7' OR typeId = '7')")
# keyword = cursor.fetchall()
# print(keyword[1])
# db.close()