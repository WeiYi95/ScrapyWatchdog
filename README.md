# 介绍
可用于爬取国学大师网站（ http://www.guoxuedashi.com ）四库全书的数据。出现问题下载停止后，爬虫可自动重启。  
🚨由于国学大师网站整改，爬虫不再能获取数据。
# 配置
pip install watchdog  
pip install scrapy  
pip install requests  
pip install pypiwin32
# 运行
```
python scrapy_watchdog.py
```
🚨运行前需在start_scrapy.bat中添加路径