# coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
from decimal import Decimal
from detect_peaks import detect_peaks
from find_close_simple import find_close
from Tkinter import *
import Tkinter
import tkMessageBox
import tkFileDialog
import glob
import tablib
from get_list_from_path import get_all_file_path


class spectrum(dict):
    def __init__(self, f_path):
        dict.__init__({})
        self.x_axis = []
        self.y_axis = []
        self.locs = []
        self.peaks = []
        try:
            self.__get_s(f_path)
        except:
            pass
        self.__locs()
        self.__peaks()
        self.concentration = re.search(r'(?P<concentration2>\b\d\.\d{1,3}\b|\b\d{3,4}\b|\b\d{2}\.\d{0,2}\b|\bck\b)', f_path.split('/')[-1]).group('concentration2')

    def __get_s(self, f_path):
        self.f = open(f_path)
        for self.line in self.f:
            (self.x, self.y) = self.line.split()
            self.x = '{:.2f}'.format(Decimal(self.x))
            self[self.x] = self.y
            self.x_axis.append(self.x)
            self.y_axis.append(self.y)
        self.f.close()

    def __peaks(self):
        self.peaks = [self.y_axis[self.ind] for self.ind in detect_peaks(self.y_axis, show=False)]

    def __locs(self):
        self.locs = [self.x_axis[self.ind] for self.ind in detect_peaks(self.y_axis, show=False)]


def update_speclist(event):
    # Rewrite the Menubutton associated with the Optionmenu.
    try:
        specs = spectrum(ck_var.get()).locs
        menu = toption['menu']
        menu.delete(0, 'end')
        for spec in specs:
            menu.add_command(label=spec, command=Tkinter._setit(target, spec))
    except:
        pass


def ask_ck():
    filepath = tkFileDialog.askopenfilename()  # 调用filedialog模块的askdirectory()函数去打开文件夹
    if filepath.strip():  # 如果字符串不为空
        chose_entry.delete(0, END)  # 清空entry里面的内容
        chose_entry.insert(0, filepath)  # 将选择好的路径加入到entry里面
    update_speclist('mean_nothing')


def ask_folder():
    filepath = tkFileDialog.askdirectory()  # 调用filedialog模块的askdirectory()函数去打开文件夹
    if filepath:
        folder_entry.delete(0, END)  # 清空entry里面的内容
        folder_entry.insert(0, filepath)  # 将选择好的路径加入到entry里面


def add_peak():
    peak_entry.insert(END, target.get()+';')


def ask_make_path():
    filepath = tkFileDialog.askdirectory()  # 调用filedialog模块的askdirectory()函数去打开文件夹
    if filepath:
        make_entry.delete(0, END)  # 清空entry里面的内容
        make_entry.insert(0, filepath)  # 将选择好的路径加入到entry里面


