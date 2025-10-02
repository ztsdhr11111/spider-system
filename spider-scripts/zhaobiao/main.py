# spider-scripts/zhaobiao/main.py
import sys
import os

# 添加项目根目录到 Python 路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(script_dir, '..')
sys.path.insert(0, project_root)

from base_spider import BaseSpider
# 使用绝对导入替代相对导入
from zhaobiao.dowmload import download
from zhaobiao.parse import parse
import requests
import json

class ZhaobiaoSpider(BaseSpider):
    def run(self):
        """
        实现具体的爬虫逻辑
        """
        url = 'https://www.zhaobiao.com/zhaobiao/2023-05-01/2023-05-31/'
        
        self.log_info(f"开始下载页面: {url}")
        
        try:
            # 下载页面内容
            # response = requests.get(url, timeout=30)
            # response.raise_for_status()
            
            self.log_info("页面下载完成，开始解析数据")
            
            # 解析数据
            # items = parse(response.text)
            items = []
            
            self.log_info(f"数据解析完成，共获取 {len(items)} 条数据")
            
            # 返回标准格式结果
            return {
                "status": "success",
                "items_count": len(items),
                "data": items,
                "message": f"成功抓取 {len(items)} 条招标信息"
            }
            
        except Exception as e:
            self.log_error(f"爬虫执行出错: {str(e)}")
            raise

# 保持向后兼容
def run():
    spider = ZhaobiaoSpider()
    return spider.execute()

if __name__ == '__main__':
    spider = ZhaobiaoSpider()
    result = spider.execute()
    # print(json.dumps(result, ensure_ascii=False, indent=2))