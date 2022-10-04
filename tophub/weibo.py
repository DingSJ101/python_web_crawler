# from utils import utils
import sys,os,re
sys.path.append(os.path.realpath('.'))
sys.path.append('.')

from utils.utils import load_url,download_html,make_soup,decode_url,download_picture,load_json,request_header
from selenium import webdriver
import socket
import socks
import requests
# socks.set_default_proxy(socks.SOCKS5,"127.0.0.1",9050)
# socket.socket = socks.socksocket
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050, True)
socket.socket = socks.socksocket

url = "https://s.weibo.com/top/summary?cate=realtimehot"
# path = download_html(url,filename='weibo') # /home/dsj/workspace/python_web_crawler/download/weibo.html
# print(path)

# web = webdriver.Firefox()
# web.get(url)
# print(web.page_source)
url = "http://myip.ipip.net/"
# print(load_url(url))

# url = "http://checkip.amazonaws.com/"
# url = "http://api.myip.la/"
# url = 'https://example.com'
# proxies = {'http': 'socks5://127.0.0.1:9050',
#            'https': 'socks5://127.0.0.1:9050'}
# r = requests.get(url, headers = request_header(),proxies=proxies)

r = requests.get(url)
print(r.text)