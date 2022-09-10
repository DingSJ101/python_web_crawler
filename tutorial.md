# python包
## requests
在浏览器开发者工具中我们能看到上述url的Headers信息，一般在获取url资源时都会先分析对应的请求头来写代码。

1. General（基本信息），Request Method: GET得知是get请求，所以调用requests.get()方法。
2. Responsese Headers（响应头信息），Content-Type: application/json; charset=utf-8代表返回的内容是json格式，所以解析数据用r.encoding = 'utf-8'编码，data = r.json()获取json信息。
3. Request Headers（请求头信息），这里主要的是Cookie/User-Agent/token等。Cookie一般存储浏览器认证信息，比如用户标识等，一般相同的cookie代表是同一用户访问，但是也有将认证信息用token的传递的。

自定义请求头
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0'
    }
```
请求网页
```python
url = 'https://example.net'
data = {'a':123,'b':456}
params = {'a':123,'b':456}
files = {'file': open('report.xls', 'rb')}
proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}
response = requests.get(url,headers=headers,params=params)
response = requests.post(url,headers=headers,data=data) 
response = requests.post(url,headers=headers,files=files)
response = requests.get(url,proxies=proxies)
```
页面内容`response.text`  
请求地址`response.url` 


关闭请求`response.close()`
## re
正则表达式,匹配资源路径
```re
t = '<img src="(.*?)" alt="(.*?)" width="160" height="120">'
result = re.findall(t, response.text)
```
## 格式化输出
### 占位符
```python
a = 'world'
b = "!"
str = 'Hello %s %s'%(a,b)
```
| 占位符 | 替换内容     | 备注 | 
| ------ | ------------ | ---- |
| %d     | 整数         |  %3d |
| %f     | 浮点数       | %.2f  |
| %s     | 字符串       |   |
| %x     | 十六进制整数 |   |

### format()
```python 
str = 'Hello {} {} '.format('world',"！")
str = "{0} \n{1:.2f}".format(123,2.333)
```

### f-string 
```python 
a = 1
b = 2.33
str = f'{a}\n{b:.1f}'
```