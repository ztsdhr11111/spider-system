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


class ChallengeSpider(BaseSpider):
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
                }

                headers['safe'], headers['timestamp'] = get_safe()

                response = requests.post('https://www.python-spider.com/api/challenge1', cookies=cookies, headers=headers, data=data)
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



cookies = {
    'sessionid': 'k5vforkobe92wdgy0j9pagki5lig8k79',
    'no-alert': 'true',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.python-spider.com',
    'priority': 'u=1, i',
    'referer': 'https://www.python-spider.com/challenge/1',
    'safe': '55deed871c8472f11982ceaac3759000',
    'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'timestamp': '1760259059',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'sessionid=k5vforkobe92wdgy0j9pagki5lig8k79; no-alert=true',
}

def get_safe():
    a = '9622'
    timestamp = str(int(time.time()))
    combined = a + timestamp

    # base64 encode
    encoded = base64.b64encode(combined.encode('utf-8')).decode('utf-8')

    # md5 hash
    tokens = hashlib.md5(encoded.encode('utf-8')).hexdigest()

    return tokens, timestamp




# 保持向后兼容
def run():
    spider = ChallengeSpider()
    return spider.execute()

if __name__ == '__main__':
    spider = ChallengeSpider()
    result = spider.execute()
    print(json.dumps(result, ensure_ascii=False, indent=2))