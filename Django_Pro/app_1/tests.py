from django.test import TestCase

# Create your tests here.

#数据库操作
from .models import *
from django.db.models import *     #导入F两属性比较  Q逻辑或  Sum求和 Avg求平均。。。。
#增
BookInfo.objects.create(btitle='天龙八部',bput_date='1986-7-24',bread=112345,bcomment=324)
book1=BookInfo(btitle='西游记',bput_date='1988-1-21',bread=11123345,bcomment=113324)
book1.save()
#含有外键的增
hero1=HeroInfo.objects.create(hname='孙悟空',hbook=book1.id)   #外键hbook要指定被关联对象的主键
hero2=book1.heroinfo_set.create(hname='猪八戒')     #book1.heroinfo_set为book对应的外键
#删
book1.delete()
#改
book1.bread=12332
book1.save()
BookInfo.objects.filter(id=1).update(bread=213234)
#查
BookInfo.objects.get(bput_date__year__gte=1980)  #返回一个类对象  未找到报错
BookInfo.objects.exclude(bread__isnull=True).count()  #计 阅读量 不为空的 数量   exclude()取反
BookInfo.objects.filter(bread__isnull=False).count()  #同上
BookInfo.objects.filter(btitle__contains='游')        #找书名包含 游 的书
BookInfo.objects.filter(id__in=[1,23,4])             #找id 在1，23，4中的书
BookInfo.objects.filter(Q(btitle__startswith='西') | Q(btitle__endswith='记'))  #Q对象 找出以‘西’开头 |(或) 以‘记’结尾的书
BookInfo.objects.filter(bread__gte=F('bcomment')*2)    #F对象 属性间比较  找出阅读数大于等于两倍评论量的书
BookInfo.objects.filter(bread__gt=1000).aggregate(Avg('bcomment'))   #求阅读数大于1000的书的平均评论数
BookInfo.objects.all().order_by('-id')           #按id降序排序
#关联查询
BookInfo.objects.filter(heroinfo__hcomment__contains='能打')   #从HeroInfo中找出hcomment中含有“能打”的对应BookInfo类对象   因为HeroInfo含有外键  小写类名heroinfo__属性名
HeroInfo.objects.filter(hbook__btitle__contains='西')          #找出符合条件（BookInfo中btitle含有“西”字）对应的HeroInfo类对象   hbook为外键
book1.heroinfo_set.all()   #找出book1对应的多个HeroInfo对象
hero1.hbook_bread          #找出hero1的被关联对象的bread属性值
