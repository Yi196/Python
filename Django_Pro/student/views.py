from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import Form,fields
from django.forms import widgets
from django.views import View
from .models import *
from django.db.models import *

# Create your views here.
def show_teacher(request):
    lst_1=Teacher.objects.all()
    # .raw(SQL语句)可直接输入SQL语句
    # lst_2=Student.objects.raw('select student.id,student.name,class.title from student left JOin class on student.class_id_id=class.id')
    lst_2=Student.objects.all().values('id','name', 'class_id__title')  # 注意values生成字典列表 value_list生成元组列表  注意键为‘class_id__title'
    return render(request, 'student/001.html', context={'lst_1': lst_1, 'lst_2': lst_2})

def edit_1(request):
    if request.method=='GET':
        id=request.GET.get('id')
        name = request.GET.get('name')
        return render(request,'student/修改.html',{'id':id,'name':name})
    else:
        id=request.POST.get('id')
        name=request.POST.get('name')
        Teacher.objects.filter(id=id).update(name=name)
        return redirect('/student/teacher/')


class StudentForm(Form):
    id= fields.CharField(min_length=2,max_length=20,widget=widgets.TextInput(attrs={'class':'a1'}))  # 在生成的标签中加关键字  此处为指定 类名为 a1
    name=fields.CharField(min_length=2,max_length=40,)
    class_id_id=fields.CharField(
        widget=widgets.Select( choices=Class.objects.values_list('id','title'),attrs={'class':'a1'}))  # 取班级列表的id 和title 元组列表 用于生成选项

'''
CBV加装饰器
from django.views.decorators.csrf import csrf_exempt  #CSRF验证 设置局部禁用
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt,name='dispatch')   '''
class Edit_2(View):                          # 根据不同的提交方法  执行不同函数 通过反射实现，性能优于if else 判断
    def dispatch(self,request,*args,**kwargs):
        # print('001')  类似装饰器 在调用函数get post。。前 后 执行一些操作
        obj=super(Edit_2,self).dispatch(request,*args,**kwargs)
        return obj

    def get(self,request,id):
        lst_1=Student.objects.filter(id=id).values('id','name','class_id_id').first()  #取字典
        obj=StudentForm(lst_1)    # 往Form表单中传字典不需要加 **
        return render(request,'student/修改02.html',{'id':id,'obj':obj})
    def post(self,request,id):
        obj=StudentForm(request.POST)  # request.POST就是一个字典
        if obj.is_valid():
            Student.objects.filter(id=id).update(**obj.cleaned_data)    # id 也是obj.cleaned_data['id'] 注意obj.cleaned_data字典只在obj.is_valid()之后成立
            return redirect('/student/teacher/')
        else:
            return render(request, 'student/修改02.html', {'meg': '请输入正确的格式', 'obj': obj})

def del_1(request):
    id=request.GET.get('id')
    Teacher.objects.filter(id=id).delete()
    return redirect('/student/teacher/')

def del_2(request,id):
    Student.objects.filter(id=id).delete()
    return redirect('/student/teacher/')

def add_1(request):
    if request.method=='GET':
        return render(request,'student/添加.html')
    else:
        id=request.POST.get('id')
        name=request.POST.get('name')
        if Teacher.objects.filter(id=id):
            return render(request,'student/添加.html',{'meg':'该教师已存在，请重新输入'})
        Teacher.objects.create(id=id,name=name)
        return redirect('/student/teacher/')

class Add_2(View):
    def get(self,request):
        obj=StudentForm()
        return render(request, 'student/添加02.html', {'obj':obj})
    def post(self,request):
        obj=StudentForm(request.POST)
        if obj.is_valid():
            if Student.objects.filter(id=obj.cleaned_data['id']):
                return render(request, 'student/添加02.html', {'meg': '该学生已存在，请重新输入', 'obj':obj})
            Student.objects.create(**obj.cleaned_data)    # 传字典要在前面加上 **
            return redirect('/student/teacher/')
        else:
            return render(request, 'student/添加02.html', {'meg': '请输入正确的格式', 'obj': obj})