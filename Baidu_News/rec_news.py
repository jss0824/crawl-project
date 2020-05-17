import scrapy


def rec_news(response):
    """
    To recognize news information form a Scrapy http response body and export it!
    :param response: A scrapy.http.Response object
    :return: A dict object {'content': content, 'html': html}
    by:
    mywang88
    2018-12-04
    2018-12-05 增加了 t_line 阈值判据
    2018-12-10 提取文字信息重新封装 <p> 标签
    2018-12-12 debug 采集 div 中的 img
    2018-12-14 debug 试图用 domain 补全图片链接
    """
    print('rec_news 开始识别 ', response.url)
    # 假设新闻内容在一个 <div> 内，每自然段对应一组 <p> 标签
    # <p> 标签数量的阈值设定为：
    p_line = 3
    # 字符串的长度的阈值设定为：
    t_line = 12
    # 列出所有的 div article 节点
    div_list = response.css('div, article')
    # 选取满足条件的 <div>
    good_div = list()
    for div in div_list:
        p_child = div.xpath('p')
        # <div>的字节点中<p>节点的数量
        if len(p_child) >= p_line:
            p_number = 0
            for p in p_child:
                # <p>节点中字符串的长度
                p_text = p.css('::text').extract()
                if len(str(p_text)) > t_line + 4:
                    p_number += 1
            if p_number >= p_line:
                good_div.append(div)
    print('rec_news 筛选出<div>数量：', len(good_div))
    if len(good_div) == 0:
        print('rec_news 解析失败，退出函数')
        return 'rec_news 解析失败'


    # 生成 html 源码
    # 选取新闻节点下的所有 p img div 子节点
    node_list = good_div[0].xpath('p|img|div')
    # 初始化源码、图片、内容
    source = ''
    img = list()
    content = ''
    for node in node_list:
        # 处理图片节点
        if node.css('img'):
            url = response.url
            srcs = node.css('img::attr(src)').extract()
            for src in srcs:
                real_src = src[:]
                # 判别图片链接是否合法
                # 如果不合法
                if src[0:4] != 'http':
                    # 新华网的图片链接要专门构造
                    if 'xinhuanet' in url:
                        real_src = url.replace(url.split('/')[-1], '') + src[:]
                        source += '\n<img src=\"' + real_src + '\">'
                    else:
                        domain = 'http://' + url.split('/')[2] + '/'
                        real_src = domain + src[:]
                        source += '\n<img src=\"' + real_src + '\">'
                # 如果合法
                else:
                    source += '\n<img src=\"' + real_src + '\">'
                # 添加图片
                img.append(real_src)

        # 处理文字节点
        else:
            text = ''
            texts = []
            # 判断整段文字是否是一个链接，这样的链接大概率为广告
            if node.css('::text') != node.css('a::text'):
                texts = node.css('::text').extract()
            if texts:
                for t in texts:
                    text += t.strip().replace('\n', '')
            if text != '':
                source += '\n<p>' + text + '</p>'
                # 添加文本
                content += text

    # 构造网页源码
    body = '<body>\n<div>\n' + source + '\n</div>\n</body>'
    print('网页源码：\n', body)

    return {'content': content, 'body': body, 'img': img}

