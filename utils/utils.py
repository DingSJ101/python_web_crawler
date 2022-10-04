from tkinter.ttk import Separator
from fake_useragent import UserAgent
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import os,re,json
from urllib.parse import quote,unquote
import hashlib
import imghdr

def request_header(random = False):
    """获取请求头

    Args:   
        random (bool, optional): 是否使用随机请求头. Defaults to False.

    Returns:
        dict : headers {'User-Agent':str}
    """
    if random:
        user_agent = UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
    else:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    headers = {
        # 'User-Agent':UserAgent().Chrome #谷歌浏览器
        'User-Agent': user_agent
    }
    return headers


def download_url(url,filename="tmp.txt",dirname='download',random=True,skip=True):
    """download file by url, param random and filename is contradict

    Args:
        url (str): url
        filename (str, optional): filename to be stored. Defaults to "tmp.txt".
        dirname (str, optional): dirname to be stored. Defaults to 'download'.
        random (bool, optional): if use md5 of the file to be the new filename. Defaults to True.
        skip (bool, optional): if skip download already exists file. Defaults to True.

    Returns:
        _type_: _description_
    """
    resp = requests.get(url,headers=request_header(),timeout=5)
    if not resp.ok:
        return None
    resp = resp.content
    if random:
        filetype = ''
        if re.search('^\S*\.(doc\S+|pdf|txt|xls|gif|png|jpg|jpeg|webp|svg|psd|bmp|tif)$',url):
            filetype='.'+url.split('.')[-1]
        filename = hashlib.md5(resp).hexdigest()+filetype
    dirpath = os.path.join(os.getcwd(),dirname)
    filepath = os.path.join(dirpath,filename)
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    # print(resp.url)
    if not random and skip and os.path.exists(filepath):
        print('%s ( already existed )'%url)
    else:
        with open(filepath, mode="wb") as f:
            f.write(resp)
    return filepath

def is_picture(obj):
    """判断obj对象是否为图片

    Args:
        obj (str): str类型的url

    Returns:
        bool:  
    """
    if isinstance(obj,str):
        flag = (re.match('http',obj) != None)
        if re.search("\.(gif|png|jpg|jpeg|webp|svg|psd|bmp|tif)",obj)!=None:
            return True
        elif flag:
            obj = download_url(obj,dirname='tmp',skip=False)
        filetype = None
        if os.path.exists(obj):
            # data = open(obj, "rb").read(32)
            # if data[6:10] in (b'JFIF', b'Exif'):
            #     filetype = 'jpeg'
            # elif data.startswith(b'\211PNG\r\n\032\n'):
            #     filetype = 'png'
            # elif data[:6] in (b'GIF87a', b'GIF89a'):
            #     filetype = 'gif'
            # elif data[:2] in (b'MM', b'II'):
            #     filetype = 'tiff'
            # elif data.startswith(b'\001\332'):
            #     filetype = 'rgb'
            # elif len(data) >= 3 and data[0] == ord(b'P') and data[1] in b'14' and data[2] in b' \t\n\r':
            #     filetype = 'pbm'
            # elif len(data) >= 3 and data[0] == ord(b'P') and data[1] in b'25' and data[2] in b' \t\n\r':
            #     filetype = 'pgm'
            # elif len(data) >= 3 and data[0] == ord(b'P') and data[1] in b'36' and data[2] in b' \t\n\r':
            #     filetype = 'ppm'
            # elif data.startswith(b'\x59\xA6\x6A\x95'):
            #     filetype = 'rast'
            # elif data.startswith(b'#define '):
            #     filetype = 'xbm'
            # elif data.startswith(b'BM'):
            #     filetype = 'bmp'
            # elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
            #     filetype = 'webp'
            # elif data.startswith(b'\x76\x2f\x31\x01'):
            #     filetype = 'exr'
            filetype=imghdr.what(obj)
            if flag:
                os.remove(obj)
        return filetype!=None
            

def load_url(url:str,headers=request_header(),**kwargs):
    """
    if url indicate a html page, return requests.get.text\n
        acquiescently use get() ;\n
        use post() if defined 'json' or 'data' as params\n
    if url indicate local file , f.read()
    """
    if re.match('http',url):
        if 'data' in kwargs or 'json' in kwargs:
            resp = requests.post(url,headers=headers, **kwargs)
        # if 'params' in kwargs:
        #     resp = requests.get(url,headers=headers, **kwargs)
        else:
            resp = requests.get(url,headers=headers, **kwargs)
        resp.encoding = 'utf-8'
        return resp.text
    with open(url, "r", encoding='utf-8') as f:
        html_content = f.read()
        # soup = BeautifulSoup(html_content,features="lxml")
        return html_content

