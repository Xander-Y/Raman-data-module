#coding:gbk

ask = 'y'
while True:
    molar_mass = input("����Ħ����������")
    M = input('������MΪ��λ��Ũ��\n����3.6��10-4�����롰3.6*10**-4������')
    ans = M*molar_mass
    ans = ans/1000  # ÿml���ж��ٿˣ�δ��ǰΪÿL��
    ans = ans*1000  # ÿml���ж��ٺ���
    ans = ans*1000  # ÿml���ж���΢��
    print("������Ũ��Ϊ %s ��g/ml" % ans)
    ask = raw_input("������������������˳�������n��Nȷ����")
    if ask =='n' or ask == 'N':
        break
