import requests
import re
import os
from utils import download_html,download_picture,load_url

url  = 'https://qq.yh31.com/zjbq/'
data={
    'kw':123,
}
url = '1.html'
# resp = load_url(url)
# print(resp.status_code)
soup = load_url(url)
print(soup.find_all('a'))