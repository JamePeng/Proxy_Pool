from Spider.basespider import BaseSpider
from DB.db_operation import MongoOperator
from Spider.proxyspider_config import *
from pyquery import PyQuery as pq
import re
import time

# 快代理爬虫
class KuaidailiSpider(BaseSpider):
    name = 'KuaidailiSpider'

    # 解析快代理的网页
    def parse_one_page(self, html):
        if html == None:
            print('错误: 无法获取网页内容进行解析')
            return None
        pattern = re.compile(
            '<tr>\s.*?<td.*?IP">(.*?)</td>\s.*?<td.*?PORT">(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?' +
            '<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?<td.*?>(.*?)</td>\s.*?</tr>', re.S)  # 构造一个正则表达式
        results = re.findall(pattern, html)
        for item in results:
            yield{
                'ip': item[0],
                'port': item[1],
                'type': item[3].strip(),
                'location': item[4].strip(),
                #'response_time': item[5].strip(),
                'v_time': item[6].strip(),
            }

    # 对网页进行处理
    def gets(self, max_page):
        self.start_url = INHA_URL  # 默认使用高匿代理
        urls = [self.start_url.format(i)
                for i in range(self._counter, self._counter + max_page)]
        self._increment(max_page)
        db = MongoOperator()

        for url in urls:
            html = self.get_one_page(url)
            # print(html) debug
            for item in self.parse_one_page(html):
                print(item)  # 输出解析出来的单元
                # proxy_spider.export_to_file(item) # 导出json字典
                db.insert(item, MONGO_TABLE)  # 导出到数据库中

            time.sleep(1)
        db.close()

# 西刺代理爬虫
class XicidailiSpider(BaseSpider):
    name = 'XicidailiSpider'

    # 解析代理的网页
    def parse_one_page(self, html):
        if html == None:
            print('错误: 无法获取网页内容进行解析')
            return None
        doc = pq(html)
        for tr in doc('tr'):
            # for i in range(len(tr)):
            #     print(pq(tr).find('td').eq(i).text())
            '''
            <tr>
                <th class="country">国家</th>
                <th>IP地址</th>
                <th>端口</th>
                <th>服务器地址</th>
                <th class="country">是否匿名</th>
                <th>类型</th>
                <th class="country">速度</th>
                <th class="country">连接时间</th>
                <th width="8%">存活时间</th>
                <th width="20%">验证时间</th>
            </tr>
            '''
            td = pq(tr).find('td')  # 解析 tr标签块中存在的td标签
            ip = td.eq(1).text()
            port = td.eq(2).text()
            location = td.eq(3).text()
            type = td.eq(5).text()
            v_time = td.eq(9).text()
            if ip == '' or port == '':
                continue  # 若获取不到数据跳过这一段tr标签块

            yield {
                'ip': ip,
                'port': port,
                'location': location,
                'type': type,
                'v_time': v_time,
            }
        time.sleep(1)

    # 对网页进行处理
    def gets(self, max_page):
        self.start_url = XICINN_URL  # 默认使用高匿代理
        urls = [self.start_url.format(i)
                for i in range(self._counter, self._counter + max_page)]
        self._increment(max_page)
        db = MongoOperator()
        for url in urls:
            html = self.get_one_page(url)
            # print(html) debug
            # self.parse_one_page(html)
            for item in self.parse_one_page(html):
                print(item)  # 输出解析出来的单元
            #    proxy_spider.export_to_file(item) # 导出json字典
                db.insert(item, MONGO_TABLE)  # 导出到数据库中
        db.close()

