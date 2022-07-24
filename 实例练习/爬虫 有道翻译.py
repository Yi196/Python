import urllib.request
import urllib.parse
import json

content=input('请输入要翻译的类容:')
url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'    #此处将translate_o?改为translate?避开反爬虫机制
head={}                                                                     #用于隐藏访问设备信息（Python 3.9）
head['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54'
data={}
data['i']=content
data['from']='AUTO'
data['to']='AUTO'
data['smartresult']='dict'
data['client']='fanyideskweb'
data['salt']='16175317070829'
data['sign']= 'c11ab29bb226ce5ca8b49335819557a2'
data['lts'] ='1617531707082'
data['bv']= 'a70166da0759fd61f4c3fd22f18d04e3'
data['doctype']= 'json'                #此处说明返回的内容为json 格式
data['version']= '2.1'
data['keyfrom']= 'fanyi.web'
data['action']='FY_BY_CLICKBUTTION'
data=urllib.parse.urlencode(data).encode('utf-8')   #将data改为能够输入urlopen的格式

seq=urllib.request.Request(url=url,data=data,headers=head,method='POST')    #method 默认就是”POST“方式
#或者使用seq.addheader（key,value）在seq生成后添加headers=的内容
answer=urllib.request.urlopen(seq)

html=answer.read().decode('utf-8')  #返回json格式字符串
html=json.loads(html)               #将json格式字符串改为字典
#print(html)
a1=html['translateResult'][0][0]['tgt']
print(f'翻译结果为:{a1}')





'''
因为有道的反爬虫机制是根据翻译内容生成不同的'salt'、'sign'参数，顾可调用以下方法生成相应参数   不能用了已经
import random
import hashlib
url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
u = 'fanyideskweb'
d = content
f = str(int(time.time()*1000) + random.randint(1,10))
c = 'rY0D^0\'nM0}g5Mm1z%1G4'
 sign = hashlib.md5((u + d + f + c).encode('utf-8')).hexdigest()
data['salt'] = f
data['sign'] = sign


'''