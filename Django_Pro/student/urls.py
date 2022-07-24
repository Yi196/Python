from django.urls import path, re_path
from . import views

urlpatterns=[
    re_path(r'^teacher/', views.show_teacher),
    re_path(r'del_1/', views.del_1),
    re_path(r'del_2/(\w+)/', views.del_2),
    re_path(r'edit_1/', views.edit_1),
    re_path(r'edit_2/(\w+)/', views.Edit_2.as_view()),  # 类 根据不同的提交方式执行类中不同的方法
    re_path(r'add_1/', views.add_1),
    re_path(r'add_2/', views.Add_2.as_view()),
]
