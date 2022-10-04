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
#提供假的请求头
from fake_useragent import UserAgent  
headers= {'User-Agent':str(UserAgent().random)}

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

#### 格式控制参数

`{<index>:<填充><对齐><宽度><,><.精度><类型>}.format(<variable>)`

- `<填充>` 填充多余位置使用的字符，默认空格
- `<对齐>` 文本所处位置`<`左对齐、`^`居中、`>`右对齐，默认左对齐
- `<宽度>` 变量的输出宽度
- `<,> `使用千位分隔符
- `<.精度>` 小数精度
- `<类型>` 数据的输出了类型：`b`二进制，`c`字符，`d`整形，`e`科学计数法，`f` 浮点型，`o`八进制，`x`十六进制，`X`大写十六进制，`%`百分比

### f-string

```python 
a = 1
b = 2.33
str = f'{a}\n{b:.1f}'
```

## User-Agent
```python
from fake_useragent import UserAgent
headers = {
        # 'User-Agent': UserAgent().random #常见浏览器的请求头伪装（如：火狐,谷歌）
        'User-Agent': UserAgent().Chrome #谷歌浏览器
    }
random_list = []
chrome_list = []
for i in range(20000):
  random_list.append(UserAgent().random)
  chrome_list.append(UserAgent().Chrome)
```

## BeautifulSoup4

基本操作对象为`tag`，使用`bs.find()`或`bs.find_all()`方法、以及`bs.title`、`bs.div`等方法获得的都是该对象，对象的属性包括`tag.name`和`tag.attrs`

```python 
html =  open('./aa.html', 'rb').read()
bs = BeautifulSoup(html,"lxml") 
print(bs.title) # 获取title标签的名称
print(bs.title.name) # 获取title的name
print(bs.title.string) # 获取head标签的所有内容
print(bs.head)
print(bs.div) # 获取第一个div标签中的所有内容
print(bs.div["id"]) # 获取第一个div标签的id的值
print(bs.a)
print(bs.find_all("a")) # 获取所有的a标签
print(bs.find(id="u1")) # 获取id="u1"
 
for item in bs.find_all("a"):
  print(item.get("href")) # 获取所有的a标签，并遍历打印a标签中的href的值
 
for item in bs.find_all("a"):
  print(item.get_text())
```
## lxml

### 输入输出

```python
from lxml import etree 
text =  '<root>data</root>'
html  = etree.fromstring(text) # fromstring方法
html1 = etree.XML(text) # XML方法，与fromstring方法基本一样
html2 = etree.HTML(text) # HTML方法，如果没有<html>和<body>标签，会自动补上
new_text = etree.tostring(html) # 输出XML
```

#### 节点操作

```python
from lxml import etree 
text =  '<root><ch1/><ch2/><ch3/></root>'
html  = etree.fromstring(text) # fromstring方法
print(html.tag) # 返回对象的当前节点名称,root
print(html[0].tag) # 子节点列表，ch1
print(html[0].getparent().tag) # 访问父节点, root
```

#### 节点属性

属性以key-value的方式存储

```python
from lxml import etree 
text =  '<root cla1="val1" cla2="val2"></root>'
html  = etree.fromstring(text) # fromstring方法
print(html.get("cla1")) # 获取"cla1"属性值
print(html.keys()) # ['cla1', 'cla2']
print(html.items()) # [('cla1', 'val1'), ('cla2', 'val2')]
print(html.attrib) #拿到所有的属性及属性值存于字典中 , {'cla1': 'val1', 'cla2': 'val2'}
```

#### 搜索节点

findall()：返回所有匹配的元素，返回列表
find()：返回匹配到的第一个元素

参数为xpath语句

```python
print(root.find('.b')) # 查找第一个b标签
print(root.findall('.//a[@x]') # 根据属性查询
```



### xpath

#### 寻找节点

