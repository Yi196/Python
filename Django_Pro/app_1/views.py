from django.shortcuts import render,redirect    #rediect 跳转  render 渲染
from django.http import HttpResponse
from django.forms import Form,fields    #Form 表单验证
from django.forms import widgets
from django.views import View
from .models import *  #python 3.6之后版本导入模块models前加 . 引用当前目录下的models
from django.db.models import *     #导入F两属性比较  Q逻辑或  Sum求和 Avg求平均。。。。

# Create your views here.
def index(request):
    v=request.session.get('user')                  #session 用于验证登录信息
    if v:
        return render(request, 'app_1/hello.html')         #视图函数的返回值必须为一个响应对象
    else:
        return redirect('/app_1/login/')

def cal(request):
    value_a=123
    value_b=321
    result=value_a+value_b
    Cal.objects.create(value_a=value_a,value_b=value_b,result=result)       #pycharm 无法连接到objects.create也没事，程序可正常执行
    context={'value_a': value_a,'value_b': value_b,'result': result}
    return render(request,'app_1/cal.html',context=context)   #context=字典 指定传入html的参数注意变量名要一致   'app_1/cal.html'为文件地址 已声明在templates文件下

#Form表单验证  用于验证提交的数据是否满足条件
#保留上次输入内容
class Lin(Form):   #定义用于验证的表单类
    user=fields.CharField(max_length=40,min_length=3,  #定义验证条件
                          label='用户名',       #自动生成form表单 widget=widgets.Select 选择生成的标签类型 默认为<input/> ,
                          label_suffix=':',    #initial='213' 默认值  help_text='帮助信息'
                          error_messages={'max_length':'用户名不能超过40位','min_length':'用户名不能少于3位'},  #错误时的返回信息 因为自动生成html 会在前端验证
                          widget=widgets.TextInput(attrs={'class':'form-control'}),)  ##在生成的标签中加关键字  此处为指定 类名为 a1
    pwd=fields.CharField(max_length=20, min_length=3,required=True,  #required=True 不能为空
                         label='密码',
                         label_suffix=':',
                         widget=widgets.PasswordInput(attrs={'class':'form-control'}),)  #设为密码类型  widget=widgets.Select 选择生成的标签类型 默认为<input/> ,

class Login(View):
    def get(self,request):
        obj=Lin()   #用于自动生成Form表单  保留上次输入内容
        return render(request,'app_1/login.html',{'obj':obj})
    def post(self,request):
        obj=Lin(request.POST)  #进行Form表单验证  满足为True  此处因为自动生成html标签  会在前端验证 满足条件才能提交
        if obj.is_valid():
            user_1=User.objects.filter(**obj.cleaned_data).first()   #obj.cleaned_data 获取验证后的字典
            if user_1:
                request.session['user']=user_1.user   #设置session 用于登录检测
                return redirect('/app_1/index/')   #redirect 方法用于跳转  '/'表示跳转回首页
            else:
                obj = Lin(request.POST)
                return render(request,'app_1/login.html',context={'obj':obj,'meg':'用户或密码错误，请重新登录！'})
        else:
            return render(request, 'app_1/login.html', {'obj': obj})

def logout(request):
    request.session.clear()
    return redirect('/app_1/login/')

def shouye(request):
    return render(request, 'shouye.html')