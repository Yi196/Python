import urllib.request
import random

url='http://www.whatismyip.com.tw'    #该网站会返回访问者的ip
iplist=['178.115.243.26:8080','94.189.133.93:8080']

proxy_support=urllib.request.ProxyHandler({'http':random.choice(iplist)})  #设置代理ip
opener=urllib.request.build_opener(proxy_support)             #创建一个自制的opener

opener.addheaders={('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54')}  #隐藏设备信息

#urllib.request.install_opener(opener)  安装一个自制的opener 以后在调用 .urlopen()时，会自动调用这个自制的opener

response=opener.open(url) #调用创建好的自制opener
html=response.read().decode('utf-8')
print(html)
