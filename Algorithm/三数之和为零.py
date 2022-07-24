'''
给你一个包含 n 个整数的数组nums，判断nums中是否存在三个元素 a，b，c，使得a+b+c=0？请你找出所有和为0且不重复的三元组。
'''

'''
不重复：第二重循环枚举到的元素不小于当前第一重循环枚举到的元素；第三重循环枚举到的元素不小于当前第二重循环枚举到的元素。
我们可以从小到大枚举b，同时从大到小枚举c，即第二重循环和第三重循环实际上是并列的关系。
有了这样的发现，我们就可以保持第二重循环不变，而将第三重循环变成一个从数组最右端开始向左移动的指针，
'''


def three_sum(nums:list)->list:
    n = len(nums)
    nums.sort()
    ans = []

    # 枚举 a
    for first in range(n-2):
        # 需要和上一次枚举的数不相同
        if first > 0 and nums[first] == nums[first - 1]:
            continue
        # c 对应的指针初始指向数组的最右端
        third = n - 1
        target = -nums[first]
        # 枚举 b
        for second in range(first + 1, n-1):
            # 需要和上一次枚举的数不相同
            if second > first + 1 and nums[second] == nums[second - 1]:
                continue
            # 需要保证 b 的指针在 c 的指针的左侧
            while second < third and nums[second] + nums[third] > target:
                third -= 1
            # 如果指针重合，随着 b 后续的增加
            # 就不会有满足 a+b+c=0 并且 b<c 的 c 了，可以退出循环
            if second == third:
                break
            if nums[second] + nums[third] == target:
                ans.append([nums[first], nums[second], nums[third]])

    return ans


'''
三数之和为目标值target
排序加双个指针
'''
def three_sum_closest(nums:list, target:int)->int:
    nums.sort()
    n = len(nums)
    best = None

    for first in range(n-2):
        # 保证每次枚举与上次不相等
        if first>0 and nums[first]==nums[first-1]:
            continue
        # 使用双指针枚举b,c
        second, third = first+1, n-1
        while second < third:
            s = nums[first] + nums[second] + nums[third]
            # 如果和为target直接返回答案
            if s == target:
                return target
            if best==None or abs(s-target) < abs(best-target):
                best = s
            if s > target:
                # 如果和大于target，移动c对应的指针
                third -= 1
                # 移动到下一个不相等的元素
                while second < third and nums[third] == nums[third+1]:
                    third -= 1
            else:
                # 如果和小于target，移动b对应的指针
                second += 1
                # 移动到下一个不相等的元素
                while second < third and nums[second] == nums[second-1]:
                    second += 1
    return best



if __name__ == '__main__':
    print(three_sum([-1,0,1,2,-1,-4]))
    print(three_sum_closest([1,2,5,10,11],12))