import json
import requests


from Spider.basespider_config import *
from requests.exceptions import ReadTimeout, ConnectTimeout, RequestException


class BaseSpider():
    name = 'BaseSpider'

    # 初始化
    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.headers = {}
        self.timeout = 10
        self.start_url = ''
        self._counter = 1  # 计数器

    # 获取请求响应
    def request_get(self, url):
        try:
            response = requests.get(
                url, headers=self.headers, timeout=self.timeout)
            return response
        except ConnectTimeout:
            print('ConnectTimeout : 建立连接超时')
        except ReadTimeout:
            print('ReadTimeout : 已经建立连接, 客户端读取超时')
        except RequestException:
            print('RequestException : 处理请求过程发生异常')
        return None

    # 解析HTTP状态码
    def parse_static_code(self, response):
        s_code = response.status_code
        if s_code == 200:
            print('HTTP 200: 请求成功')
            return response.text  # 请求成功后返回网页内容
        elif s_code == 301:
            print('HTTP 301: 资源（网页等）被永久转移到其它URL')
        elif s_code == 302:
            print('HTTP 302: 资源（网页等）被暂时转移到其它URL')
        elif s_code == 403:
            print('HTTP 403: 没有权限访问此站')
        elif s_code == 404:
            print('HTTP 404: 请求的资源(网页等)不存在')
        elif s_code == 500:
            print('HTTP 500: 服务器内部错误，无法完成请求')
        elif s_code == 503:
            print('HTTP 503: 服务器当前无法处理请求, 可能请求过快')
        else:
            print('HTTP UNKNOWN_CODE: 请求异常,未知的请求返回码是%d' % s_code)
        return None

    # 处理解析网页的接口
    def parse_one_page(self, html):
        if html == None:
            print('无法获取网页内容')
            return None

    # 获取处理获得数据
    def gets(self, max_page=3):
        if max_page <= 0:
            print('非法最大检索页参数')

    # 尝试请求访问某个url
    def get_one_page(self, url, t_headers=None):
        if(t_headers == None):  # 若使用的时候未提供UA头,则使用默认的UA头
            self.headers = default_headers
        else:
            self.headers = t_headers

        response = self.request_get(url)  # 获取请求响应
        if response == None:  # 如果无响应
            print("本次请求无响应, 请求失败")
            return None

        return self.parse_static_code(response)  # 获取响应后的状态码进行识别

    # 导出字典数据到文件
    def export_to_file(self, content):
        with open('result.txt', 'a', encoding='utf8') as fh:
            fh.write(json.dumps(content, ensure_ascii=False) + '\n')
            fh.close()

    # 计数器增长 count
    def _increment(self, count):
        """子类用于增加计数器的方法
        :param count: 计数器增加量
        :return: None
        """
        self._counter += count

    # 清空计数器
    def _flush(self):
        """计数器刷新为 1
        :return: None
        """
        self._counter = 1
