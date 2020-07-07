"""
Created by fmujie on 2020/6/10
"""
__author__ = ''

from tkinter import Tk, StringVar, Label, Button, Entry, Radiobutton
from numpy import mean, var
from math import sqrt, log10
from tkinter.messagebox import showinfo


class App(object):
    window = Tk()
    window.title('Calculation window')
    window.geometry('500x300')
    kw = 10 ** 14
    num_a = 65
    num_b = 71
    num_c = 65
    ef_load_judge = False
    F = False
    number_arr = []
    string_arr = []
    cur_string_arr = []
    cur_number_arr = []
    var = StringVar()
    dicts_main = {
        'A': '平均值',
        'B': '平均偏差',
        'C': '相对平均偏差',
        'D': '标准偏差',
        'E': '相对标准偏差',
        'F': '溶液H+离子浓度',
        'G': '强酸',
        'H': '一元弱酸',
        'I': '两性物质',
        'J': '缓冲溶液'
    }

    dicts_middle = {
        'A': '一位',
        'B': '两位',
        'C': '三位',
        'D': '四位'
    }

    # 初始化实例属性、方法
    def __init__(self):
        self.lab = Label(self.window, bg='yellow', width=60, height=2, text='Please check method.')
        self.lab.pack()
        self.btn = None
        self.entry = None
        self.option = None
        self.option2 = None
        self.sure_btn = None
        self.ef_digits = None
        self.reset_btn = None
        self.load_r('r')

    #
    def print_ser0(self):
        current_ef_digits = self.__class__.var.get()
        self.ef_digits = str(int(current_ef_digits) - 64)
        self.lab.config(text='You want to keep ' + self.ef_digits)

        self.pk_forget('r0', 65, 68)

        self.sure_btn = Button(self.window, text='calculate', width=15, height=2, command=self.calculate)
        self.sure_btn.pack()

    """
    功能封装, 简化代码(组件隐藏与显示)
    """
    def pk_forget(self, name, num1=65, num2=70, judge=False):
        for i in range(num1, num2 + 1):
            attr_name = name + chr(i)
            if not judge:
                getattr(self, attr_name).pack_forget()
            else:
                getattr(self, attr_name).pack()

    """
    展示所选选项内容并初始化输入表格与添加按钮
    """
    def print_selection(self):
        self.option = self.__class__.var.get()
        self.lab.config(text='You have selected ' + self.__class__.var.get() + ', please add numbers separated by commas.')

        self.pk_forget('r')

        self.entry = Entry(self.window, show=None)
        self.entry.pack()

        self.btn = Button(self.window, text='add numbers', width=15, height=2, command=self.add_numbers)
        self.btn.pack()

    """
    效果同上print_selection(), 展示G H I J选项
    """
    def print_ser1(self):
        self.option = self.__class__.var.get()
        self.lab.config(text='You have selected ' + self.__class__.var.get() + ', please add numbers separated by commas.')

        self.pk_forget('r1', 71, 74)

        self.entry = Entry(self.window, show=None)
        self.entry.pack()

        self.btn = Button(self.window, text='add numbers', width=15, height=2, command=self.add_numbers)
        self.btn.pack()

    """
    展示保留位数选项
    """
    def ef_digits_btn(self):
        self.sure_btn.pack_forget()
        self.lab.config(text='Please enter the number of valid digits to keep.')

        if self.__class__.ef_load_judge is False:
            self.load_r('r0', 65, 68, False)
            self.__class__.ef_load_judge = True
        else:
            self.pk_forget('r0', 65, 68, True)

    """
    重置按钮
    """
    def reset(self):
        self.lab.config(text='Please check method.')
        self.reset_btn.pack_forget()

        self.pk_forget('r', 65, 70, True)

        self.__class__.cur_string_arr = []
        self.__class__.cur_number_arr = []

    # 选择 F 后的逻辑
    def select_h(self):
        self.option2 = self.__class__.var.get()
        self.lab.config(text='Please check method.')

        self.pk_forget('r')

        if self.F is False:
            self.load_r('r1', 71, 74)
        else:
            self.pk_forget('r1', 71, 74, True)

    """
    自定义switch, python语法不支持(利用字典变相实现其功能)
    包含A B C D E简单算法功能
    lambda表达式精简代码
    """
    @staticmethod
    def switch(item):
        switcher = {
            "A": lambda res: mean(res),
            "B": lambda res: mean(list(map(lambda x: abs(x - mean(res)), res))),
            "C": lambda res: mean(list(map(lambda x: abs(x - mean(res)), res))) / mean(res),
            "D": lambda res: sqrt(var(res)),
            "E": lambda res: sqrt(var(res)) / mean(res),
        }
        return switcher.get(item, 'No that method.')

    """
    效果同上switch()
    包含G H I J简单算法功能
    lambda表达式精简代码
    """
    def switch2(self, item):
        switcher = {
            "G": lambda res: (res[0] + sqrt(res[0] ** 2 + 4 * self.__class__.kw)) / 2,
            "H": lambda res: sqrt(res[0] * res[1]),
            "J": lambda res: (-log10(res[0])) + log10(res[1] / res[2]),
        }
        return switcher.get(item, 'No that method.')

    """
    点击计算按钮后实现的计算功能
    保留有效数字规则如下：
    若结果的有效位数<选项保留有效位数，则选项无效
    若结果是含有%的简单算法 C / E, 则有效位数为小数部分(以上为format()函数所限)
    """
    def calculate(self):
        sett = '.' + self.ef_digits
        setted = sett + 'g'

        if self.option2 is None:
            resf = self.switch(self.option)
            if self.option == 'C' or self.option == 'E':
                setted = sett + '%'
        else:
            if self.option == 'H' or self.option == 'I':
                self.option = 'H'
            resf = self.switch2(self.option)

        res_number = resf(self.__class__.number_arr)

        if self.option != 'C' or self.option != 'E':
            num_arr = str(res_number).split('.', 1)
            if len(num_arr[0]) > int(self.ef_digits):
                setted = sett + 'f'

        result = format(res_number, setted)
        self.lab.config(text='The result is: ' + result)

        self.sure_btn.pack_forget()

        self.reset_btn = Button(self.window, text='reset', width=15, height=2, command=self.reset)
        self.reset_btn.pack()

    """
    输入框添加数字功能, 英文逗号分隔
    A B C D E无限制
    G H I J根据所给参数限制如下:
    G -> 浓度 C, 多填的数据无效
    H / I -> K C / K1 K2, 多填的数据无效
    J -> Ka Cb Ca
    按照上述顺序则逻辑正确 
    这边写的不符合编码规范, 太过冗余, 去掉相关条件会更简洁
    """
    def add_numbers(self):
        values = self.entry.get()
        if values == '':
            showinfo(message='请输入具体数值，以英文逗号分隔')
        else:
            self.__class__.cur_string_arr = values.split(",")
            self.__class__.cur_number_arr = list(map(float, self.__class__.cur_string_arr))
            if self.option == 'H' or self.option == 'I':
                if len(self.__class__.cur_number_arr) < 2:
                    showinfo(message='请输入K C / K1 K2两位数值，以英文逗号分隔')
                else:
                    self.lab.config(text='You have add ' + values)
                    self.__class__.string_arr = values.split(",")
                    self.__class__.number_arr = list(map(float, self.__class__.string_arr))
                    self.entry.pack_forget()
                    self.btn.pack_forget()
                    self.sure_btn = Button(self.window, text='effective', width=15, height=2,
                                           command=self.ef_digits_btn)
                    self.sure_btn.pack()
            elif self.option == 'J':
                if len(self.__class__.cur_number_arr) < 3:
                    showinfo(message='请输入Ka Cb Ca三位数值，以英文逗号分隔')
                else:
                    self.lab.config(text='You have add ' + values)
                    self.__class__.string_arr = values.split(",")
                    self.__class__.number_arr = list(map(float, self.__class__.string_arr))
                    self.entry.pack_forget()
                    self.btn.pack_forget()
                    self.sure_btn = Button(self.window, text='effective', width=15, height=2,
                                           command=self.ef_digits_btn)
                    self.sure_btn.pack()
            else:
                self.lab.config(text='You have add ' + values)
                self.__class__.string_arr = values.split(",")
                self.__class__.number_arr = list(map(float, self.__class__.string_arr))
                self.entry.pack_forget()
                self.btn.pack_forget()
                self.sure_btn = Button(self.window, text='effective', width=15, height=2,
                                       command=self.ef_digits_btn)
                self.sure_btn.pack()

    """
    初始化选项函数
    三合一:
    1、A B C D E F   变量为rA rB...
    2、G H I J   变量为r1G r1H...
    3、A B C D   变量为r0A r0B...(保留有效数字选项)
    """
    def load_r(self, name, num1=65, num2=70, judge=True):
        for i in range(num1, num2 + 1):
            attr_name = name + chr(i)
            if num1 == 71:
                self.__class__.F = True
                stt = self.__class__.dicts_main.get(chr(i))
                setattr(self, attr_name, Radiobutton(
                    self.window, text=chr(i) + ' ' + stt,
                    variable=self.__class__.var, value=chr(i),
                    command=self.print_ser1
                ))
                self.pk_forget('r1', self.__class__.num_b, self.__class__.num_b, True)
                self.__class__.num_b = self.__class__.num_b + 1
            else:
                if judge:
                    stt = self.__class__.dicts_main.get(chr(i))
                    if chr(i) != 'F':
                        setattr(self, attr_name, Radiobutton(
                            self.window, text=chr(i) + ' ' + stt,
                            variable=self.__class__.var, value=chr(i),
                            command=self.print_selection
                        ))
                    else:
                        setattr(self, attr_name, Radiobutton(
                            self.window, text=chr(i) + ' ' + stt,
                            variable=self.__class__.var, value=chr(i),
                            command=self.select_h
                        ))
                    self.pk_forget('r', self.__class__.num_a, self.__class__.num_a, True)
                    self.__class__.num_a = self.__class__.num_a + 1
                else:
                    stt = self.__class__.dicts_middle.get(chr(i))
                    setattr(self, attr_name, Radiobutton(
                        self.window, text=chr(i) + ' ' + stt,
                        variable=self.__class__.var, value=str(i),
                        command=self.print_ser0
                    ))
                    self.pk_forget('r0', self.__class__.num_c, self.__class__.num_c, True)
                    self.__class__.num_c = self.__class__.num_c + 1
    """
    窗口循环显示
    """
    def main(self):
        self.window.mainloop()


if __name__ == '__main__':
    root = App()
    root.main()
