from scrapy import cmdline
import os
import time
cmdline.execute("scrapy crawl data -s LOG_FILE=spider.log".split())
'''
minute = input('请定义爬取周期(min):\n')
num = 0 #运行次数
while 1:
    print("第"+str(num+1)+"次爬取数据...\n")
    os.system('scrapy crawl data -s LOG_FILE=spider.log')
    # cmdline.execute("scrapy crawl data -s LOG_FILE=spider.log".split())
    time.sleep(float(minute)*60)
    num += 1
'''