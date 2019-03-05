# Proxy_Pool
My proxy_pool project with MongoDB
本代理池启动后处于后台自动维护状态.
之所以我选择采用mongodb,在于其适合大数据量存储,查询和增删改查操作相对于redis方便很多,更好维护数据

1. 需要在你的Windows系统环境下部署mongodb数据库环境(数据库操作中也加入了传统代理池使用的Redis操作).

2. MONGO 数据库配置,确保对于的数据库和表格已经建立
   MONGO_URL = 'localhost'
   MONGO_PORT = 27017
   MONGO_DB = 'proxy_ip'
   MONGO_TABLE = 'proxy_common'

3. config.py中包含了采集的页数限制,校验地址,校验周期和校验阈值

4. 如检测到数据库中的采集数据低于阈值将重新补充代理池, 如检测到数据库中的采集数据高于阈值的时候停止补充.

5. 校验器会定时校验数据库中的代理IP是否有效, 无效的代理ip将会从数据库中剔除

6. 使用上, 任意爬虫程序只需通过flask定制网页的get操作获取有效的代理ip,通过count操作获取代理池中有效代理ip的数量

7. 加入批处理文件, 适合开机启动的时候操作, (1)打开数据库服务, (2)加载数据库(默认路径:D:\MongoDB\data\db), (3)运行代理池
