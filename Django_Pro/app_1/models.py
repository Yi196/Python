from django.db import models

# Create your models here.
class BookInfo(models.Model):
    btitle=models.CharField(max_length=20,verbose_name='名称')   #verbose_name= 指明在admin站点显示的名称 缺省以属性名 btitle代替
    bpub_data=models.DateField(verbose_name='发布日期')
    bread=models.IntegerField(default=0,verbose_name='阅读量')
    bcomment=models.IntegerField(default=0,verbose_name='评论量')
    is_delete=models.BooleanField(default=False,verbose_name='逻辑删除')

    class Meta:
        db_table='tb_books'  #指明数据库表明
        verbose_name='图书'   #指明在admin站点中显示的名称
        verbose_name_plural=verbose_name #指明显示的复数名称
    #books=BookInfoManager() #声明自定义的管理对象
    def __str__(self):
        return self.btitle    #重写__str__方法，使print（类对象）返回书名  及用 书名 替代 'bookinfoobject'

class HeroInfo(models.Model):
    GENDER_CHOICES=(        #选项 性别  自定 用于限制输入类容的范围
        (0,'male'),
        (1,'female')
    )
    hname=models.CharField(max_length=20,verbose_name='姓名')
    hgender=models.SmallIntegerField(choices=GENDER_CHOICES,default=0,verbose_name='性别')   #用choices= 限制输入类容
    hcomment=models.CharField(max_length=200,null=True,verbose_name='描述信息')     #Null=True表示可为空
    hbook=models.ForeignKey(BookInfo,to_field='id', on_delete=models.CASCADE,verbose_name='图书')  #外键 on_delete=models.CASCADE 指定级联删除
    is_delete=models.BooleanField(default=False,verbose_name='逻辑删除')

    class Meta:
        db_table='tb_heros'  #指定数据库表名
        verbose_name='英雄'   #admin站点显示名
        verbose_name_plural=verbose_name  #复数名
    def __str__(self):
        return self.hname
#我们在通过模型类的objects属性提供的方法操作数据库时，即是在使用一个管理器对象objects。当没有为模型类定义管理器时，Django会为每一个模型类生成一个名为objects的管理器，它是models.Manager类的对象
#一旦为模型类指明自定义的过滤器后，Django不再生成默认管理对象objects。
'''定义自定义的管理对象
class BookInfoManager(models.Manager):
    def all(self):                               #重写all（）方法，使调用时返回所有is_delete=False的类对象
        return super().filter(is_delete=False)  '''

class Cal(models.Model):           #在数据库中创建表
    value_a=models.FloatField(max_length=10)
    value_b=models.FloatField(max_length=10)
    result =models.CharField(max_length=20)
    def __str__(self):
        return self.value_a    #重写__str__方法，使print（类对象）返回书名  此处为在admin站点中显示的索引名

class User(models.Model):
    user=models.CharField(primary_key=True, max_length=40,verbose_name='用户名')
    pwd=models.CharField(max_length=20,verbose_name='密码')
    class Meta:
        db_table='user_pwd'
        verbose_name='用户信息'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.user


#数据库操作
#https://blog.csdn.net/yanpenggong/article/details/82316514?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522161893557516780357276769%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=161893557516780357276769&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-82316514.pc_search_result_before_js&utm_term=django+%E6%95%B0%E6%8D%AE%E5%BA%93%E6%93%8D%E4%BD%9C
#注意sqlist只有单线程，故在运行时，要断开与pycharm链接