
# 利用滑动窗口
def find_max_chstr(string:str)->list:
    temp = ''
    max_chstr = ''
    ret_lst = []
    size = len(string)
    for i in range(size):
        for j in string[i:]:
            if j not in temp:
                temp += j
            else:
                break
        if len(temp) > len(max_chstr):
            max_chstr = temp
            ret_lst = []
            ret_lst.append(temp)
        elif len(temp) == len(max_chstr):
            ret_lst.append(temp)
        temp = ''

    return ret_lst

# 最长回文字串
def find_max_restr(string:str)->list:
    max_restr = ''
    ret_lst = []
    for idx,i in enumerate(string):
        str_t = string[idx:]
        while True:
            idx_1 = str_t.rfind(i)
            str_t = str_t[:idx_1+1]
            if str_t == str_t[::-1]:
                temp = str_t
                break
            else:
                str_t = str_t[:-1]

        if len(temp) > len(max_restr):
            max_restr = temp
            ret_lst = []
            ret_lst.append(temp)
        elif len(temp) == len(max_restr):
            ret_lst.append(temp)

    return ret_lst


if __name__ == '__main__':
    print("最长子串：",find_max_chstr("aabbccdd"))  #['ab', 'bc', 'cd']
    print("最长回文子串：",find_max_restr("aabbccdd"))  # ['aa', 'bb', 'cc', 'dd']
    print("最长回文子串：",find_max_restr("abcdcba1221221")) # ['abcdcba', '1221221']