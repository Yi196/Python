import os
import sqlite3
import time
from threading import Thread


def test_sqlite():
    '''
    可多链接访问数据库，当某个链接修改数据库时，所有链接都会被阻塞，直至修改完成，等待超时时间默认5秒
    注意多线程使用同一个链接时，链接时要加参数check_same_thread=False， 并且对数据库的访问要加线程锁
    :return:
    '''
    path = r'../logs/img_cache.db'

    # 链接数据库，没有时会创建
    conn = sqlite3.connect(path)
    sql = conn.cursor()

    # 查看数据库中所有表格名称
    sql.execute("SELECT name FROM sqlite_master WHERE type='table' order by name")

    # 没有表格时创建表格
    if 'img_cache' not in [i[0] for i in sql.fetchall()]:
        sql.execute("CREATE TABLE img_cache \
                    (id TEXT PRIMARY KEY NOT NULL, \
                    img_path TEXT NOT NULL, \
                    last_time INT NOT NULL);")

    while True:
        str_time = str(int(time.time()))
        local_time = str(time.strftime('%Y-%m-%d', time.localtime()))
        id = 'qqwe12312'
        img_path = str(f'./img_cache/images/{local_time}/{id}.jpg')
        last_time = str_time
        # 插入数据（若该数据已存在，当插入数据与数据库中现有数据完全一至时不会报错，否则会报主键唯一错误）
        # sql.execute(f"INSERT INTO img_cache (id, img_path, last_time) VALUES ('{id}', '{img_path}', {last_time})", )   # 注意字符串要加引号 '{id}'，整数不用 {last_time}
        # conn.commit()  # 插入后需要提交 可insert 1000条后再提交

        find_id = 'qqwe12312'
        # 查询数据
        cursor = sql.execute(f"SELECT * from img_cache WHERE id = '{find_id}'")
        # print(cursor.fetchone())
        # print(cursor.fetchmany(3))
        # print(cursor.fetchall())
        for i in cursor:
            print(i)
            # time.sleep(1)

        # 更新数据
        update_id = 'qqwe12312'
        update_last_time = str(int(time.time()))
        sql.execute(f"UPDATE img_cache set last_time = {update_last_time} where id = '{update_id}'")
        conn.commit()    # 更新会直接修改数据库，若不提交，其他链接可能会报错 数据库被锁

    conn.close()


# Linux上可配和touch指令修改文件最后访问时间，并用tmpwatch指令删除长期未使用的文件
# os.system('touch file_name')
# os.system('tmpwatch -a 30d ./img_cache ')  # 删除./img_cache下30天未被访问的文件

if __name__ == '__main__':
    t = []
    for _ in range(5):
        t.append(Thread(target=test_sqlite))

    for i in t:
        i.start()

    for i in t:
        i.join()




