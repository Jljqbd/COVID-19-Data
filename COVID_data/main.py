#!/usr/bin/env python
#-*- coding:utf-8 -*-

from scrapy.cmdline import execute

#执行 scrapy 内置的函数方法execute，  使用 crawl 爬取并调试，最后一个参数jobbole 是我的爬虫文件名
execute(['scrapy', 'crawl', 'data'])