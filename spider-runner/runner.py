# spider-runner/runner.py
import sys
import os
import importlib.util
import json
import traceback
from datetime import datetime

def run_spider(script_path, main_module='main.py'):
    """
    安全地执行爬虫脚本
    """
    main_path = os.path.join(script_path, main_module)
    
    if not os.path.exists(main_path):
        raise FileNotFoundError(f"Main module {main_module} not found in {script_path}")
    
    # 添加脚本路径到Python路径
    sys.path.insert(0, script_path)
    
    try:
        # 动态导入并执行main模块
        spec = importlib.util.spec_from_file_location("__main__", main_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # 优先检查是否有Spider类（继承自BaseSpider）
        if hasattr(module, 'BaseSpider'):
            # 查找继承自BaseSpider的类
            for name in dir(module):
                obj = getattr(module, name)
                if hasattr(obj, '__bases__') and any(base.__name__ == 'BaseSpider' for base in obj.__bases__):
                    # 找到爬虫类，实例化并执行
                    spider_instance = obj()
                    if hasattr(spider_instance, 'execute'):
                        result = spider_instance.execute()
                        return {"status": "completed", "result": result, "message": "Script executed successfully"}
        
        # 检查是否有run函数
        if hasattr(module, 'run') and callable(getattr(module, 'run')):
            result = module.run()
            return {"status": "completed", "result": result, "message": "Script executed successfully"}
        else:
            return {"status": "completed", "message": "Script executed successfully (no run function)"}
            
    except Exception as e:
        return {"status": "failed", "error": str(e), "traceback": traceback.format_exc()}
    finally:
        # 清理路径
        if script_path in sys.path:
            sys.path.remove(script_path)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "Usage: python runner.py <script_path> [main_module]"}))
        sys.exit(1)
    
    script_path = sys.argv[1]
    main_module = sys.argv[2] if len(sys.argv) > 2 else 'main.py'
    
    result = run_spider(script_path, main_module)
    print(json.dumps(result))