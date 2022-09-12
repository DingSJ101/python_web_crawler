import requests
from lxml import etree
from utils import download_html

class baidu_sosuo:
    def __init__(self):
        self.url = 'https://www.starry101.top/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

    def one_page(self):
        res = requests.get(self.url, headers=self.headers)
        html = etree.HTML(res.text)
        title = html.xpath("//div[@id='content_left']//h3/a")
        for i in title:
            print(i.xpath('string(.)'))
        self.next_page(html)

    def next_page(self, html):
        next_page = html.xpath("//div[contains(text(),'Course_')]")
        print(next_page[0].xpath('string()'))
        # if next_page is not None:
        #     next_page = 'https://www.baidu.com' + ''.join(next_page)
        #     res = requests.get(next_page, headers=self.headers)
        #     htmls = etree.HTML(res.text)
        #     title = htmls.xpath(''.join("//div[@id='content_left']//h3/a"))
        #     for i in title:
        #         print(i.xpath('string(.)'))


if __name__ == "__main__":
    bd = baidu_sosuo()
    bd.one_page()
    url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=44004473_102_oem_dg&wd=VSC%20%20python%20%20%E5%88%B6%E8%A1%A8%E7%AC%A6%20%E7%A9%BA%E6%A0%BC&oq=lxml%2520%25E8%258A%2582%25E7%2582%25B9%25E6%2596%2587%25E6%259C%25AC&rsv_pq=c6827dfc00084e6e&rsv_t=d041HUVG21qoqGURyWRE44g6b0nzhNBaWshYrajV5YWqZch6lIUeG%2FLPH3GSzw%2Fdwoi0sXnpLlV5ng&rqlang=cn&rsv_enter=1&rsv_dl=tb&rsv_sug3=43&rsv_sug1=31&rsv_sug7=100&rsv_sug2=0&rsv_btype=t&inputT=10023&rsv_sug4=10501"
    # download_html(url,filename='baidu')
