from config import MAX_COLLECT_PAGE
from DB.db_operation import MongoOperator
from Spider.proxyspider import KuaidailiSpider,XicidailiSpider
from valid_tester import ValidTester



class PoolAdder(object):
    def __init__(self, threshold):
        self.db = MongoOperator()
        self._threshold = threshold
        self.valid_tester = ValidTester()

    def is_over(self):
        if self.db.count >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        print('代理池添加器 PoolAdder 开始工作')
        while not self.is_over(): # 代理池未满继续添加代理ip
            self.update_proxy_ip()

    def update_proxy_ip(self, max_page=MAX_COLLECT_PAGE):
        kuaidaili_spider = KuaidailiSpider()
        kuaidaili_spider.gets(max_page)

        xici = XicidailiSpider()
        xici.gets(max_page)

            