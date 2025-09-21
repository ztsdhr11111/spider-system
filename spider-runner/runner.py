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
        
        # 如果main模块有run函数，则执行
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