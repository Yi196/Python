import importlib
import importlib.util
import imp


'''
importlib为imp模块衍生及拓展，它们都可以用于载入模块，并且具备reload的功能，但是在网上查阅大量资料显示最常用的importlib.import_module()只能已相对路径载入模块，
现已找到一种使用importlib库以文件绝对路径载入模块的方法，下面分别对imp载入模块、importlib相对路径载入模块、importlib绝对路径载入模块的使用方法进行示例说明
'''

# 方法一、imp.load_module()
# 先使用imp.find_module()根据文件绝对路径找到需要载入的模块：
fp,path,descrip = imp.find_module('config_user',['/Desktop/Scripts'])
# fp相当于调用open()后返回的文件句柄，path的为文件完整路径：/Desktop/Scripts/config_user.py，descrip为一些描述值，然后调用imp.load_module()载入模块：

module = imp.load_module('config_user', fp,path,descrip)
# 此时模块载入完成，可以通过module.attribute或者module.func()的方式调用模块中的属性和方法，模块使用完毕后需要关闭fp：
if fp:
    fp.close()


# 方法二、importlib.import_module() 主目录都为程序运行时的根目录
# 这种方法只能通过相对路径载入模块，与imp.find_module()的区别是：它无需先调用一个find函数，可以直接一步到位载入模块，缺点是它无法找到当前所在文件夹之外的文件，但是当前文件夹之内所有文件都能载入，无论中间嵌套了多少层，只要把相对路径写正确就行，使用方法为：
module = importlib.import_module('test_dir.test1.test1')

module = importlib.import_module('.test1', package='test_dir/test1')


# 方法三、使用importlib以文件绝对路径载入模块
# 首先使用importlib.util.spec_from_file_location()获取模块的specification信息：
spec = importlib.util.spec_from_file_location('np_test', '/Desktop/Scripts/del_test/test1/test1.py')
# 其中的第一个参数np_test是你对于这个要载入模块的命名，载入的文件为test1.py。
# 然后调用importlib.util.module_from_spec(spec)获取需要导入的模块，最后使用spec.loader.exec_module(foo)进行模块加载。
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

foo.np_test()   # 使用test1.py中的.np_test()函数