| 语法               | 含义                                                |
| ------------------ | --------------------------------------------------- |
| nodename(节点名字) | 直接根据写的节点名字查找节点,如：div                |
| //                 | 在当前节点下的子孙节点中寻找,如：//div，查找所有div |
| /                  | 在当前节点下的子节点中寻找,如：/div                 |
| .                  | 代表当前节点（可省略不写），如：./div               |
| ..                 | 当前节点的父节点，如：../div                        |

```python
result = html.xpath('//div') #使用xpath语法,在子孙节点中寻找div标签
result = html.xpath('/html/body/div') #html标签内的body标签的子节点的div
```

#### 获取属性

| 方法   | 作用                 |
| ------ | -------------------- |
| @      | 获取属性或者筛选属性 |
| text() | 获取文本             |

```python
from lxml import etree
text = '''
<div class="hello" name="test">
	<p>/div/p</p>
</div>
<div class="hello test hi">line1
	<div>line2
		<div>/div/div</div>line3
	</div>line4
	line5
	<div>line6
		<div>/div/div</div>line7
	</div>line8
</div>
<div class="button">
	<div class="menu">
		<input name="btn" type="button" value="按钮" />
	<div>
</div>
'''
html = etree.HTML(text)

content = html.xpath('//div/p/text()')    #获取第一个div中的p标签中的文本
print(content)  # ['/div/p']
 
content_two = html.xpath('//div[position() = 2]/text()') #获取拥有第二个div中的文本
print(content_two)  # ['line1\n\t', 'line4\n\tline5\n\t', 'line6\n\t\t', 'line7\n\t', 'line8\n']
 
content_three = html.xpath('//div[position() = 2]//text()')
print(content_three)  # ['line1\n\t', 'line2\n\t\t', '/div/div', 'line3\n\t', 'line4\n\tline5\n\t', 'line6\n\t\t', '/div/div', 'line7\n\t', 'line8\n']
 
first_div_class = html.xpath('//div[@class="hello"]/@name')#获取第一个div的name属性
print(first_div_class)  # ['test']
 
input_tag_class = html.xpath('//input/@name')#获取input标签的name值
print(input_tag_class) # ['btn']
```



#### 属性筛选

当我们使用筛选时，筛选的方法都是包含在`[]`中的。

| 方法名\符号 | 作用                                                         |
| ----------- | ------------------------------------------------------------ |
| @           | 获取属性或者筛选属性,如：@class                              |
| contains    | 判断属性中是否含有某个值（用于多值判断），如：contains(@class,'hello') |

```python
from lxml import etree
html = etree.fromstring("<div class="hello test hi">test</div>")
hello_tag = html.xpath('//div[@class="hello"]')  #筛选出class="hello"的div标签
input_tag = html.xpath('//input[@name="btn"]') #找出具有name="btn"的input标签
hello_tags = html.xpath('//div[contains(@class,"hello")]') #筛选出具有class="hello"的div标签
```

#### **按序筛选**

有时候我们会有这样的需求，我们爬取的内容是一个table标签（表格标签），或者一个ul（标签），了解过html的应该都知道这样的标签，内部还有很多标签，比如table标签里就有tr、td等，ul里面就有li标签等。对于这样的标签，我们有时候需要选择第一个或者最后一个或者前几个等。这样的方式我们也可以实现。

| 方法                | 作用                       |
| ------------------- | -------------------------- |
| last()              | 获取最后一个标签           |
| 1                   | 获取第一个标签             |
| position() <op> num | 筛选多个标签（具体见实例） |

```python
from lxml import etree
text = '''
<ul>
    <li>1</li>
    <li>2</li>
    <li>3</li>
    <li>4</li>
    <li>5</li>
    <li>6</li>
    <li>7</li>
</ul>     
'''
html = etree.HTML(text)
first_tag = html.xpath('//li[1]') #获取第一个li标签
last_tag = html.xpath('//li[last()]') #获取最后一个li标签
li_tags = html.xpath('//li[position() < 3]') #获取前2个标签
print(html.xpath('//li[position() < 3]') ==  html.xpath('//li[position() = 1 or position() = 2]'))
for tag in li_tags: print(etree.tostring(tag))

```

