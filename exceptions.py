
# 数据库
class DatabaseOperationFailed(Exception):
    def __str__(self):
        str = '数据库操作失败'
        return str

# 代理池
class PoolEmptyError(Exception):
    def __str__(self):
        str = '代理池枯竭,请及时补充'
        return str
