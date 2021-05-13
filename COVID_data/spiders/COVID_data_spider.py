from scrapy import Request
from scrapy.spiders import Spider
from COVID_data.items import CovidDataItem
import json
import os
from scrapy.utils.project import get_project_settings
class COVIDSpider(Spider):
    # 定义爬虫名称
    name = "data"
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.44',
        'Authorization': 'token 2fe1fd1949abcf4bc0ba0c1a92cf5780bbf8fe42',
        # 59316d931215888f77f80acd9c7fd38969994214
        # 2fe1fd1949abcf4bc0ba0c1a92cf5780bbf8fe42
        'Content-Type':'application/json',
        'method':'GET',
        'Accept':'application/json'
    }
    '''
    settings = get_project_settings()
    headers = settings.get("HEADERS")
   # 获取初始 Request
    def start_requests(self):
        url = "https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports?ref=master"
        # 生成请求对象，设置 url , headers , callback
        yield Request(url,headers = self.headers,callback = self.parse)
    def property_parse(self, response):
        # downfile_path = "E:/VSC_project/VSC py/COVID_data/csv_file/"
        downfile_path = self.settings.get("DOWNFILE_PATH")
        print("正在爬取 " + response.meta['items'] + " ...")
        with open(downfile_path + response.meta['items'], 'w+', encoding='utf-8') as f:
            f.write(response.text)
            f.close()
        print('写入 '+ response.meta['items'] +' 成功...')
        item = CovidDataItem()
        item['filename'] = response.meta['items']
        yield item
    # 解析函数
    def parse(self,response):
        # 使用xpath定位到小说内容的div元素，保存到列表中
        # downfile_path = "E:/VSC_project/VSC py/COVID_data/csv_file/"
        downfile_path = self.settings.get("DOWNFILE_PATH")
        # print(downfile_path)
        item = CovidDataItem()
        if not os.path.exists(downfile_path):
            os.makedirs(downfile_path)
        json_data = json.loads(response.text)
        all_download_url_list = [json_data[i]['download_url'] for i in range(len(json_data))]  # 现有项目中的文件下载网址
        all_download_filename = [json_data[i]['name'] for i in range(len(json_data))]  # 现有项目中的文件列表
        exsit_file = os.listdir(downfile_path)  # 已下载的文件
        download_file_list = list(set(all_download_filename) - set(exsit_file))  # 需要下载的文件名称
        download_file_index = [all_download_filename.index(i) for i in download_file_list]  # 需要下载文件的下标
        #item['filename'] = [ all_download_filename[i] for i in download_file_index]  
        for i in download_file_index:
            print(all_download_url_list[i])
            item['filename'] =  all_download_filename[i]
            yield Request(all_download_url_list[i], headers=self.headers, callback=self.property_parse, meta=({'items': all_download_filename[i], 'item': item}))