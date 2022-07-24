"""
如果字符串中不含有任何 'aaa'，'bbb' 或 'ccc' 这样的字符串作为子串，那么该字符串就是一个「快乐字符串」。
给你三个整数 a，b ，c，请你返回 任意一个 满足下列全部条件的字符串 s：
s 是一个尽可能长的快乐字符串。
s 中 最多 有a 个字母 'a'、b 个字母 'b'、c 个字母 'c' 。
s 中只含有 'a'、'b' 、'c' 三种字母。
如果不存在这样的字符串 s ，请返回一个空字符串 ""。
"""

"""
思路：每次从a，b，c中个数最多的字母tmp，该tmp（比如a）能否放入结果res，分三种情况：
1、tmp能放入res，则放入（res倒数第1、第2个字母不同时为tmp）
2、tmp不能放入res，并且没有其他字符可选（比如b、c个数为0），则结束
3、tmp不能放入res，选择个数次多的元素放入（比如b，一定能放入）
"""

def solution(a: int, b: int, c: int) -> str:
    lst = [['a',a], ['b',b], ['c',c]]
    re = ''

    while True:
        lst.sort(key= lambda x:x[1], reverse=True)

        if len(re)>=2 and re[-1]==re[-2] and re[-1]==lst[0][0]:  # 不能放入
            if lst[1][1]==0:
                break
            re += lst[1][0]
            lst[1][1] -= 1
        else:
            if lst[0][1]==0:
                break
            re += lst[0][0]
            lst[0][1] -= 1

    return re


if __name__ == '__main__':
    re = solution(8,2,9)
    print(re)