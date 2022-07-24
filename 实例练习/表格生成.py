import prettytable as pt
def show_ticket(row_num):
    tb=pt.PrettyTable()                                                #产生一个表格
    tb.field_names=["行号","座位1","座位2","座位3","座位4","座位5"]         #定义表头
    for i in range(row_num):
        lst=[f"第{i+1}行","有座","有座","有座","有座","有座"]
        tb.add_row(lst)                                                #定义行
    print(tb)

def order(row_num,row,column):
    tb=pt.PrettyTable()
    tb.field_names=["行号","座位1","座位2","座位3","座位4","座位5"]
    for item in range(row_num):
        if item+1!=row:
            lst = [f"第{item+1}行", "有座", "有座", "有座", "有座", "有座"]
            tb.add_row(lst)
        else:
            lst = [f"第{item+1}行", "有座", "有座", "有座", "有座", "有座"]
            lst[column]="已售"
            tb.add_row(lst)
    print(tb)

if __name__ == '__main__':
    order(13,10,4)