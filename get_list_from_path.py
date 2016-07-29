# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os.path


def get_file_list(path):
    fileList = []
    files = os.listdir(path)
    for f in files:
        if(os.path.isfile(path+'/'+f)):
            f = f.decode()
            fileList.append(f)
    return fileList


def get_all_file_path(folder_path):
    all_file_path=[]
    file_list=get_file_list(folder_path)
    for f in file_list:
        all_file_path.append(folder_path+f)
    return all_file_path   # 返回数组，所有文件的完整路径
