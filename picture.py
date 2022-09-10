import requests
import re
import os
from utils import download_html,download_picture,load_url

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
}
url = 'https://qq.yh31.com/zjbq/'

response = load_url(url)
# print(response.request.headers)
# print(response.status_code)
t = '<img src="(.*?)" alt="(.*?)" width="160" height="120">'
result = re.findall(t, response.text)
for img in result[:1]:
    download_picture(img[0],'picture',img[1],skip=True)
    # print(img)
    # res = requests.get(img[0])
    # print(res.status_code)
    # s = img[0].split('.')[-1]  #截取图片后缀，得到表情包格式，如jpg ，gif
    # with open(image + '/' + img[1] + '.' + s, mode='wb') as file:
    #     file.write(res.content)