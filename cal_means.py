# coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import get_list_from_path
from detect_peaks import detect_peaks  # detect_peaks返回的是索引值
from Tkinter import *
import tkFileDialog
import tkMessageBox
import os
import shutil


def ask_dir():
    filepath = tkFileDialog.askdirectory()  # 调用filedialog模块的askdirectory()函数去打开文件夹
    if filepath.strip():  # 如果字符串不为空
        chose_entry.delete(0, END)  # 清空entry里面的内容
        chose_entry.insert(0, filepath)  # 将选择好的路径加入到entry里面


def ask_make_path():
    filepath = tkFileDialog.askdirectory()  # 调用filedialog模块的askdirectory()函数去打开文件夹
    if filepath.strip():
        make_entry.delete(0, END)  # 清空entry里面的内容
        make_entry.insert(0, filepath)  # 将选择好的路径加入到entry里面


def make():
    all_s_line = []
    s_line_total2 = []
    line_num = 0
    c = 0
    folder_path = chose_entry.get()
    folder_path.replace('\\', '/')
    if folder_path[-1] != "/":
        folder_path += "/"  # 输入的路径如果没有\的话，加上\
    folder_path = folder_path.decode()  # 将path解码成unicode
    all_file_path = get_list_from_path.get_all_file_path(folder_path)  # 获取所有文件的路径
#    all_file_path = all_file_path.decode()  # 将all_file_path解码
    means_file_path = make_entry.get()
    means_file_path.replace('\\', '/')
    if means_file_path[-1] != '/':  # 有'/'与没有'/'的两种情况
        means_file_path += '/11means.txt'
    elif means_file_path[-1] == '/':  # 再判断一下结尾是否有'/'
            means_file_path += '11means.txt'
    means_file_path = means_file_path.decode()  # 将means_file_path解码
    if means_file_path in all_file_path:
        tkMessageBox.showwarning("注意", "11means.txt已在该split目录下存在，\n要重新生成请先将此文件删除。")
        return None
    for path in all_file_path:  # 逐个文件打开
        file = open(path)
        s_line = []
        x_axis = []
#        s_line_del = []
        for line in file:  # 逐行读取
            (x, y) = line.split()  # 将同一行根据空格分割开x,y
            x1 = float(x)
            if 453.00 < x1 < 3260.00:
                s_line.append(float(y))  # 合成一条线
                x_axis.append(float(x))
#        s_line_del = [s_del for s_del in s_line if s_del < 453.00 or s_del > 3260.00]
#        for s_del2 in s_line_del:
#            s_line.remove(s_del2)
        all_s_line.append(s_line)  # 将一条线加入“所有图谱”的list中
        file.close()

    s_line_total = all_s_line[0]  # 先将第一条线赋值给s_line_total
    del all_s_line[0]
    for line in all_s_line:  # 将逐条线读出来，即line
        line_num += 1  # 累加计算有多少条线
#        if line != all_s_line[0]:  # 如果是第一条线，就不向s_line_total赋值了，因为前面已经赋了
#            s_line_total = [x+y for x, y in zip(s_line_total, line)]  # 一句实现了以下for的功能，将line加入s_line_total中
        s_line_total = map(lambda xx: xx[0]+xx[1], zip(s_line_total, line))
#        print(s_line_total[178])
#        s_line_total = s_line_total2
#        s_line_total2 = []

#for x,y in zip(s_line,s_line2):
#    s_line_total.append(x+y)
    s_line_mean = [s/(line_num+1) for s in s_line_total]  # 将s_line_total除以线数目
    means_file = open(means_file_path, 'w')  # 'w'代表可以写，注意文件不可以生成在先前读取的目录下
    for a in x_axis:
        b = s_line_mean[c]
        means_file.write("%f %f\n" % (a, b))
        c += 1
    means_file.close()
    if os.path.exists(means_file_path):
        tkMessageBox.showinfo("已完成", "已完成")


def ask_distinguish_folder():
    filepath = tkFileDialog.askdirectory()  # 调用filedialog模块的askdirectory()函数去打开文件夹
    if filepath.strip():  # 如果字符串不为空
        chose_distinguish_entry.delete(0, END)  # 清空chose_distinguish_entry里面的内容
        chose_distinguish_entry.insert(0, filepath)  # 将选择好的路径加入到chose_distinguish_entry里面


def make_division():
    name_del = []
    distinguish_path = chose_distinguish_entry.get()  # 从chose_distinguish_entry获取路径
    distinguish_path.replace('\\', '/')  # 替换字符
    if distinguish_path[-1] != '/':  # 加上'/'
        distinguish_path += '/'
    distinguish_path_yanghe = distinguish_path + '氧合'  # 氧合文件夹路径
    distinguish_path_tuoyang = distinguish_path + '脱氧'
    distinguish_path_del = distinguish_path + '删除'
    distinguish_path = distinguish_path.decode()
    distinguish_path_yanghe = distinguish_path_yanghe.decode()  # 解码
    distinguish_path_tuoyang = distinguish_path_tuoyang.decode()
    distinguish_path_del = distinguish_path_del.decode()

    if not os.path.exists(distinguish_path_yanghe):  # 判断氧合
        os.makedirs(distinguish_path_yanghe)  # 建立氧合文件夹
    if not os.path.exists(distinguish_path_tuoyang):  # 判断脱氧
        os.makedirs(distinguish_path_tuoyang)
    if not os.path.exists(distinguish_path_del):  # 判断脱氧
        os.makedirs(distinguish_path_del)

    all_file_path = get_list_from_path.get_all_file_path(distinguish_path)  # 获取所有文件的路径
    for path in all_file_path:
        file = open(path)
        s_line = []
        x_axis = []
        s_peaks = []
        for line in file:  # 逐行读取
            (x, y) = line.split()
            s_line.append(float(y))  # 合成一条线
            x_axis.append(float(x))  # 组成x坐标
        file.close()
        peaks = [x_axis[ind] for ind in detect_peaks(s_line, show=False)]  # detect_peaks返回的是索引值
        s_peaks = [peak for peak in peaks if 1624.00 < peak < 1643.00]  # 查找峰值范围
        if max([s_line[ind] for ind in detect_peaks(s_line, show=False)[19:-20:1]]) > 250:
            if s_peaks:
                shutil.move(path, distinguish_path_yanghe)
            else:
                shutil.move(path, distinguish_path_tuoyang)
        else:
            shutil.move(path, distinguish_path_del)
            name_del.append(os.path.basename(path))
    if name_del:
        tkMessageBox.showinfo('以下文件而被移动至“删除”', '小于200的文件： %d' % name_del)


app = Tk()
app.title("均值计算")

Label(app, text="要区分的文件夹").grid(row=0, column=0)
chose_distinguish_entry = Entry(app, width=40)
chose_distinguish_entry.grid(row=0, column=2)
Button(app, text="..", command=ask_distinguish_folder, width=2, padx=2).grid(row=0, column=1)
Button(app, text="开始区分", command=make_division, width=7).grid(row=0, column=3)

Label(app, text="要平均的文件夹").grid(row=1, column=0)
chose_entry = Entry(app, width=40)
chose_entry.grid(row=1, column=2)
Button(app, text="..", command=ask_dir, width=2, padx=2).grid(row=1, column=1)

Label(app, text="存放平均文件").grid(row=2, column=0)
make_entry = Entry(app, width=40)
make_entry.grid(row=2, column=2)
make_entry.insert(0, "D:/")
Button(app, text="..", command=ask_make_path, width=2, padx=2).grid(row=2, column=1)
Button(app, text="生成", command=make, width=7).grid(row=3, column=3)
app.mainloop()