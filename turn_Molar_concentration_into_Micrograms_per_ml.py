#coding:gbk

ask = 'y'
while True:
    molar_mass = input("输入摩尔质量数：")
    M = input('输入以M为单位的浓度\n（如3.6×10-4请输入“3.6*10**-4”）：')
    ans = M*molar_mass
    ans = ans/1000  # 每ml中有多少克（未除前为每L）
    ans = ans*1000  # 每ml中有多少毫克
    ans = ans*1000  # 每ml中有多少微克
    print("换算后的浓度为 %s μg/ml" % ans)
    ask = raw_input("继续请输入任意键，退出请输入n或N确定：")
    if ask =='n' or ask == 'N':
        break