def load_json(url:str):
    return json.loads(load_url(url))

def download_html(url:str,dirname='download',filename=''):
    """
    download html and save as dirname/filename \n
    default:
      dirname :  peer directory 'download'
      filename : use title of the html (in title widget) as title.html
    return : filepath
    """
    resp = ""
    try:
        resp = requests.get(url,headers=request_header())
        if resp.status_code != 200:
            return "None"
        resp.encoding = 'utf-8'
    except RequestException as e:
        return e
    
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

def download_picture(url:str,dirname='download',random=True,filename='',skip = True):
    """
    download picture and save as dirname/filename \n if defined random=True,the param filename will abolish
    default:
      dirname :  peer directory 'download'
      filename : use title of the html (in title widget) as title.html
    params:
        skip : False , dont download existed picture
        random : True , use md5 to generate filename
    """
    if not is_picture(url):
        return None
    path = download_url(url,filename,dirname,random,skip)
    filetype=imghdr.what(path)
    if random and filetype!=path.split('.')[-1]:
        ori_path = path
        path = ori_path+'.'+filetype
        os.rename(ori_path,path)
    return path

def make_soup(html,parse='lxml'):
    return BeautifulSoup(html,parse)

def encode_url(url,encoding='utf-8'):
    return quote(url,encoding)
def decode_url(url,encoding='utf-8'):
    return unquote(url,encoding)


## mysql
# 导入PyMySQL库
import pymysql
# 导入数据库的配置信息
from .setting import DB_CONFIG,MYSQL_DB_URL

class MysqlUtil:
    def __init__(self,database=''):
        # 读取配置文件，初始化pymysql数据库连接
        config = DB_CONFIG.copy()
        self.charset = config.pop('charset')
        self.dbname = config.pop('database')
        if database != '':
            self.dbname = database
        
        self.db = pymysql.connect(**config)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
        # 检查数据库是否存在，并自动创建
        if self.get_fetchone("show databases like '{}'".format(self.dbname)):
            self.db = pymysql.connect(**config,charset=self.charset,database=self.dbname)
        else:
            try:
                self.sql_execute("CREATE DATABASE `{}` CHARACTER SET 'utf8mb4';".format(self.dbname))
                self.db = pymysql.connect(**config,charset=self.charset,database=self.dbname)
            except:
                print("error occur when create database {}".format(self.dbname))
        # 创建数据库游标  返回字典类型的数据
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)
            

    # 获取单条数据
    def get_fetchone(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    # 获取多条数据
    def get_fetchall(self, sql,count=-1):
        """执行sql语句，返回前count项结果

        Args:
            sql (str): sql语句
            count (int, optional): 返回前count项，-1表示全部. Defaults to -1.

        Returns:    
            List: 
        """
        self.cursor.execute(sql)
        if count<=0:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchmany(count)

    # 执行更新类sql
    def sql_execute(self, sql):
        try:
            # db对象和指针对象同时存在
            if self.db and self.cursor:
                self.cursor.execute(sql)
                # 提交执行sql到数据库，完成insert或者update相关命令操作，非查询时使用
                self.db.commit()
                print("执行%s成功!"%(sql))
        except Exception as e:
            # 出现异常时，数据库回滚
            self.db.rollback()
            return False

    # 关闭对象，staticmethod静态方法，可以直接使用类名.静态方法
    @staticmethod
    def close(self):
        # 关闭游标对象
        print("close()")
        if self.cursor is not None:
            self.cursor.close()
        # 关闭数据库对象
        if self.db is not None:
            self.db.close()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata
class mysqlengine:
    def __init__(self):
        # 使用pymysql驱动连接到mysql
        # self.engine = create_engine(MYSQL_DB_URL,echo=True)
        self.engine = create_engine(MYSQL_DB_URL)
        self.create_database()
    
    def create_database(self):
        Base.metadata.create_all(self.engine)
    def drop_database(self):
        Base.metadata.drop_all(self.engine)
    def init_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()
        
        




