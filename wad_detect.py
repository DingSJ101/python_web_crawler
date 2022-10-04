from cgi import print_arguments
from importlib import import_module


# 分析网页的框架
import wad.detection
det = wad.detection.Detector()
url  = "http://www.baidu.com"
url = "https://starry101.top"
url = "https://s.weibo.com/top/summary?cate=realtimehot"
url = "https://top.baidu.com/board"
print(det.detect(url))