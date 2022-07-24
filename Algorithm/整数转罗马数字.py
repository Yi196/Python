

def intToRoman(num: int) -> str:
    lst = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
    number = ''
    count = 0
    while True:
        idx = num % 10
        num = num // 10
        temp = lst[idx]
        if count == 0:
            temp = temp
        elif count == 1:
            temp = temp.replace('X', 'C')
            temp = temp.replace('I', 'X')
            temp = temp.replace('V', 'L')
        elif count == 2:
            temp = temp.replace('X', 'M')
            temp = temp.replace('I', 'C')
            temp = temp.replace('V', 'D')
        else:
            temp = 'M' * (idx * (10**(count-3)))
        number = temp + number
        count += 1
        if num == 0:
            break
    return number

if __name__ == '__main__':
    print(intToRoman(19940))