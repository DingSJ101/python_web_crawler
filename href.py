# import requests
# from bs4 import BeautifulSoup
# import os,re
from  utils import download_html, load_url
# pip install bs4 lxml


def parse(html_filepath):
    soup = load_url(html_filepath)
    post_list = soup.find_all("div", class_="item-body flex xx flex1 jsb")
    for post in post_list:
        link = post.find_all("h2")[0].find_all("a")[0]
        print(link.text.strip())
        print(link["href"])
        download_html(link["href"],'download')

def main():
    # 下载报考指南的网页
    url = "https://zkaoy.com/sions/exam"
    url = "https://zkaoy.com/new"
    filepath = download_html(url)
    parse(filepath)
    

if __name__ == '__main__':
    main()

