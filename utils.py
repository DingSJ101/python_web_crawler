import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import os
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}

def load_url(url:str,headers=headers,**kwargs):
    """
    if url indicate a html page, return requests response\n
        acquiescently use get() ;\n
        use post() if defined 'json' or 'data' as params\n
    if url indicate local file ,return beautifulsoup 
    """
    if re.match('http',url):
        if 'data' in kwargs or 'json' in kwargs:
            resp = requests.post(url,headers=headers, **kwargs)
        # if 'params' in kwargs:
        #     resp = requests.get(url,headers=headers, **kwargs)
        else:
            resp = requests.get(url,headers=headers, **kwargs)
        resp.encoding = 'utf-8'
        return resp
    with open(url, "r", encoding='utf-8') as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content,features="lxml")
        return soup



def download_html(url:str,dirname='download',filename=''):
    """
    download html and save as dirname/filename \n
    default:
      dirname :  peer directory 'download'
      filename : use title of the html (in title widget) as title.html
    """
    resp = requests.get(url,headers=headers)
    try:
        resp = requests.get(url)
        if resp.status_code != 200:
            return "None"
    except RequestException as e:
        return e
    resp.encoding = 'utf-8'
    
    pat = r"<title>(.*?)</title>"
    if  filename == '':
        filename = re.search(pat, resp.text).group(1)
    if filename.split('.')[-1] not in ['html','htm']:
        filename = filename+'.html'

    dirpath = os.path.join(os.getcwd(),dirname)
    filepath = os.path.join(dirpath,filename)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    with open(filepath, mode="w", encoding="utf-8") as f:
        f.write(resp.text)
    return filepath

def download_picture(url:str,dirname='download',filename='',skip = False):
    """
    download picture and save as dirname/filename \n
    default:
      dirname :  peer directory 'download'
      filename : use title of the html (in title widget) as title.html
    params:
        skip : False , dont download existed picture
    """
    resp = requests.get(url,headers=headers)
    pic = resp.content
    filetype = url.split('.')[-1] 
    if  filename == '':
        filename = url.split('/')[-1] 
    else :
        if not re.search("\.(gif|png|jpg|jpeg|webp|svg|psd|bmp|tif)+",filename):
            filename = filename + '.' + filetype
    dirpath = os.path.join(os.getcwd(),dirname)
    filepath = os.path.join(dirpath,filename)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    # print(resp.url)
    if skip and os.path.exists(filepath):
        print('%s ( already existed )'%resp.url)
    else:
        with open(filepath, mode="wb") as f:
            f.write(pic)
    return filepath