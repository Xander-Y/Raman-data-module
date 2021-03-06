# coding:utf-8

import re
from decimal import Decimal
from detect_peaks import detect_peaks
from find_close_simple import find_close
from Tkinter import *
import Tkinter
import tkMessageBox
import tkFileDialog
from get_list_from_path import get_all_file_path

"""import sys
reload(sys)
sys.setdefaultencoding('utf-8')"""


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
        self.concentration = re.search(r'(?P<concentration2>\d.\d\d|\d\d.\d|\d{3}|[ck]{2})', f_path.split('/')[-1]).group('concentration2')

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
    pass
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
    compared_path_list = get_all_file_path(file_path)
    if chose_entry.get() in compared_path_list:
        compared_path_list.remove(chose_entry.get())

    for each_compared_path in compared_path_list:
        each_compared_path = each_compared_path.decode('gbk')
#        print(each_compared_path)
#        print(type(each_compared_path))
        print(each_compared_path.split('/'))
        concentration_path_dict[re.search(r'(?P<concentration2>\d.\d\d|\d\d.\d|\d{3})', each_compared_path.split('/')[-1]).group('concentration2')] = each_compared_path

    for path_dict in sorted(concentration_path_dict, key=lambda v: [int(i) for i in v.rstrip('@').split('.')]):
        compared_path_list2.append(concentration_path_dict[path_dict])
    standard_peaks_locs = peak_entry.get().split(';')  # 下面可以加上排序
    if standard_peaks_locs[-1] == '':
        standard_peaks_locs.remove(standard_peaks_locs[-1])
    make_path = make_entry.get()
    if make_path[-1] != '/' and make_path[-1] != '\\':
        make_path += '/'
    try:
        new_file = open(make_path+name_entry.get()+'.csv', 'a')
        for loc in standard_peaks_locs:
            new_file.write(',,'+loc)
        new_file.write('\n')
        new_file.write(ck.concentration)
        for loc in standard_peaks_locs:
            new_file.write(',,'+ck[loc])
        new_file.write('\n')

        for path in compared_path_list2:
            compared_peaks_locs_float = []
            spec = spectrum(path)
            final_r = spec.concentration
            for loc in standard_peaks_locs:
                if loc in spec.locs:
                    final_r += ',,'+spec[loc]
                else:
                    standard_loc_float = float(loc)
                    for compared_loc_str in spec.locs:
                        compared_peaks_locs_float.append(float(compared_loc_str))
                    close_peak_loc = find_close(standard_loc_float, compared_peaks_locs_float)
                    final_r += ",%s,%s" % (close_peak_loc, spec['{:.2f}'.format(Decimal(close_peak_loc))])
            new_file.write(final_r+'\n')
        new_file.write('\n')
        tkMessageBox.showinfo("已完成", "已完成")
    except:
        tkMessageBox.showwarning("Failed", "未能生成文件")
    finally:
        new_file.close()


app = Tk()
app.title("对比谱线")

AGEOPT = ['800', '1000']

ck_var = StringVar()
chose_entry = Entry(app, width=80, textvariable=ck_var)
chose_entry.grid(row=0, column=0)
chose_entry.bind('<Leave>', update_speclist)
Button(app, text="选择ck文件", command=ask_ck).grid(row=0, column=1, sticky=W)

folder_entry = Entry(app, width=80)
folder_entry.grid(row=1, column=0)
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
Button(app, text="+", command=add_peak,  width=6).grid(row=5, column=0, sticky=E)

target = Tkinter.StringVar(value='1000')
toption = Tkinter.OptionMenu(app, target, *AGEOPT)
toption.grid(row=5, column=1, sticky=W)

Button(app, text="对比谱线", command=make).grid(row=6, column=0)

app.mainloop()