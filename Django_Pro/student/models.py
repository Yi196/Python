from django.db import models

# Create your models here.
class Teacher (models.Model):
    id=models.CharField(primary_key=True,max_length=20,verbose_name='教师编号')
    name=models.CharField(max_length=40,verbose_name='姓名')

    class Meta:
        db_table='teacher'
        verbose_name='教师'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name       #重写__str__方法，使print（类对象）返回书名  此处为在admin站点中显示的索引名

class Class(models.Model):
    id=models.CharField(primary_key=True, max_length=20, verbose_name='教室编号')
    title=models.CharField(max_length=20,verbose_name='班级名称')

    class Meta:
        db_table='class'
        verbose_name='班级'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title    #重写__str__方法，使print（类对象）返回书名  此处为在admin站点中显示的索引名

class Student(models.Model):
    id=models.CharField(primary_key=True,max_length=20,verbose_name='学号')
    name=models.CharField(max_length=40,verbose_name='姓名')
    class_id=models.ForeignKey(Class,on_delete=models.SET_NULL,null=True,verbose_name='班级')

    class Meta:
        db_table='student'
        verbose_name='学生'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name    #重写__str__方法，使print（类对象）返回书名  此处为在admin站点中显示的索引名

class Class_T(models.Model):
    class_id= models.ForeignKey(Class,on_delete=models.CASCADE)
    teacher_id =models.ForeignKey(Teacher,on_delete=models.CASCADE)

    class Meta:
        db_table='class_t'
        verbose_name = '班级-老师'
        verbose_name_plural = verbose_name