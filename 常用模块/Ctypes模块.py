import ctypes

value = 'hello world'  # 定义一个字符串变量
address = id(value)  # 获取value的地址，赋给address
get_value = ctypes.cast(address, ctypes.py_object).value  # 读取地址中的变量
print(get_value)