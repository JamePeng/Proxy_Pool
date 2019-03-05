@echo Launch mongoDB server
start mongod.exe --dbpath  D:\MongoDB\data\db
@ping 127.0.0.1:27017 -n 6 >nul
@echo Launch Proxy_tool
python d:/python_test/proxy_pool/proxy_pool.py