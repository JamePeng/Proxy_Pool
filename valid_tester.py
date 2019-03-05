import aiohttp
import asyncio
from config import TEST_URL
from DB.db_operation import MongoOperator
from DB.db_config import MONGO_TABLE

class ValidTester(object): 
    test_url = TEST_URL

    # 校验测试初始化
    def __init__(self):
        self.__raw_proxies = None
        self.__usable_proxies = None
        self.db = MongoOperator()

    # 设置初始需校验数据
    def set_raw_proxies(self, raw_proxies):
        self.__raw_proxies = raw_proxies
        self.__usable_proxies = []


    # 测试一个代理
    async def test_one_proxy(self, proxy):
        async with aiohttp.ClientSession() as session:
            try:
                if isinstance(proxy, bytes): # 确保proxy是字符串数据
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + ("%s:%s" % (proxy['ip'], proxy['port']))
                print('Testing ', real_proxy)

                async with session.get(self.test_url, proxy=real_proxy, timeout=15) as response:
                    if response.status == 200: # 使用代理连接后访问正常
                        print('Valid proxy', proxy)
                        self.__usable_proxies.append(proxy) # 存入可用代理set
                    else:
                        print('Invalid proxy', proxy)
                        self.db.delete(proxy, filterone=True)

                        
            except (TimeoutError, ValueError, Exception):
                print('Exception ,Invalid proxy %s' % (proxy))
                self.db.delete(proxy, filterone=True)

    # 对队列中的代理进行测试
    def test(self):
        print('ValidTester is working')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_one_proxy(proxy) for proxy in self.__raw_proxies] # 对数据迭代检测
            loop.run_until_complete(asyncio.wait(tasks)) # 直到迭代检测任务完成
        except ValueError:
            print('Async Error')

    # 获取有用代理的set
    @property
    def usable_proxies(self):
        return self.__usable_proxies
