'''
有一个整数数组nums，和一个查询数组requests，其中requests[i] = [starti, endi]。
第i个查询求nums[starti] + nums[starti + 1] + ... + nums[endi - 1] + nums[endi]的结果，starti 和endi数组索引都是从0开始的。
你可以任意排列 nums中的数字，请你返回所有查询结果之和的最大值。
由答案可能会很大，请你将它对109 + 7取余后返回。
'''

'''
根据查询数组requests计算得到数组nums的每个下标位置被查询的次数，应满足数组nums中的越大的数字被查询的次数越多，因此可以使用贪心算法求解
暴力的做法是遍历查询数组中的每个查询范围，对于每个查询范围，将其中的每个下标位置的被查询的次数加1。显然，暴力的做法时间复杂度太高
优化的做法是维护一个差分数组，对于每个查询范围只在其开始和结束位置进行记录，
例如查询范围是[start,end]，则只需要将start处的被查询的次数加 1，将end+1处的被查询的次数减1即可（如果end+1超出数组下标范围则不需要进行减1的操作）
然后对于被查询的次数的差分数组计算前缀和，即可得到数组nums的每个下标位置被查询的次数
'''
def maxSumRangeQuery(nums: list, requests: list) -> int:
    size = len(nums)
    n = 10 ** 9 + 7
    count = [0] * size
    for start, end in requests:
        count[start] += 1
        if end + 1 < size:
            count[end + 1] -= 1

    for i in range(1, size):
        count[i] += count[i - 1]

    nums.sort(reverse=True)
    count.sort(reverse=True)
    s = 0
    for x, y in zip(nums, count):
        s += x * y
        if y == 0:
            break
    return s % n

if __name__ == '__main__':
    print(maxSumRangeQuery([1,2,3,4,5], [[1,3],[0,1]]))  # 19