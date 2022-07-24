import urllib.request
import re

def open_url(url):
    req=urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54')
    page=urllib.request.urlopen(req)
    html=page.read().decode('gbk')
    return html
def get_img(html):
    p=r'<img src="([^"]+\.(?:jpg|gif))'             #搜索jpg和gif两种文件格式 （？:  ）为了避免re.findall（）将结果返回元组
    imglist=re.findall(p,html)
    for each in imglist:
        each=zh(each)
        if each=='':
            continue
        filename='C:\\Users\\YJL\\Desktop\\Python练习\\实例练习\\壁纸\\'+each.split('/')[-1]     #获得文件路径
        #print(each)
        urllib.request.urlretrieve(each,filename,None)           # __.urlretrieve()方法用于下载网页内容，参数以此为：下载地址、保存路径、下载进度（缺省不显示进度）

def zh (a):              #用于将缩略图地址转为原图地址
    b=list(a)
    for _ in range(5):
        b.pop(38)
    for _ in range(10):
        b.pop(-5)
    c=''.join(b)
    if len(c)>60:
        return c
    else:
        return ''

if __name__ == '__main__':
    url='http://www.netbian.com/1920x1080/'       #该网址图片地址需要拼接后得到
    get_img(open_url(url))
#下载的都是网页里的缩略图   观察缩略图和原图网址差异  多一个’small‘，结尾处在.gif前多10个数字