import pymongo
import redis
import sys
sys.path.append("..")

from exceptions import PoolEmptyError, DatabaseOperationFailed
from pymongo.errors import ConnectionFailure
from DB.db_config import *

# Mongodb数据库操作
class MongoOperator(object):
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(MONGO_URL, MONGO_PORT, serverSelectionTimeoutMS=3)
            self.db = self.client[MONGO_DB]
        except ConnectionFailure:
            print("访问异常:数据库服务器不可用")
    
    # 导出数据插入到 MongoDB 数据库
    def insert(self, content, table_name=MONGO_TABLE):
        try:
            if self.db[table_name].find_one({'ip': content['ip']}): # 去重
                print('数据库已存在该ip ',content['ip'])
                return None
            else:
                self.db[table_name].insert(content)
                print('当条爬取数据已成功存储到mongodb数据库', content)
        except Exception:
            print('当条爬取数据存储失败', content)
            raise DatabaseOperationFailed

    # 删除条件下的元素
    def delete(self, conditions=None, table_name=MONGO_TABLE, filterone=False):
        try:
            if conditions and filterone==False:
                self.db[table_name].delete_many(conditions)
                print('删除多条数据的操作完成')
            elif conditions and filterone:
                self.db[table_name].delete_one(conditions)
                print('删除单条数据的操作完成')
            else:
                print('条件为空,无法进行删除操作')
        except Exception:
            print('删除元素操作失败')
            raise DatabaseOperationFailed

    # 删除特定表全部元素
    def delete_all(self, table_name=MONGO_TABLE):
        try:
            self.db[table_name].remove()
        except Exception:
            print('删除全部元素操作失败')
            raise DatabaseOperationFailed

    # 删除特定数据库
    def clean(self, db_name = MONGO_DB):
        self.client.drop_database(db_name)

    # 获取特定条件的元素
    def select(self, count=None, conditions=None, table_name=MONGO_TABLE):
        # 确保参数count合法
        if count:
            count = int(count)
        else:
            count = 0
        if count == 0:
            print('请求查询数量参数为0,结束操作')
            return None
        else:
            if conditions:
                conditions = dict(conditions)
            else:
                conditions = {}
            items = self.db[table_name].find(conditions, limit=count)
            results = []
            for item in items:
                result = {'ip': item['ip'],'port': item['port']}
                results.append(result)
            return results
    
    # 是否存在某个条件下的元素
    def is_exists(self, conditions=None, table_name=MONGO_TABLE):
        if conditions:
            conditions = dict(conditions)
        else:
            conditions = {}
        if self.db[table_name].find(conditions):
            return True
        else:
            return False

    @property
    def count(self, table_name=MONGO_TABLE):
        return self.db[table_name].count()

    # 关闭数据库连接
    def close(self):
        self.client.close()


# Redis数据库操作
class RedisOperator(object):
    def __init__(self):
        self.redis_pool = redis.ConnectionPool(
            host=REDIS_URL, port=REDIS_PORT, max_connections=20)
        if self.redis_pool:
            print('创建redis池成功')
            self.__conn = redis.Redis(connection_pool=self.redis_pool)
            print(type(self.__conn))
        else:
            print('创建redis池失败,无法创建连接')

    # 从左边获取一个新的代理
    def get(self, count=1):
        proxies = self.__conn.lrange(POOL_NAME, 0, count - 1)
        self.__conn.ltrim(POOL_NAME, count, -1)
        return proxies

    # 新验证后的代理ip从右边进入队列
    def put(self, proxy):
        return self.__conn.rpush(POOL_NAME, proxy)

    # 从右边送出最新的代理
    def pop(self):
        try:
            return self.__conn.rpop(POOL_NAME).decode('utf-8')
        except:
            raise PoolEmptyError

    # 获取redis队列的长度
    @property
    def queue_len(self):
        return self.__conn.llen(POOL_NAME)

    @property
    def size(self):
        return self.__conn.scard(POOL_NAME)

    # 清空redis队列
    def flush_db(self):
        self.__conn.flushall()



    
