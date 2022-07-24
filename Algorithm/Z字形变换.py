"""
将一个给定字符串 s 根据给定的行数 numRows ，以从上往下、从左到右进行 Z 字形排列。
之后，你的输出需要从左往右逐行读取，产生出一个新的字符串。
"""

def z_change(s:str, num_rows:int)->str:
    if num_rows==1:
        return s
    num_str = min(len(s), num_rows)
    row = 0
    lst_row = [''] * num_str
    bool_row = False
    for c in s:
        lst_row[row] += c
        if row==0 or row==num_str-1:
            bool_row = not bool_row
        row = row + (1 if bool_row else -1)

    s1 = ''
    for i in lst_row:
        s1 += i
    return s1

if __name__ == '__main__':
    s = "abcdedcbabcdedcba"
    num = 5
    print(z_change(s,num))