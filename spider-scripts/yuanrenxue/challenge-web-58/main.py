import requests
import base64
import hashlib
import time
import json

import sys
import os

# 添加项目根目录到 Python 路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..', '..')
sys.path.insert(0, project_root)

from base_spider import BaseSpider


def md5_js_compat(data, length=16):
    """
    更贴近JavaScript版本行为的MD5实现
    """
    # 模拟JavaScript中的字符串处理
    if not isinstance(data, str):
        data = str(data)

    # 处理换行符，与JavaScript中的一致
    data = data.replace('\r\n', '\n')

    # 使用Python标准库计算MD5
    md5_hash = hashlib.md5()
    md5_hash.update(data.encode('utf-8'))
    hex_digest = md5_hash.hexdigest().lower()

    # 根据length参数返回相应长度的哈希值
    if length == 32:
        return hex_digest
    else:
        # 返回16位MD5（中间部分）
        return hex_digest[8:24]

# 针对你代码中的具体使用场景
def generate_request_token(page_number):
    """
    生成请求所需的token，与JavaScript中行为一致
    """
    return md5_js_compat(str(page_number))


class ChallengeSpider(BaseSpider):

    def __init__(self):
        super().__init__()
        self.cookies = {
            'no-alert': 'true',
            'sessionid': 'ql7a59wokz3383dggpm3hhxpwj28w0es',
        }

        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.python-spider.com',
            'priority': 'u=1, i',
            'referer': 'https://www.python-spider.com/challenge/58',
            'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            # 'cookie': 'no-alert=true; sessionid=ql7a59wokz3383dggpm3hhxpwj28w0es',
        }
    def run(self):
        """
        实现具体的爬虫逻辑
        """
        try:
            total_count = 0

            for i in range(1, 101):
                self.log_info(f'正在处理第 {i} 页...')
                data = {
                    'page': i,
                    'token': generate_request_token(i),
                }


                response = requests.post('https://www.python-spider.com/api/challenge58', cookies=self.cookies, headers=self.headers, data=data)
                numbers = response.json()['data']
                for number in numbers:
                    total_count += int(number['value'])

            print(total_count)
            self.log_info(f"数据解析完成，计算结果为：{total_count}")
            return {
                    "status": "success",
                    "items_count": total_count,
                    "data": [],
                    "message": f"计算结果为：{total_count}"
                }    
        except Exception as e:
            self.log_error(f"爬虫执行出错: {str(e)}")
            raise

# 保持向后兼容
def run():
    spider = ChallengeSpider()
    return spider.execute()

if __name__ == '__main__':
    spider = ChallengeSpider()
    result = spider.execute()
    print(json.dumps(result, ensure_ascii=False, indent=2))