import zipfile
import os


def zip_file(source_dir, zip_path):
    """zip file"""
    zipf = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        if not dirnames and not filenames:  # 空文件夹也保留
            filenames = ['']
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()


def unzip_file(file_name):
    """unzip file"""
    zip_file = zipfile.ZipFile(file_name)
    save_dir = os.path.split(file_name)[0]
    for names in zip_file.namelist():
        zip_file.extract(names, save_dir)
    zip_file.close()

if __name__ == '__main__':
    zip_file('../logs', './001.zip')
    unzip_file('./001.zip')
