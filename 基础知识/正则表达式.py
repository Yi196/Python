import re

a=re.search(r'[a-c]\.\d','woshi.2c.43')       #re.search()找出第一个符合条件的内容
print(a)
print(a.group())
print(a.start())
a=re.findall(r'caa[^_]+','woshicaaasd_sajcaajhsd_sad')    #[^_]表示除下划线外所有字符 +表示重复1到无数次
b=re.findall(r'caa([^_]+)','woshicaaasd_sajcaajhsd_sad')  #当r' () '内有括号时，会返回括号里的内容  当有多个括号时会返回一个元组，在括号内加问号可解除元组(?:   )
print(a,b)

p=r'(?:(?:1[0-9][0-9]\.)|(?:2[0-4][0-9]\.)|(?:25[0-5]\.)|(?:[1-9][0-9]\.)|(?:[0-9]\.)){3}(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])|(?:[1-9][0-9])|(?:[0-9]))'    #ip地址的正则表达式
c=re.findall(p,'asd117.135.250.1sad')
print(c)