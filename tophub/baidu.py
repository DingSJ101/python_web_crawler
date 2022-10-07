# from utils import utils
import random
import sys,os,re
from time import sleep
sys.path.append(os.path.realpath('.'))
# sys.path.append('.')
from utils.utils import load_url,download_html,make_soup,decode_url,download_picture,load_json
from utils.utils import MysqlUtil,mysqlengine
from models import HotList,Base
from datetime import datetime
engine = mysqlengine(Base)
engine.create_database()
session = engine.init_session()

"""
方法一 : https://www.baidu.com页面在浏览器上和下载后读取的文件div的属性内容不一致,硬解html
方法二 : 
"""

def fun1():
    """
    方案一：硬解百度首页html，只显示部分
    """
    url = "https://www.baidu.com/"
    html = load_url(url)
    # path = download_html(url,filename = 'baidu')
    # html = load_url(path)
    soup = make_soup(html,"html.parser")

    res = soup.find_all('div',class_ = 'wrapper_new',id = 'wrapper')[0]
    res = res.find('div',id='head')
    res = res.find('div',id = 's-hotsearch-wrapper')
    res = res.find('ul',id="hotsearch-content-wrapper")
    res = res.find_all('li')
    for li in res:
        index = li.find('span',class_="title-content-index").text 
        text = li.find('span',class_="title-content-title").string
        ori_url = li.find('a').get('href').encode('utf8')
        url = decode_url(ori_url)
        print('-'*10,index,'-'*10)
        print(text,url)
        
def fun2():
    """
    方案二：硬解百度热榜html，
    """
    url = "https://top.baidu.com/board?tab=realtime"
    html = load_url(url)
    # path = download_html(url,filename = 'baidu_top')
    # html = load_url(path)
    soup = make_soup(html,"html.parser")
    res = soup.find('main')
    res = res.find('div',style="margin-bottom:20px")
    res = res.find_all('div',class_ = "category-wrap_iQLoo horizontal_1eKyQ")
    for div in res :
        hot_data = div.find('div',class_="hot-index_1Bl1a")
        title = div.find('div',class_="c-single-text-ellipsis")
        paper_url = title.parent.get('href')
        desc = div.select('div.hot-desc_1m_jR.large_nSuFU')[0]
        index = div.find('div',class_ = "index_1Ew5p")
        paper_img = index.parent.find("img",src=re.compile("http"))
        pic_url = paper_img.get('src').replace('amp;','')
        print(hot_data.text)
        print(title.text)
        print(paper_url)
        print(desc.text.split('查看更多')[0])
        print(index.text)
        path = download_picture(pic_url,'pic')
        print(path)
        # break
def fun3():
    """
    方案三：使用API接口
    """
    url = "https://top.baidu.com/api/board" # 热搜榜主页，热搜十条+小说/电影/电视剧/汽车/游戏榜
    url2 = "https://top.baidu.com/api/board?platform=wise&tab=realtime" # 热搜页，热搜30条,tab:realtime/novel/movie/teleplay/car/game/phrase
    url = 'https://top.baidu.com/api/board?platform=pc&tab=movie&tag={"category":"动画","country":"中国大陆"}' # tag参数见Url2中tag字段中typeName和content
    url = url2
    # url = "https://top.baidu.com/api/board?platform=wise&tab=novel"
    data = load_json(url)['data']
    cards = data['cards']
    tag = data['tag']
    # db = MysqlUtil("crawl")

    for card in cards:
        component, content, more, moreAppUrl, moreUrl, text, topContent, typeName, updateTime = card.values()
        # component = card['component']
        # content = card['content']
        # res = card.keys()
        # print(res)
        # print("-"*15,text,"-"*20)
        if component == 'hotList': # 热搜
            content.append(topContent[0])
            for item in content:
                appUrl = item.get("appUrl","") # 搜索链接
                desc = item.get("desc","")
                hotChange = item.get("hotChange","") # 热度变化 same/up/down
                hotScore = int(item.get("hotScore","")) # 热度值
                # hotTag = item.get("hotTag","") # 热度状态 热/爆
                # hotTagImg = item.get("hotTagImg","")
                img = item.get("img","")
                index = item.get("index",-1) # 排序
                query = item.get("query","")
                rawUrl = item.get("rawUrl","") # appUrl 简短版
                # url = item.get("url","") # 同appUrl
                show = item.get("show",[]) # 其他榜单的子项目的描述
                try:
                    show_json = {i.split('：')[0]:i.split('：')[1] for i in list}
                except:
                    show_json = {}
                url = item.get("url","") # 同appUrl
                word = item.get("word","") # 展示文字
                # print(index,"(热度%s)"%hotScore ,word)
                # if not db.get_fetchone("select * from hotList")
                res = session.query(HotList).filter_by(word=word).order_by(HotList.time.desc()).first()
                if res:
                    if res.index==index:
                        # print('no operate')
                        continue
                    else:
                        # print(datetime.now(),'update',word)
                        pass
                else:
                    # print(datetime.now(),'add',word)
                    pass
                record = HotList(
                            time=datetime.now(),
                            type = component,
                            desc = desc,
                            hotscore = hotScore,
                            img = img,
                            rawurl = rawUrl,
                            word = word,
                            index = index,
                            query = query,
                            show = show_json
                            )
                session.add(record)
                session.commit()
                
        else:
            for item in content:
                appUrl = item.get("appUrl","")
                desc = item.get("desc","")
                hotChange = item.get("hotChange","")
                hotScore = item.get("hotScore","")
                img = item.get("img","")
                index = item.get("index","")
                query = item.get("query","")
                rawUrl = item.get("rawUrl","")
                show = item.get("show",[])
                # url = item.get("url","") # 同appUrl
                word = item.get("word","")
                print("{3:<3}{0: <15}{1:^20}热度：{2}".format(word,show[0],hotScore,index))
                print(show,type(show))
            # print(card.keys())

def create_table():
    sql = """
        CREATE TABLE `crawl`.`hotList`  (
            `time` datetime NOT NULL,
            `type` varchar(255) NULL,
            `desc` varchar(255) NULL,
            `hotchange` varchar(255) NULL,
            `hotscore` int NULL,
            `img` varchar(255) NULL,
            `query` varchar(255) NULL,
            `rawurl` varchar(255) NULL,
            `show` varchar(255) NULL,
            `word` varchar(255) NULL,
            PRIMARY KEY (`time`)
        );
    """
    db = MysqlUtil("crawl")
    if db.sql_execute(sql):
        print("success create db ")
    else:
        print("cant create ")
        

if __name__ == '__main__':
    
    # fun1()
    # fun2()
    fun3()
    ## test MysqlUtil and create_table()
    # create_table()
    # mysql = MysqlUtil("crawl")
    # res = mysql.get_fetchall("show tables ;")
    # print(res)
    # res = mysql.sql_execute("create table baidu ")
    # print(res)
    # sql = """
    #     select * from `hotList` where `hotList`.`word` = %s;
    # """%('酒店民宿“逢假必涨”合法吗？')
    # print(sql)
    # res=  mysql.get_fetchall(sql)
    # print(res)
    ## 
    cnt = 4000
    while(cnt):
        print(datetime.now(),cnt)
        fun3()
        time = random.randint(30,60)
        sleep(time)
        cnt=cnt-1
    
    
    
