from email import header
from operator import truediv
import time
from unittest import TestProgram
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
from utils.utils import get_page,request_header


def test_proxy(proxy,url = "http://httpbin.org/ip"):
    # url = 'http://api.myip.la/'
    proxies = {
        "http": "http://" + proxy,
        "https": "http://" + proxy,
        # "http": proxy,
        # "https": proxy,
    }
    try:
        resq = requests.get(url,headers=request_header(),proxies=proxies,timeout=1)
        if resq.status_code == 200:
            print("--"*15,resq.json()['origin'],"--"*15)
            print(proxy, '\033[31m可用\033[0m')
        else:
            print(proxy, '不可用')
        resq.close()
    except Exception as e:
        print(proxy,'请求异常')
        print(e)
    

def crawl_daili66(page_count=4):
    """
    获取代理66
    2018.9.2测试可用
    :param page_count: 页码
    :return: 代理
    """
    start_url = 'http://www.66ip.cn/{}.html'
    urls = [start_url.format(page) for page in range(1, page_count + 1)]
    for url in urls:
        print('Crawling: ', url)
        html = get_page(url)
        if html:
            #     yield ':'.join([ip, port])
            page = etree.HTML(html)
            table = page.xpath("//div[@align='center']/table")[0]
            for tr in table[1:]:
                ip = tr[0].text
                ip = tr[0].xpath('string()')
                port = tr[1].text
                # print(ip,port)
                proxy = ip+":"+port
                test_proxy(proxy)

# # def crawl_goubanjia():
#     """
#     获取Goubanjia
#     2018.9.2测试可用
#     :return: 代理
#     """
#     start_url = 'http://www.goubanjia.com'
#     html = get_page(start_url)
#     if html:
#         doc = pq(html)
#         tds = doc('td.ip').items()
#         for td in tds:
#             td.find('p').remove()
#             yield re.sub('\n', '', td.text())

# def crawl_ip181():
    # '''
    # 一个很Low的，只有body的代理网站
    # 2018.9.2测试可用
    # :return: 代理
    # '''
    # start_url = 'http://www.ip181.com/'
    # html = get_page(start_url)
    # # 因为网页里的数据都是放在body中的，我们需要用正则来匹配得到表达式
    # pattern = re.compile(',"port":"(.*?)","ip":"(.*?)"},', re.S)

    # # 用findall来查找相应的匹配结果
    # re_ip_address = re.findall(pattern, html)
    # for address, port in re_ip_address:
    #     result = address + ':' + port
    #     yield result.replace(' ', '')

def crawl_ip3366():
    '''
    获取云代理
    2018.9.2测试可用
    :return: 代理
    '''
    print("Test ip3366")
    for i in range(1, 4):
        start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(i)
        html = get_page(start_url)
        if html:
            page = etree.HTML(html)
            table = page.xpath("//table[contains(@class,'table')]/tbody")
            # print(etree.tostring(table[0]))
            for tr in table[0]:
                id = tr[0].text
                port = tr[1].text
                proxy = id+':'+port
                test_proxy(proxy)

def crawl_ip3366_free():
    '''
    2018.9.2测试可用
    :return: 代理
    '''
    for page in range(1, 4):
        start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
        html = get_page(start_url)
        ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
        # \s * 匹配空格，起到换行作用
        re_ip_address = ip_address.findall(html)
        for address, port in re_ip_address:
            proxy = address + ':' + port
            # yield result.replace(' ', '')
            test_proxy(proxy)

def crawl_kuaidaili():
    '''
    获取快代理
    2018.9.2测试可用
    :return: 代理
    '''
    for i in range(1, 4):
        start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
        html = get_page(start_url)
        if html:
            # ip_address = re.compile('<td data-title="IP">(.*?)</td>')
            # re_ip_address = ip_address.findall(html)
            # port = re.compile('<td data-title="PORT">(.*?)</td>')
            # re_port = port.findall(html)
            # for address, port in zip(re_ip_address, re_port):
            #     address_port = address + ':' + port
            #     yield address_port.replace(' ', '')
            page = etree.HTML(html)
            table = page.xpath("//table[contains(@class,'table')]/tbody")
            # print(etree.tostring(table[0]))
            for tr in table[0]:
                id = tr[0].text
                port = tr[1].text
                proxy = id+':'+port
                test_proxy(proxy)

