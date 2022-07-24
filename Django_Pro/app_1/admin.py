from django.contrib import admin
from .models import *

# Register your models here.
class BookStackedInline(admin.StackedInline):   #StackedInline 用于设置在父级的编辑页面内  可以编辑其关联的子级
    model = HeroInfo  #关联子对象
    extra = 0  # 额外预留新增选项默认为3个

class BookAdmin(admin.ModelAdmin):
    list_per_page = 10  #设置每页显示条数
    list_display = ['btitle','bpub_data','bread','bcomment',]  #显示那些内容
    inlines = [BookStackedInline]        #引入 以便可在父级的编辑页面下直接操作其关联的子级

class HeroAdmin(admin.ModelAdmin):
    list_per_page = 10  #设置每页显示条数
    list_display = ['hname','hgender','hcomment','hbook',] #此处hbook为外键 会显示‘bookinfoobject’ 而在BookInfo的类定义中重写了__str__方法 使‘bookinfoobject’变为书名  注意此处不能跨表
    list_filter = ['hbook','hgender',]                     #过滤器 指定按什么属性过滤
    search_fields = ['hname','hcomment',]                  #搜索框 及搜索范围  注意不能搜索外键‘hbook’ 以及性别在后台数据我0 1输入male查不到
    #fields = ['hname','hgender','hcomment','hbook',]      #设置编辑页面内容  及可编辑的属性
    fieldsets=(
        ('基本',{'fields':('hname','hgender')}),            #设置编辑页面  分为 基本 高级 两部分 与fileds=[] 互斥
        ('高级',{'fields':('hcomment','hbook')}),)

class UserAdmin(admin.ModelAdmin):
    list_per_page = 10  #设置每页显示条数
    list_display = ['user','pwd']  #显示那些内容


admin.site.register(BookInfo,BookAdmin)
admin.site.register(HeroInfo,HeroAdmin)
admin.site.register(User,UserAdmin)