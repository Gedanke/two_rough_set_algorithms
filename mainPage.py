# -*- coding: utf-8 -*-
import tkinter
import tkinter.filedialog
import tkinter.messagebox
import os.path
import time
from reduct import Reduct
from multiReduct import mulReduct
import re
import threading
from tkinter.scrolledtext import ScrolledText


class MainPage(object):
    def __init__(self):
        """"主窗口"""
        self.window = tkinter.Tk()
        self.window.title('基于粗糙集的增量式特征选择系统')
        self.window.geometry('1040x650')
        """数据成员"""
        self.al1_hit = False
        self.var_al = tkinter.StringVar()
        self.var_label_granularity = tkinter.StringVar()
        self.file_path = ''
        self.file_name = ''
        self.al_name = ''
        self.error_line = 0
        self.separator = ''
        self.reduction_set = []
        self.attr_B = ''
        self.now_time = tkinter.StringVar()
        """左侧布局"""
        '''打开文件'''
        self.button_open = tkinter.Button(self.window, text='打开', bg='#a3cf62', font=('Arial', 12),
                                          command=self.button_open_click)
        self.button_open.place(relwidth=0.13, relheight=0.17, relx=0, rely=0)
        '''检查数据'''
        self.button_check = tkinter.Button(self.window, text='检查数据', font=('Arial', 12),
                                           command=self.button_check_click)
        self.button_check.place(relwidth=0.122, relheight=0.18, relx=0, rely=0.16)
        '''保存特征选择结果'''
        self.button_save = tkinter.Button(self.window, text='保存结果', bg='#a3cf62', font=('Arial', 12),
                                          command=self.button_save_click)
        self.button_save.place(relwidth=0.13, relheight=0.18, relx=0, rely=0.33)
        '''算法一'''
        self.button_al1 = tkinter.Button(self.window, text='算法 1', bg='#f58220', font=('Arial', 12),
                                         command=self.button_al1_click)
        self.button_al1.place(relwidth=0.13, relheight=0.18, relx=0, rely=0.50)
        '''算法二'''
        self.button_al2 = tkinter.Button(self.window, text='算法 2', bg='#a3cf62', font=('Arial', 12),
                                         command=self.button_al12_click)
        self.button_al2.place(relwidth=0.13, relheight=0.18, relx=0, rely=0.66)
        '''帮助'''
        self.button_help_hit = False
        self.button_help = tkinter.Button(self.window, text='帮助', bg='#f58220', font=('Arial', 12),
                                          command=self.button_help_click)
        self.button_help.place(relwidth=0.13, relheight=0.18, relx=0, rely=0.83)
        """"中间布局"""
        '''显示当前算法名称'''
        self.label_content = tkinter.Label(self.window, textvariable=self.var_al, bg='green', font=('Arial', 16))
        self.label_content.place(relwidth=0.602, relheight=0.24, relx=0.12, rely=0)
        '''结果展示'''
        self.label_show = tkinter.Label(self.window, text='结果展示', bg='#a3cf62', font=('Arial', 12))
        self.label_show.place(relwidth=0.24, relheight=0.07, relx=0.34, rely=0.24)
        '''显示结果'''
        self.text_result = ScrolledText(self.window, bg='green',
                                        font=('Arial', 16))
        self.text_result.place(relwidth=0.68, relheight=0.69, relx=0.12, rely=0.31)
        """"右侧布局"""
        '''时间'''
        self.label_time = tkinter.Label(self.window, text='时间', bg='#a3cf62')
        self.label_time.place(relwidth=0.28, relheight=0.04, relx=0.722, rely=0)
        '''显示当前时间'''
        self.text_time = tkinter.Label(self.window, font=('Arial', 16))
        self.text_time.place(relwidth=0.28, relheight=0.16, relx=0.722, rely=0.04)
        self.show_time()
        '''了解'''
        self.button_learn_hit = False
        self.button_learn = tkinter.Button(self.window, text='了解', font=('Arial', 11), command=self.button_learn_click)
        self.button_learn.place(relwidth=0.28, relheight=0.052, relx=0.722, rely=0.19)
        '''参数设置'''
        self.label_set = tkinter.Label(self.window, text='参数设置', bg='#a3cf62', font=('Arial', 12))
        self.label_set.place(relwidth=0.20, relheight=0.07, relx=0.80, rely=0.24)
        '''决策属性数目'''
        self.var_decision_num = tkinter.StringVar()
        self.label_decision_num = tkinter.Label(self.window, text='决策属性数 ', font=('Arial', 11))
        self.label_decision_num.place(relwidth=0.08, relheight=0.06, relx=0.81, rely=0.355)
        self.entry_decision_num = tkinter.Entry(self.window, textvariable=self.var_decision_num, font=('Arial', 16))
        self.entry_decision_num.place(relwidth=0.10, relheight=0.08, relx=0.89, rely=0.335)
        '''精度 1 '''
        self.var_precision_one = tkinter.StringVar()
        self.label_precision_one = tkinter.Label(self.window, text='参数 1', font=('Arial', 11))
        self.label_precision_one.place(relwidth=0.05, relheight=0.06, relx=0.82, rely=0.47)
        self.entry_precision_one = tkinter.Entry(self.window, textvariable=self.var_precision_one, font=('Arial', 16))
        self.entry_precision_one.place(relwidth=0.10, relheight=0.08, relx=0.89, rely=0.45)
        '''精度 2 '''
        self.var_precision_two = tkinter.StringVar()
        self.label_precision_two = tkinter.Label(self.window, text='参数 2', font=('Arial', 11))
        self.label_precision_two.place(relwidth=0.05, relheight=0.06, relx=0.82, rely=0.59)
        self.entry_precision_two = tkinter.Entry(self.window, textvariable=self.var_precision_two, font=('Arial', 16))
        self.entry_precision_two.place(relwidth=0.10, relheight=0.08, relx=0.89, rely=0.57)
        '''精度 3 '''
        self.var_precision_three = tkinter.StringVar()
        self.label_precision_three = tkinter.Label(self.window, text='参数 3', font=('Arial', 11))
        self.label_precision_three.place(relwidth=0.05, relheight=0.06, relx=0.82, rely=0.705)
        self.entry_precision_three = tkinter.Entry(self.window, textvariable=self.var_precision_three,
                                                   font=('Arial', 16))
        self.entry_precision_three.place(relwidth=0.10, relheight=0.08, relx=0.89, rely=0.685)
        '''粒度 '''
        self.var_granularity = tkinter.StringVar()
        self.label_granularity = tkinter.Label(self.window, textvariable=self.var_label_granularity,
                                               font=('Arial', 11))
        self.label_granularity.place(relwidth=0.05, relheight=0.06, relx=0.82, rely=0.82)
        self.entry_granularity = tkinter.Entry(self.window, textvariable=self.var_granularity, font=('Arial', 16))
        self.entry_granularity.place(relwidth=0.10, relheight=0.08, relx=0.89, rely=0.80)
        '''确定'''
        self.button_sure = tkinter.Button(self.window, text='开始', bg='#f58220', font=('Arial', 15),
                                          command=self.button_sure_click)
        self.button_sure.place(relwidth=0.205, relheight=0.105, relx=0.80, rely=0.9)
        self.window.mainloop()

    """
    button_open_click(),button_check_click(),button_save_click(),button_sure_click()
    这四个事件(函数)所花费的时间，占用的资源比较多
    使用多线程，创建一个线程用于处理这些时间，防止主界面假死
    """

    def button_open_click(self):
        """
        使用多线程，创建一个线程用于打开并读取文件
        :return: NULL
        """
        thread = threading.Thread(target=self.button_open_click_thread)
        thread.setDaemon(True)
        thread.start()

    def button_open_click_thread(self):
        """
        打开txt文件，目前只设置了打开txt文件
        解析文件路径，对未选择文件进行错误提示
        同时得到数据集的分隔符
        分隔符得到的方法的前提是，数据对象是字母或者数字
        而分隔符是数字和字母之外的字符
        :return: NULL
        """
        self.file_path = tkinter.filedialog.askopenfilename(title='请选择 .txt 结尾的文本文件', filetypes=[('TXT', '*.txt')])
        full_file_name = os.path.split(self.file_path)[1]
        self.file_name, ext_name = os.path.splitext(full_file_name)
        if self.file_path == '':
            tkinter.messagebox.showwarning(title='警告', message='您未选择任何文件!')
        else:
            file = open(self.file_path, 'r')
            lines = file.readlines()
            line_one = lines[0]
            for i in line_one:
                if not i.isalnum():
                    self.separator = i
                    break
            tkinter.messagebox.showinfo(title='已选择文件', message='该文件的路径是 ' + self.file_path)

    def button_check_click(self):
        """
        使用多线程，创建一个线程用于打开并核对数据集 
        :return: NULL
        """
        self.thread = threading.Thread(target=self.check_data_thread)
        self.thread.setDaemon(True)
        self.thread.start()

    def check_data_thread(self):
        """
        数据校验部分,对未选择文件进行预警
        以分隔符作为校验,即统计每一个对象的属性数
        每一列有多少个分隔符
        若每一列的分隔符数目相同,数据无误
        否则指出可能有误所在的行数   
        :return: NULL
        """
        if self.file_path == '':
            tkinter.messagebox.showwarning(title='警告', message='您未选择任何文件!')
        else:
            full_file_name = os.path.split(self.file_path)[1]
            self.file_name, ext_name = os.path.splitext(full_file_name)
            if self.check_data():
                tkinter.messagebox.showinfo(title='数据', message='数据校验成功!')
            else:
                """暂时提示有缺失，后期可能加入那部分缺失"""
                tkinter.messagebox.showerror(title='错误',
                                             message='数据校验失败，该数据集部分内容不完整!\n' + '可能出现在第 ' + str(
                                                 self.error_line) + ' 行')

    def check_data(self):
        """
        数据检验部分，针对完备数据集
        :return: 
        返回判断结果
        @result
        """
        result = True
        list_separator = []
        file = open(self.file_path, 'r')
        lines = file.readlines()
        line_one = lines[0]
        count_separator = line_one.count(self.separator)
        for line in range(len(lines)):
            list_separator.append(lines[line].count(self.separator))
        for i in range(len(list_separator)):
            if list_separator[i] != count_separator:
                self.error_line = int(i) + 1
                result = False
                break
        return result

    def button_save_click(self):
        """
        使用多线程，创建一个子线程用来保存文件
        :return: 
        """
        self.thread = threading.Thread(target=self.button_save_click_thread)
        self.thread.setDaemon(True)
        self.thread.start()

    def button_save_click_thread(self):
        """
        保存文件操作
        保存文件的格式是*.txt , *.data , *.* 三种方式
        若未选择文件，提示先选择文件
        选择文件后
        若结果未生成，则提示先选择算法
        否则将结果写入文件中
        :return: NULL
        """
        file_save_path = tkinter.filedialog.asksaveasfilename(defaultextension='.txt',
                                                              filetypes=[('txt Files', '*.txt'),
                                                                         ('data Files', '*.data'),
                                                                         ('All Files', '*.*')])
        if file_save_path != '':
            if len(self.reduction_set) == 0:
                tkinter.messagebox.showerror(title='错误', message='结果还未生成，请先选择算法，设置参数然后点击确定')
            else:
                file = open(file_save_path, 'w')
                for i in range(len(self.reduction_set)):
                    string = ''
                    j = 0
                    for j in range(len(self.reduction_set[i]) - 1):
                        string += str(self.reduction_set[i][j]) + self.separator
                    if i != len(self.reduction_set) - 1:
                        string += str(self.reduction_set[i][j]) + '\n'
                    else:
                        string += str(self.reduction_set[i][j])
                    file.write(string)
                file.close()
                tkinter.messagebox.showinfo(title='成功', message='特征选择结果已经成功写入文件中\n' + '路径是 ' + file_save_path)
        else:
            tkinter.messagebox.showerror(title='保存失败', message='您得先选择您的文件!')

    def button_al1_click(self):
        """
        点击算法一，在中央横栏出显示算法一的名称
        :return: NULL
        """
        self.al_name = '算法一'
        self.var_al.set('算法一\n' + '\n基于知识粒度的决策系统经典的启发式属性约简算法')
        self.var_label_granularity.set('')

    def button_al12_click(self):
        """
        点击算法二，在中央横栏出显示算法二的名称
        :return: NULL
        """
        self.al_name = '算法二'
        self.var_al.set('算法二\n' + '\n基于知识粒度和多粒度视角的启发式约简算法')
        self.var_label_granularity.set('粒度')

    def button_help_click(self):
        """
        点击帮厨后，显示对程序的介绍
        :return: 
        """
        help_mes = tkinter.Tk()
        help_mes.title('帮助')
        help_mes.geometry('640x400')
        help_mes_text = '\t\t程序简介\n' + '\t本系统中有两个特征选择算法，算法理论层面上参考了' \
                                       'Yunge Jing, Tianrui Li, Hamido Fujita , Zeng Yu, Bin Wang，' \
                                       'An incremental attribute reduction approach based on knowledge granularity with a multi-granulation view，' \
                                       'Information Sciences 411 (2017) 23–38 中的算法一，算法二。\n' + \
                        '\n在实际实现过程中，加入了一些自己的理解，一部分体现在参数设置部分，点击了解更多可以了解到具体原因\n' + \
                        '\n使用时，选择完文件后，建议检查数据，其他的使用信息会以弹窗形式给出'
        button_mes = tkinter.Button(help_mes, text='了解更多', font=('Arial', 11), command=self.button_mes_click)
        button_mes.place(relwidth=0.15, relheight=0.1, relx=0.25, rely=0.78)
        button_exit = tkinter.Button(help_mes, text='退出', font=('Arial', 11), command=help_mes.destroy)
        button_exit.place(relwidth=0.15, relheight=0.1, relx=0.6, rely=0.78)
        message_help = tkinter.Message(help_mes, text=help_mes_text, font=('Arial', 12))
        message_help.pack()
        help_mes.mainloop()

    def button_mes_click(self):
        """
        点击弹出窗口中的更多，显示对程序的更多介绍
        :return: NULL
        """
        learn_more = tkinter.Tk()
        learn_more.title('了解更多')
        learn_more.geometry('750x450')
        text_title = '\t\t\t\t为什么会有这些参数\n'
        text_head = '\n在算法的理论层次上并不需要一部分参数，但为什么需要它们呢\n' + '' \
                                                         '首先，介绍下各个参数的作用，有默认值，可以不输入\n\n'
        text_1 = '\n决策属性个数: 默认为1\n'
        text_2 = '\n各个精度设置的原因是，该系统选择了python语言，其定义的变量精度很高，' \
                 '而在其他语言中如果使用基本的变量，会有精度限制，或者精度截断，即计算机实际得到的结果与预期结果可能会有出路。此处将精度控制权交给使用者，' \
                 '让其选择自己需要的精度参数，从而得到预期结果。\n'
        text_3 = '\n参数一: 默认为0.0，在原算法选择核属性时，计算内部属性重要度，其值要大于0，此处可以设置为0-1之间的浮点数，即超过该值则认为大于0\n'
        text_4 = '\n参数二: 默认为1e-7，此处是判断约简集和条件属性集的知识粒度是否相等，不相等满足条件，此处可以设置二者差的' \
                 '绝对值在什么样的范围内默认是相等的，超过该范围则认为不相等，不建议设置成0.0\n'
        text_5 = '\n参数三: 默认为0，判断条件属性集和约简集去除约简集中的一个元素的知识粒度是否相等，' \
                 '相等则满足条件，此处认为二者差的绝对值在该范围内就是相等\n'
        text_6 = '\n粒度: 只在第二个算法中出现并使用，必须输入正整数\n'
        text_mine = '\n\n作者邮箱：13767927306@163.com\n\n' + '使用过程中，对该系统的程序或者其他问题可以与本人联系哦!'
        learn_more_text = text_title + text_head + text_1 + text_2 + text_3 + text_4 + text_5 + text_6 + text_mine
        mes_learn_more = ScrolledText(learn_more, font=('Arial', 12))
        mes_learn_more.insert('insert', learn_more_text)
        mes_learn_more.place(relwidth=1, relheight=1, relx=0, rely=0)
        learn_more.mainloop()

    def show_time(self):
        """
        显示当前时间
        循环以一秒钟的间隔显示时间
        :return: NULL
        """
        self.now_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.text_time.configure(text=self.now_time)
        self.window.after(1000, self.show_time)

    def button_learn_click(self):
        """
        根据选择的算法显示对该算法的介绍
        :return: NULL
        """
        text_learn_al1 = '算法一简介\n\n' + \
                         '\n基于知识粒度的经典启发式属性约简算法\n' + \
                         '\n针对决策系统的基于知识粒度的经典启发式属性约简算法\n' + '' \
                                                           '\n详细介绍可参考相关论文'
        text_learn_al2 = '算法二简介\n\n' + '' \
                                       '\n基于知识粒度的多粒度启发式约简算法\n' \
                         + '\n简单来说，就是将一个大的数据集划分成若干个小的数据集\n' + \
                         '\n在每个子数据集上求得约简结果后，合并\n' + \
                         '\n分而治之的方法，会使特征选择的时间复杂度明显减少，程序耗时减少\n' + \
                         '\n详细介绍可参考相关论文'
        if self.al_name == '算法一':
            self.show_name(text_learn_al1)
        elif self.al_name == '算法二':
            self.show_name(text_learn_al2)
        else:
            tkinter.messagebox.showinfo(title='提示', message='您还未选择任何算法!')

    def show_name(self, text_learn_al):
        """
        :param text_learn_al: 显示当前中央横栏处算法的详细介绍。
        :return: NULL
        """
        learn_mes = tkinter.Tk()
        learn_mes.title('了解该算法')
        learn_mes.geometry('640x400')
        label_learn = tkinter.Label(learn_mes, text=text_learn_al, font=('Arial', 12))
        label_learn.pack()
        button_exit = tkinter.Button(learn_mes, text='退出', font=('Arial', 11), command=learn_mes.destroy)
        button_exit.place(relwidth=0.15, relheight=0.1, relx=0.425, rely=0.8)
        learn_mes.mainloop()

    def button_sure_click(self):
        """
        使用多线程，创建一个子线程用来处理特征选择过程
        :return: NULL
        """
        self.thread = threading.Thread(target=self.button_sure_click_thread)
        self.thread.setDaemon(True)
        self.thread.start()

    def button_sure_click_thread(self):
        """
        该部分首先得到五个参数输入框的内容
        注意，选择算法一时，粒度参数不出现
        对五个参数进行校验，返回其相应的逻辑值和提示信息
        当框内不输入参数时，使用并显示默认参数
        仅仅是选择算法二时，粒度参数必须强制输入，其他任何参数可以不输入
        首先先判断是否选择了文件以及是否选择了算法
        若没有，发出对应的提示信息
        符合条件后，根据选择的算法
        调用相应的算法类，以及得到的参数
        得到结果，显示在文本框中
        :return: NULL
        """
        if self.file_path == '' or self.separator == '':
            tkinter.messagebox.showerror(title='错误', message='未导入文件，请先导入文件，并核对数据')
        else:
            self.text_result.delete(1.0, 'end')
            result_decision_num, mes_decision_num = self.decision_num_check()
            result_precision_one, mes_precision_one = self.precision_one_check()
            result_precision_two, mes_precision_two = self.precision_two_check()
            result_precision_three, mes_precision_three = self.precision_three_check()
            result_granularity, mes_granularity = self.granularity_check()
            decision_num = int(self.var_decision_num.get())
            precision_set = [float(self.var_precision_one.get()), float(self.var_precision_two.get()),
                             float(self.var_precision_three.get())]
            result = result_decision_num and result_precision_one and result_precision_two and result_precision_three
            if not self.check_data():
                tkinter.messagebox.showerror(title='错误', message='数据集可能有误，请核对数据!')
            else:
                # 选择算法一进行特征选择
                if self.al_name == '算法一':
                    if result:
                        algorithm1 = Reduct(self.file_path, self.separator, decision_num, precision_set)
                        tkinter.messagebox.showinfo(title='选择成功', message='您已经选择算法一进行特征选择!')
                        self.reduction_set = []
                        self.attr_B = ''
                        time_start = time.time()
                        algorithm1.gainReduct()
                        time_end = time.time()
                        self.reduction_set = algorithm1.attrB
                        for i in range(len(algorithm1.yuejian) - 1):
                            self.attr_B += str(algorithm1.yuejian[i]) + ' , '
                        self.attr_B += str(algorithm1.yuejian[len(algorithm1.yuejian) - 1])
                        content = self.file_name + '数据集\n' + '有 ' + str(algorithm1.rowsNum) + ' 个对象，有 ' + str(
                            algorithm1.listsNum) + ' 个属性\n' + '特征选择耗时是 ' + str(
                            time_end - time_start) + ' s\n特征选择的结果(列):\n' + self.attr_B
                        self.text_result.insert('insert', content)
                        del algorithm1

                    else:
                        tkinter.messagebox.showerror(title='错误',
                                                     message='1.  ' + mes_decision_num + '\n' + '2.  ' + mes_precision_one + '\n' + '3.  ' + mes_precision_two + '\n' + '4.  ' + mes_precision_three)
                # 选择算法二进行特征选择
                elif self.al_name == '算法二':
                    if result and result_granularity:
                        algorithm2 = mulReduct(self.file_path, self.separator, decision_num,
                                               int(self.var_granularity.get()),
                                               precision_set)
                        tkinter.messagebox.showinfo(title='选择成功', message='您已经选择算法二进行特征选择!')
                        self.reduction_set = []
                        self.attr_B = ''
                        time_start = time.time()
                        algorithm2.multiReduct()
                        time_end = time.time()
                        self.reduction_set = algorithm2.attrB
                        for i in range(len(algorithm2.result) - 1):
                            self.attr_B += str(algorithm2.result[i]) + ' , '
                        self.attr_B += str(algorithm2.result[len(algorithm2.result) - 1])
                        content = self.file_name + '数据集\n' + '有 ' + str(algorithm2.rowsNum) + ' 个对象，有 ' + str(
                            algorithm2.listsNum) + ' 个属性\n' + '特征选择耗时是 ' + str(
                            time_end - time_start) + ' s\n' + '该数据集被划分为 ' + str(
                            self.var_granularity.get()) + ' 个粒度\n特征选择的结果(列):\n' + self.attr_B
                        self.text_result.insert('insert', content)
                        del algorithm2
                else:
                    tkinter.messagebox.showerror(title='错误', message='您未新选择任何算法!')

    def decision_num_check(self):
        """
        先判断决策属性数，输入的数必须为正整数，未输入则默认为1
        :return: 
        @result:判断结果
        @mes_decision_num:弹窗中的提示信息
        """
        result = False
        decision_num = self.var_decision_num.get()
        mes_decision_num = ''
        if decision_num != '':
            if not str(decision_num).isdigit():
                mes_decision_num = decision_num + '不是正整数'
            else:
                if int(decision_num) <= 0:
                    mes_decision_num = decision_num + '不是正整数'
                else:
                    result = True
                    mes_decision_num = '您已经成功设置决策属性为 ' + decision_num
        else:
            result = True
            self.var_decision_num.set('1')
            mes_decision_num = '您使用了默认值 ' + self.var_decision_num.get()
        return result, mes_decision_num

    def precision_one_check(self):
        """
        参数1
        范围在0-1之间的浮点数，默认值为0.0
        :return: 
        @result:判断结果
        @mes_decision_one:弹窗中的提示信息
        """
        result = False
        mes_precision_one = ''
        precision_one_num = self.var_precision_one.get()
        '''判断条件的正则表达式'''
        value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
        result_one = value.match(precision_one_num)
        if precision_one_num != '':
            if result_one:
                if 0 <= float(precision_one_num) and float(precision_one_num) < 1:
                    result = True
                    mes_precision_one = '您已经设置了第一个精度 ' + precision_one_num
                else:
                    mes_precision_one = precision_one_num + ' 该参数不在合理范围内'
            else:
                mes_precision_one = precision_one_num + ' 不是浮点数'
        else:
            self.var_precision_one.set('0.0')
            mes_precision_one = '您使用了默认值' + precision_one_num
            result = True
        return result, mes_precision_one

    def precision_two_check(self):
        """
        参数2
        范围在0-1之间的浮点数，越接近0越好，默认值是1e-7
        :return: 
        @result:判断结果
        @mes_decision_two:弹窗中的提示信息
        """
        result = False
        mes_precision_two = ''
        precision_two_num = self.var_precision_two.get()
        '''判断条件的正则表达式'''
        value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
        result_two = value.match(precision_two_num)
        if precision_two_num != '':
            if result_two:
                if 0 <= float(precision_two_num) and float(precision_two_num) < 1:
                    result = True
                    mes_precision_two = '您已经设置了第二个精度 ' + precision_two_num
                else:
                    mes_precision_two = precision_two_num + '该参数不在合理范围内'
            else:
                mes_precision_two = precision_two_num + ' 不是浮点数'
        else:
            self.var_precision_two.set('0.0000001')
            mes_precision_two = '您使用了默认值' + precision_two_num
            result = True
        return result, mes_precision_two

    def precision_three_check(self):
        """
        参数3
        范围在0-1之间的浮点数，默认值为0.0
        :return: 
        @result:判断结果
        @mes_decision_three:弹窗中的提示信息
        """
        result = False
        mes_precision_three = ''
        precision_three_num = self.var_precision_three.get()
        '''判断条件的正则表达式'''
        value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
        result_one = value.match(precision_three_num)
        if precision_three_num != '':
            if result_one:
                if 0 <= float(precision_three_num) and float(precision_three_num) < 1:
                    result = True
                    mes_precision_three = '您已经设置了第三个精度 ' + precision_three_num
                else:
                    mes_precision_three = precision_three_num + '该参数不在合理范围内'
            else:
                mes_precision_three = precision_three_num + ' 不是浮点数'
        else:
            self.var_precision_three.set('0.0')
            mes_precision_three = '您使用了默认值' + precision_three_num
            result = True
        return result, mes_precision_three

    def granularity_check(self):
        """
        粒度值，选择算法一时，固定为1
        选择算法二时，需要用户输入
        :return: 
        @result:判断结果
        @mes_granularity:弹窗中的提示信息
        """
        mes_granularity = ''
        result = False
        if self.al_name == '算法一':
            self.var_granularity.set('')
        else:
            if self.var_granularity.get() == '':
                mes_granularity = '您未设置粒度数!'
            else:
                if not str(self.var_granularity.get()).isdigit():
                    mes_granularity = self.var_granularity.get() + '不是正整数'
                else:
                    if int(self.var_granularity.get()) < 0:
                        mes_granularity = self.var_granularity.get() + '不是正整数'
                    else:
                        result = True
                        mes_granularity = '您已经设置了粒度!' + self.var_granularity.get()
        return result, mes_granularity
