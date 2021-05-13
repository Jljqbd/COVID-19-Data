# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# -*- coding: utf-8 -*-
import pymysql
import os
import pandas as pd
import sys
import MySQLdb
from COVID_data.items import CovidDataItem
from scrapy.utils.project import get_project_settings
#from itemadapter import ItemAdapter

#pd.set_option()就是pycharm输出控制显示的设置
pd.set_option('expand_frame_repr', False)#True就是可以换行显示。设置成False的时候不允许换行
pd.set_option('display.max_columns', None)# 显示所有列
#pd.set_option('display.max_rows', None)# 显示所有行
pd.set_option('colheader_justify', 'centre')# 显示居中

class MySQLPipeline: 

    def open_spider(self, spider):
        db = spider.settings.get('MYSQL_DB_NAME', 'scrapy_default')
        host = spider.settings.get('MYSQL_HOST', 'localhost')
        port = spider.settings.get('MYSQL_PORT', '3306')
        user = spider.settings.get('MYSQL_USER', 'root')
        passwd = spider.settings.get('MYSQL_PASSWORD', 'root')
        try:
            self.conn = MySQLdb.connect(host=host, port=port, db=db, 
            user=user, passwd=passwd, charset='utf8')
            '''
            conn =  pymysql.connect(host='localhost', port=3306,
                    user='root', passwd='root', db='learn', charset='utf8')
            '''
            self.cur = self.conn.cursor()
            print('数据库连接成功！')
            print(' ')
        except:
            print('数据库连接失败！')
            sys.exit(1)
    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
    def process_item(self, item, spider):
        self.insert_db(item)
        return item
    def insert_db(self, item):
        files = item['filename']
        # basepath = "E:/VSC_project/VSC py/COVID_data/csv_file/"
        settings = get_project_settings()
        basepath = settings.get("DOWNFILE_PATH")
        '''
        i = 0  #计数器，后面可以用来统计一共导入了多少个文件
        for file in files:
            if file.split('.')[-1] in ['csv']:
                i += 1
        '''
        filename = files.split('.')[0]  #获取剔除后缀的名称
        filename = 'data_' + filename
        f = pd.read_csv(basepath + files, encoding='gbk')  #用pandas读取文件，得到pandas框架格式的数据
        columns = f.columns.tolist()  #获取表格数据内的列标题文字数据

        types = f.dtypes  #获取文件内数据格式
        field = []  #设置列表用来接收文件转换后的数据，为写入mysql做准备
        table = []
        char = []
        for items in range(len(columns)):  #开始循环获取文件格式类型并将其转换成mysql文件格式类型
            if 'object' == str(types[items]):
                char = '`' + columns[items] + '`' + ' VARCHAR(255)' 
            elif 'int64' == str(types[items]):
                char = '`' + columns[items] + '`' + ' INT'
            elif 'float64' == str(types[items]):
                char = '`' + columns[items] + '`' + ' FLOAT'
            elif 'datetime64[ns]' == str(types[items]):
                char = '`' + columns[items] + '`' + ' DATETIME'
            else:
                char = '`' + columns[items] + '`' + ' VARCHAR(255)'
            table.append(char)
            field.append('`' + columns[items] + '`')

        tables = ','.join(table)  #将table中的元素用，连接起来为后面写入mysql做准备
        fields = ','.join(field)

        filename = filename.replace('-','_')
        self.cur.execute('drop table if exists {};'.format(filename))
        self.conn.commit()

        #创建表格并设置表格的列文字跟累数据格式类型
        table_sql = 'CREATE TABLE IF NOT EXISTS ' + filename + '(' + 'id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,' + tables + ');'
        print('表:' + filename + ',开始创建数据表...')
        self.cur.execute(table_sql)
        self.conn.commit()
        print('表:' + filename + ',创建成功!')

        print('表:' + filename + ',正在写入数据当中...')
        f_sql = f.astype(object).where(pd.notnull(f), None)  #将原来从csv文件获取得到的空值数据设置成None，不设置将会报错
        values = f_sql.values.tolist()  #获取数值
        s = ','.join(['%s' for _ in range(len(f.columns))])  #获得文件数据有多少列，每个列用一个 %s 替代
        insert_sql = 'insert into {}({}) values({})'.format(filename,fields,s)
        self.cur.executemany(insert_sql, values)
        self.conn.commit()
        print('表:' + filename + ',数据写入完成！')
        print(' ')
        #print('文件导入数据库完成！一共导入了 {} 个CSV文件。'.format(i))
