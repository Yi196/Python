from xlutils import copy
import xlrd
import traceback
import time
import os
import random

def write_excel(chicun,path,banci, day, no):
    try:
        # print('chicun',chicun.shape)
        info = ""
        excel_path =path
        info = "1"

        #Linux上判断Excel文件是否已打开
        file_name = os.path.basename(path)
        file_name_1 = '.~lock.' + file_name + '#'
        is_opened_path = os.path.join(os.path.dirname(path), file_name_1)
        if os.path.exists(is_opened_path):
            time.sleep(2)


        try:
            home_path = os.environ['HOME']
            copy_dir = os.path.join(home_path, 'xls_copy')
            if not os.path.exists(copy_dir):
                os.mkdir(copy_dir)
            if not os.path.exists(path):
                copy_path = os.path.join(copy_dir, file_name)
                os.system(f'cp {copy_path} {excel_path}')
        except:
            pass


        workxls = xlrd.open_workbook(path)
        wbook = copy.copy(workxls)
        w_sheet = wbook.get_sheet(0)  # 索引sheet表
        worksheet = workxls.sheet_by_name("Sheet1")
        row = worksheet.nrows

        # print(row)
        col = 0
        ret_dict ={
            "0":row,
            "1":info
        }

        # print("chicun",chicun[0][0][1])

        element = banci + '-' + day + '-' + no
        chicun = chicun[0]
        chicun.insert(0,element)

        for i in chicun:
            try:
                i =float(i)
            except:
                i =str(i)
            w_sheet.write(row,col, i )
            col+=1
        wbook.save(excel_path)

        try:
            if random.randint(1, 20) == 1:
                copy_path = os.path.join(copy_dir, file_name)
                os.system(f'cp {excel_path} {copy_path}')
        except:
            pass

        return ret_dict

    except Exception as e:
        traceback.print_exc()
        dict = {
            "0":-1,
            "1":"error",
        }
        return dict


if __name__ == "__main__":
    write_excel([[12,12,12]], r'/home/pc/Desktop/800_335_1R.xls', 'A', '12','133')
