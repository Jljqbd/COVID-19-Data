import numpy as np
import requests
import json
from openpyxl import Workbook
import time
import hashlib
import os
import datetime
import MySQLdb
from lxml import etree
headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36 Edg/83.0.478.44',
    'Authorization':'token 2fe1fd1949abcf4bc0ba0c1a92cf5780bbf8fe42',
    'Content-Type':'application/json',
    'method':'GET',
    'Accept':'application/json'
}
url = "https://api.github.com/rate_limit"
data = requests.get(url = url, headers = headers, verify = False)
json_data = json.loads(data.text)
print('ok')