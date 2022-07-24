"""pro1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path, re_path
from app_1.views import shouye

urlpatterns = [
    path('admin/', admin.site.urls),
    #把子路由信息添加到总路由中
    re_path(r'^app_1/', include('app_1.urls')),         #使用include来将子应用app_1里的全部路由包含进工程路由中
    # r'^app_1/' 决定了app_1子应用的所有路由都已/app_1/开头，如我们刚定义的视图index，其最终的完整访问路径为/app_1/index/
    re_path(r'^student/', include('student.urls')),

    re_path(r'^$', shouye),
]
