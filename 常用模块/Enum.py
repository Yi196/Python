from enum import Enum

# 自定义枚举类型继承Enum,避免成员被重复声明 或被外部修改
# 枚举类不能被实例化
class DEFECTS(Enum):
    LIANGPIN = 0
    MOZHOU = 1
    MAOSI = 2
    QUELIAO = 3
    YASHANG = 4
    YIJIAO = 5
    ZANGWU = 6
    PIANXIN = 7
    NOPET = 8
    HUANGJIAODAI = 9
    CHICUN = 10
    KONGLIAO = 11
    DUKONG = 12

print(DEFECTS.YASHANG)
print(DEFECTS.YASHANG.name)
print(DEFECTS.YASHANG.value)

DEFECTS.YASHANG.label = '压伤'