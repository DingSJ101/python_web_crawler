from numpy import rec
from utils.utils import mysqlengine
from tophub.models import HotList
session = mysqlengine().init_session()
res = session.query(HotList).all()
print(res)
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index

'https://m.baidu.com/s?word=%E4%B8%AD%E5%9B%BD%E5%90%AF%E5%8A%A8%E7%AC%AC%E5%9B%9B%E6%89%B9%E9%A2%84%E5%A4%87%E8%88%AA%E5%A4%A9%E5%91%98%E9%80%89%E6%8B%94&sa=fyb_news'
''
'same'
'4974254'
0
'https://fyb-2.cdn.bcebos.com/hotboard_img/f864e1f1e9dd062ade2068bf86f5655a'
'0'
'中国启动第四批预备航天员选拔 https://m.baidu.com/s?word=%E4%B8%AD%E5%9B%BD%E5%90%AF%E5%8A%A8%E7%AC%AC%E5%9B%9B%E6%89%B9%E9%A2%84%E5%A4%87%E8%88%AA%E5%A4%A9%E5%91%98%E9%80%89%E6%8B%94' 
'https://m.baidu.com/s?word=%E4%B8%AD%E5%9B%BD%E5%90%AF%E5%8A%A8%E7%AC%AC%E5%9B%9B%E6%89%B9%E9%A2%84%E5%A4%87%E8%88%AA%E5%A4%A9%E5%91%98%E9%80%89%E6%8B%94&sa=fyb_news'
'中国启动第四批预备航天员选拔'
record = HotList(time = datetime.now(),desc = "据中国载人航天工程办公室消息，为满足载人航天工程后续飞行任务需要，我国第四批预备航天员选拔工作已于近期启动。")
# session.add(record)
session.commit()