# def crawl_xicidaili():
    # '''
    # 获取西刺免费代理
    # 2018.9.2测试可用
    # :return:高匿代理
    # '''
    # for i in range(1, 3):
    #     start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #         'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
    #         'Host': 'www.xicidaili.com',
    #         'Referer': 'http://www.xicidaili.com/nn/3',
    #         'Upgrade-Insecure-Requests': '1',
    #     }
    #     html = get_page(start_url, options=headers)
    #     if html:
    #         find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
    #         trs = find_trs.findall(html)
    #         for tr in trs:
    #             find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
    #             re_ip_address = find_ip.findall(tr)
    #             find_port = re.compile('<td>(\d+)</td>')
    #             re_port = find_port.findall(tr)
    #             for address, port in zip(re_ip_address, re_port):
    #                 address_port = address + ':' + port
    #                 yield address_port.replace(' ', '')

# def crawl_iphai():
#     '''
#     获取ip海代理
#     2018.9.2测试可用
#     :return:国内高匿代理
#     '''
#     start_url = 'http://www.iphai.com/free/ng'
#     html = get_page(start_url)
#     if html:
#         find_tr = re.compile('<tr>(.*?)</tr>', re.S)
#         trs = find_tr.findall(html)
#         for s in range(1, len(trs)):
#             find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
#             re_ip_address = find_ip.findall(trs[s])
#             find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
#             re_port = find_port.findall(trs[s])
#             for address, port in zip(re_ip_address, re_port):
#                 address_port = address + ':' + port
#                 yield address_port.replace(' ', '')

def crawl_89ip():
    '''
    获取89代理
    2018.9.2测试可用
    :return: 代理
    '''
    start_url = 'http://www.89ip.cn/'
    html = get_page(start_url)
    if html:
        page = etree.HTML(html)
        table = page.xpath("//table[contains(@class,'layui-table')]/tbody")
        # print(etree.tostring(table[0]))
        for tr in table[0]:
            id = tr[0].text
            port = tr[1].text
            proxy = id+':'+port
            test_proxy(proxy.replace(' ',"").replace('\t',"").replace('\n',""))

def crawl_data5u():
    '''
    获取无忧代理IP
    2018.9.2测试可用
    :return: 高匿代理
    '''
    start_url = 'http://www.data5u.com/free/gngn/index.shtml'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=47AA0C887112A2D83EE040405F837A86',
        'Host': 'www.data5u.com',
        'Referer': 'http://www.data5u.com/free/index.shtml',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36',
    }
    html = get_page(start_url, options=headers)
    if html:
        ip_address = re.compile('<span><li>(\d+\.\d+\.\d+\.\d+)</li>.*?<li class=\"port.*?>(\d+)</li>', re.S)
        re_ip_address = ip_address.findall(html)
        for address, port in re_ip_address:
            result = address + ':' + port
            yield result.replace(' ', '')



if __name__ == "__main__":
    # crawl_daili66()
    # crawl_ip3366()
    # crawl_ip3366_free()
    # crawl_kuaidaili()
    # crawl_89ip()


    # crawl_data5u()
    # 失效代理
    # crawl_iphai()

    # url = "http://myip.ipip.net/"
    url = "http://www.baidu.com"
    # # url = "https://ip.sb/"
    # test_proxy("119.5.224.111","14946",url)
    # test_proxy("127.0.0.1","443",url)
    proxy = "223.96.90.216:8085"
    while 1:
        test_proxy(proxy)
        time.sleep(0.6)
    # resq = requests.get(url,proxies = {"http": "http://117.92.127.231:16924",
    #     "https": "https://117.92.127.231:16924"})
    # resq = requests.get(url)
    # print(resq.status_code)
    # print(resq.text)