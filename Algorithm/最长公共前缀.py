'''
依次遍历字符串数组中的每个字符串，对于每个遍历到的字符串，更新最长公共前缀，当遍历完所有的字符串以后，即可得到字符串数组中的最长公共前缀。
'''

def longestCommonPrefix(strs: list) -> str:
    def _temp(str1, str2):
        prefix = ''
        if len(str1) > len(str2):
            str1, str2 = str2, str1
        for idx, i in enumerate(str1):
            if str2[idx] != i:
                return prefix
            prefix += i
        return prefix

    prefix = strs[0]
    for i in strs:
        prefix = _temp(prefix, i)
        if prefix == '':
            return prefix
    return prefix

if __name__ == '__main__':
    print(longestCommonPrefix(["flower","flow","flight"]))