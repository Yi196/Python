import urllib.request
answer=urllib.request.urlopen('http://placekitten.com/g/500/600')    #返回一个网页对象    （原本该网址直接返回一个图片信息）
html=answer.read()                                                   #read()从对象中获取二进制文件
#html=html.decode('utf-8')                                #解码
with open('Cat.png','wb')as file:
    file.write(html)


