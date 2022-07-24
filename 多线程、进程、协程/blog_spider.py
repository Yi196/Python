from urllib import request, parse

urls =[
    f'https://www.cnblogs.com/#p{page}'
    for page in range(1,51)
]

def craw(url):
    # data = bytes(parse.urlencode({'world':'hello'}), encoding='utf8')  #产生Post请求，默认None为Get请求
    r = request.urlopen(url, data=None)
    print(url,len(r.read()))
    return r.read()



