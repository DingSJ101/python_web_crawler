import requests
url="http://movie.douban.com/j/chart/top_list"
param={
	"type":"24",
	"interval_id":"100:90",
	"action":"",
	"start":0,
	"limit":20,
	} #右键->检查，network，点击Payload即可将参数复制到此处的字典
headers={
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55"
	}
resp=requests.get(url=url,params=param,headers=headers)
print(resp.json())
print(resp.url)
resp.close() #关掉resp
