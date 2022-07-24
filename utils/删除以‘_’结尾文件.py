import os
import os.path

def delete(path):
    for file in os.listdir(path):
        if os.path.splitext(file)[0].endswith('_'):
            os.remove(os.path.join(path,file))



if __name__ == '__main__':
    path = 'C:/Users/dihuge/Desktop/685_huangjiaodai'
    delete(path)