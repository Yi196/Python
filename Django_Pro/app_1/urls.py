from django.urls import path, re_path
from . import views

# urlpatterns是被django自动识别的路由列表变量
urlpatterns=[
    # 每个路由信息都需要使用url函数来构造
    # url(路径, 视图)
    re_path(r'^index/', views.index),          # 网址为..../app_1/index
    # 此处r'^index/$'为正则表达式，^表示匹配字符串开头 $表示匹配字符串末尾  /则是浏览器中的文件隔离符
    re_path(r'^cal/', views.cal),
    re_path(r'^login/', views.Login.as_view()),
    re_path(r'^logout/', views.logout),

]