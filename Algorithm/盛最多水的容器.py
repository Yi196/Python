'''
给你 n 个非负整数 a1，a2，...，an，每个数代表坐标中的一个点(i,ai) 。
在坐标内画 n 条垂直线，垂直线 i的两个端点分别为(i,ai) 和 (i, 0) 。
找出其中的两条线，使得它们与x轴共同构成的容器可以容纳最多的水。
'''


# 利用双指针 每次向中间移动值较小的指针
def calculate_area(lst):
    size = len(lst)
    max_area = 0
    point_1 = 0
    point_2 = size-1
    while point_2 > point_1:
        area = (point_2-point_1) * min(lst[point_1], lst[point_2])
        if area > max_area:
            max_area = area
        if lst[point_1] < lst[point_2]:
            point_1 += 1
        else:
            point_2 -= 1
    return max_area

if __name__ == '__main__':
    print(calculate_area([321,432,4565,765132,21]))