import requests
import os
import re

def download_html(url:str,dirname='download',filename=''):
    # download html and save as dirname/filename
    # default:
    #   dirname :  peer directory 'download'
    #   filename : use title of the html (in title widget) as title.html
    resp = requests.get(url).text
    pat = r"<title>(.*?)</title>"
    if  filename == '':
        filename = re.search(pat, resp).group(1)+'.html'
    dirpath = os.path.join(os.getcwd(),dirname)
    filepath = os.path.join(dirpath,filename)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    with open(filepath, mode="w", encoding="utf-8") as f:
        f.write(resp)
    return filepath