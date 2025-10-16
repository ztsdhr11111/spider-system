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
from utils.aes import AESCipher


class ChallengeSpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.key = 'aiding6666666666'
        self.aes = AESCipher()
    def run(self):
        """
        实现具体的爬虫逻辑
        """
        try:
            total_count = 0

            cookies = {
                    'no-alert': 'true',
                    'sessionid': 'ql7a59wokz3383dggpm3hhxpwj28w0es',
                }

            headers = {
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'accept-language': 'zh-CN,zh;q=0.9',
                'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'origin': 'https://www.python-spider.com',
                'priority': 'u=1, i',
                'referer': 'https://www.python-spider.com/challenge/55',
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

            for i in range(1, 101):
                print(f'正在处理第 {i} 页...')
                data = {
                    'page': i,
                }
                response = requests.post('https://www.python-spider.com/api/challenge55', cookies=cookies, headers=headers, data=data)
                result = response.json()['result']
                decrypt_text = self.aes.decode_ecb_pkcs7(result, self.key)
                result_json = json.loads(decrypt_text)
                for item in result_json['data']:
                    total_count += int(item['value'])

                

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