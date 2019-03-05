import time

from config import VALID_CHECK_CYCLE, POOL_LOWER_THRESHOLD, POOL_UPPER_THRESHOLD, POOL_LEN_CHECK_CYCLE
from DB.db_operation import MongoOperator
from multiprocessing import Process
from pooladder import PoolAdder
from Webapi.webapi import app
from valid_tester import ValidTester


class Scheduler(object):

    @staticmethod
    def valid_proxy(cycle=VALID_CHECK_CYCLE):
        __db = MongoOperator()
        __tester = ValidTester()
        while True:
            print('正在校验代理IP')
            total = int(0.5 * __db.count)
            if total == 0:
                print('当前可用代理IP为空, 等待添加补充')
                time.sleep(cycle)
                continue
            raw_proxies = __db.select(total) # 从redis数据库获取原始代理ip
            __tester.set_raw_proxies(raw_proxies)
            __tester.test() # 校验原始代理ip
            time.sleep(cycle)


    @staticmethod
    def check_pool(lower_threshold=POOL_LOWER_THRESHOLD, 
                   upper_threshold=POOL_UPPER_THRESHOLD,
                   cycle=POOL_LEN_CHECK_CYCLE):
        __db = MongoOperator()
        adder = PoolAdder(upper_threshold)
        while True:
            if __db.count < lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)
        

    def run(self):
        print('Scheduler 开始运行.')
        valid_process = Process(target=Scheduler.valid_proxy)
        check_process = Process(target=Scheduler.check_pool)
        valid_process.start()
        check_process.start()
        app.run(debug=True)