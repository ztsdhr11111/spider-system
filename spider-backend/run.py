# run.py
from app import create_app
# from app.init_spiders import init_default_spiders

app = create_app()

# 初始化默认爬虫
# with app.app_context():
#     init_default_spiders()

if __name__ == '__main__':
    app.run(debug=True)