def make():
    concentration_path_dict = {}
    compared_path_list2 = []

    ck = spectrum(chose_entry.get())
    file_path = folder_entry.get()
    if file_path[-1] != '/' and file_path[-1] != '\\':
        file_path += '/'

    compared_path_list = glob.glob(file_path+'*.txt')
    compared_path_list = [path.decode('utf-8').replace('\\', '/') for path in compared_path_list]

    if chose_entry.get() in compared_path_list:
        compared_path_list.remove(chose_entry.get())

    for each_compared_path in compared_path_list:
        each_compared_path_last = each_compared_path.split('/')[-1]
        concentration_path_dict[re.search(r'(?P<concentration2>\b\d\.\d{1,3}\b|\b\d{3,4}\b|\b\d{2}\.\d{0,2}\b)', each_compared_path_last).group('concentration2')] = each_compared_path

    for path_dict in sorted(concentration_path_dict, key=lambda v: [int(i) for i in v.rstrip('@').split('.')]):
        compared_path_list2.append(concentration_path_dict[path_dict])
    standard_peaks_locs = peak_entry.get().split(';')  # 下面可以加上排序
    if standard_peaks_locs[-1] == '':
        standard_peaks_locs.remove(standard_peaks_locs[-1])

    standard_peaks_locs = sorted(standard_peaks_locs, key=lambda v: [int(i) for i in v.rstrip('@').split('.')], reverse=True)

    make_path = make_entry.get()
    if make_path[-1] != '/' and make_path[-1] != '\\':
        make_path += '/'

    ck_list = []
    ck_list.append('ck')

    for loc in standard_peaks_locs:
        ck_list.append('')
        ck_list.append(ck[loc])
        ck_list.append('')

    all_fin = []
    all_fin.append(ck_list)

    for path in compared_path_list2:
        compared_peaks_locs_float = []
        spec = spectrum(path)
        current_list = []
        current_list.append(spec.concentration)
        for loc in standard_peaks_locs:
            if loc in spec.locs:
                current_list.append('')
                current_list.append(spec[loc])
                percentage_shift = str((float(spec[loc])-float(ck[loc]))/float(ck[loc])*100)
                percentage_shift = '{:.2f}'.format(Decimal(percentage_shift))+'%'
                current_list.append(percentage_shift)
            else:
                standard_loc_float = float(loc)
                for compared_loc_str in spec.locs:
                    compared_peaks_locs_float.append(float(compared_loc_str))
                close_peak_loc = find_close(standard_loc_float, compared_peaks_locs_float)
                current_list.append(close_peak_loc)
                current_list.append(spec['{:.2f}'.format(Decimal(close_peak_loc))])
                close_peak_loc = '{:.2f}'.format(Decimal(close_peak_loc))
                percentage_shift = str((float(spec[close_peak_loc])-float(ck[loc]))/float(ck[loc])*100)
                percentage_shift = '{:.2f}'.format(Decimal(percentage_shift))+'%'
                current_list.append(percentage_shift)

        all_fin.append(current_list)

    standard_peaks_locs_insert = standard_peaks_locs
    standard_peaks_locs_insert.insert(0, '浓度')
    standard_peaks_locs_insert = (sum([[i, ''] for i in standard_peaks_locs_insert], [])[:-1])
    standard_peaks_locs_insert2 = []
    i = 2
    for insert in standard_peaks_locs_insert:
        standard_peaks_locs_insert2.append(insert)
        if i != 2 and i%2 == 0:
            standard_peaks_locs_insert2.append('比率')
        i = i+1

    data = tablib.Dataset(*all_fin, headers=standard_peaks_locs_insert2, title='sheet1')

    try:
        with open(make_path+name_entry.get()+'.xls', 'ab') as fin_file:
            fin_file.write(data.xls)
        tkMessageBox.showinfo("已完成", "已完成")
    except:
        tkMessageBox.showwarning("Failed", "未能生成文件")


def show_help(event):
    tkMessageBox.showinfo('使用帮助',
                          '1：此帮助尚未完成\
                          \n2：\
                          \n3：')


app = Tk()
app.title("拉曼光谱对比")

AGEOPT = ['1602.51', '1631.42']

ck_var = StringVar()
chose_entry = Entry(app, width=80, textvariable=ck_var)
chose_entry.grid(row=0, column=0)
chose_entry.insert(0, "C:/Users/mygre_000/Desktop/4d/4d-ck-混合-平均-标-B.txt")
chose_entry.bind('<Leave>', update_speclist)
Button(app, text="选择ck文件", command=ask_ck).grid(row=0, column=1, sticky=W)

folder_entry = Entry(app, width=80)
folder_entry.grid(row=1, column=0)
folder_entry.insert(0, "C:/Users/mygre_000/Desktop/4d/")
Button(app, text="选择整个文件夹", command=ask_folder).grid(row=1, column=1, sticky=W)

make_entry = Entry(app, width=80)
make_entry.grid(row=2, column=0)
make_entry.insert(0, "D:/")
Button(app, text="选择存放位置", command=ask_make_path).grid(row=2, column=1, sticky=W)

Label(app, text="——生成的文件名").grid(row=3, column=1, sticky=W)
name_entry = Entry(app, width=35)
name_entry.grid(row=3, column=0, sticky=E)
name_entry.insert(0, "table")

Label(app, text="——波长").grid(row=4, column=1, sticky=W)
peak_entry = Entry(app, width=80)
peak_entry.grid(row=4, column=0)
peak_entry.insert(0, '1631.42;1602.54;')
Button(app, text="+", command=add_peak,  width=6).grid(row=5, column=0, sticky=E)

target = Tkinter.StringVar(value='波长')
toption = Tkinter.OptionMenu(app, target, *AGEOPT)
toption.grid(row=5, column=1, sticky=W)

Button(app, text="对比谱线", command=make).grid(row=6, column=0)

Lb1 = Listbox(app, height=1, bg='Gray', selectbackground='Gray',
              highlightcolor='black', font="NewTimes 8 italic")  #  'Gray', 'Red', 'Blue', 'Purple', 'Yellow','green',"white",'black'
Lb1.insert(1, 'Created by Xunda Ye')
Lb1.grid(row=6, column=1, sticky=W)
Lb1.bind('<Double-1>', show_help)


app.mainloop()
