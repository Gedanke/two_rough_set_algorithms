# -*- coding: utf-8 -*-
import pickle
import tkinter.messagebox
from mainPage import *
import re


class LoginPage(object):
    def __init__(self, master=None):
        """
        :param master: tkinter.Tk
        """
        self.window = master
        '''设置登陆窗口的大小'''
        self.window.geometry('800x500')
        self.var_user_name = tkinter.StringVar()
        self.var_user_password = tkinter.StringVar()
        self.signup = False
        ''''注册与登录界面'''
        '''名称'''
        self.label_title = tkinter.Label(self.window, text='基于粗糙集的增量式特征选择系统', bg='green', font=('', 16))
        self.label_title.place(relwidth=0.5, relheight=0.15, relx=0.25, rely=0.1)
        '''输入用户名'''
        self.label_name = tkinter.Label(self.window, text='用户名:', font=('', 16))
        self.label_name.place(relwidth=0.1, relheight=0.06, relx=0.23, rely=0.35)
        self.var_user_name.set('')
        self.entry_name = tkinter.Entry(self.window, textvariable=self.var_user_name, font=('', 18))
        self.entry_name.place(relwidth=0.4, relheight=0.09, relx=0.35, rely=0.335)
        '''输入密码'''
        self.label_password = tkinter.Label(self.window, text='密码:', font=('', 16))
        self.label_password.place(relwidth=0.1, relheight=0.06, relx=0.23, rely=0.525)
        self.entry_password = tkinter.Entry(self.window, textvariable=self.var_user_password,
                                            font=('', 18), show='*')
        self.entry_password.place(relwidth=0.4, relheight=0.09, relx=0.35, rely=0.50)
        '''登录操作'''
        self.button_login = tkinter.Button(self.window, text='登录', font=('', 17), command=self.user_login)
        self.button_login.place(relwidth=0.15, relheight=0.1, relx=0.25, rely=0.72)
        '''注册操作'''
        self.button_signup = tkinter.Button(self.window, text='注册', font=('', 17), command=self.user_signup)
        self.button_signup.place(relwidth=0.15, relheight=0.1, relx=0.6, rely=0.72)

    def user_login(self):
        """
        定义用户登录功能
        :return: NULL
        """
        user_name = self.var_user_name.get()
        user_pwd = self.var_user_password.get()
        '''这里设置异常捕获，当我们第一次访问用户信息文件时是不存在的，所以这里设置异常捕获。
        中间的两行就是我们的匹配，即程序将输入的信息和文件中的信息匹配。'''
        try:
            with open('user_info.pickle', 'rb') as user_file:
                user_info = pickle.load(user_file)
        except FileNotFoundError:
            '''这里就是我们在没有读取到user_file的时候，程序会创建一个'user_file'这个文件，并将管理员
            的用户和密码写入，即用户名为'admin'密码为'admin'。'''
            with open('user_info.pickle', 'wb') as user_file:
                user_info = {'admin': 'admin'}
                pickle.dump(user_info, user_file)
                # 必须先关闭，否则pickle.load()会出现EOFError: Ran out of input
                user_file.close()
        '''如果用户名和密码与文件中的匹配成功，则会登录成功
        同时销毁登录窗口，转到主窗口'''
        if user_name in user_info:
            if user_pwd == user_info[user_name]:
                self.window.destroy()
                MainPage()
            # 如果用户名匹配成功，而密码输入错误，则会弹出‘您的密码错误，请继续尝试!'
            else:
                tkinter.messagebox.showerror(message='您的密码错误，请继续尝试!')
        # 如果发现用户名不存在
        else:
            is_sign_up = tkinter.messagebox.askyesno('欢迎您', '您还未注册，现在注册吗?')
            '''提示需不需要注册新用户'''
            if is_sign_up:
                self.user_signup()

    def user_signup(self):
        """
        定义用户注册功能
        对注册的用户名和密码进行限制
        用户名：只允许使用26个英文字母(大写，小写都可以)，10个数字的组合
        长度没有限制，不允许使用纯数字，可以是中文，纯字母，数字或者组合
        密码：字母和数字的组合，至少8个字符，不能有中文--isalpha()
        确认密码：字母和数字的组合，至少8个字符--isalpha()，和密码一致
        :return: NULL
        """

        def signup():
            """
            注册操作
            :return: 
            """
            # 以下三行就是获取我们注册时所输入的信息
            np = new_pwd.get()
            npf = new_pwd_confirm.get()
            nn = new_name.get()
            mes_np = self.pwd_check(np)[1]
            mes_npf = self.pwd_check(npf)[1]
            mes_nn = self.name_check(nn)[1]
            '''对用户名，密码，确认密码进行限制'''
            if self.name_check(nn)[0] and self.pwd_check(np)[0] and self.pwd_check(npf):
                # 这里是打开我们记录数据的文件，将注册信息读出
                with open('user_info.pickle', 'rb') as user_file:
                    exist_user_info = pickle.load(user_file)
                '''这里就是判断，如果两次密码输入不一致，则提示‘密码和确认密码必须相同!’'''
                if np != npf:
                    tkinter.messagebox.showerror('错误', '密码和确认密码必须相同!')
                else:
                    '''如果用户名已经在我们的数据文件中，则提示该用户已经被注册了!'''
                    if nn in exist_user_info:
                        tkinter.messagebox.showerror('错误', '该用户已经被注册了!')
                    # 最后如果输入无以上错误，则将注册输入的信息记录到文件当中，并提示注册成功
                    else:
                        exist_user_info[nn] = np
                        with open('user_info.pickle', 'wb') as user_file:
                            pickle.dump(exist_user_info, user_file)
                        tkinter.messagebox.showinfo('欢迎您', '您已注册成功!')
                        '''销毁弹窗'''
                        self.signup = False
                        window_signup.destroy()
            else:
                tkinter.messagebox.showerror(title='错误', message=mes_nn + '\n' + mes_np + '\n' + mes_npf)

        '''定义长在窗口上的窗口'''
        window_signup = tkinter.Toplevel(self.window)
        window_signup.geometry('400x300')
        window_signup.title('注册窗口')
        '''将输入的注册名赋值给变量'''
        new_name = tkinter.StringVar()
        new_name.set('')
        tkinter.Label(window_signup, text='用户名: ', font=('', 10)).place(x=20, y=20)
        entry_new_name = tkinter.Entry(window_signup, textvariable=new_name)
        entry_new_name.place(x=130, y=20)
        new_pwd = tkinter.StringVar()
        tkinter.Label(window_signup, text='密码: ', font=('', 10)).place(x=20, y=70)
        entry_user_pwd = tkinter.Entry(window_signup, textvariable=new_pwd, show='*')
        entry_user_pwd.place(x=130, y=70)
        new_pwd_confirm = tkinter.StringVar()
        tkinter.Label(window_signup, text='确认密码: ', font=('', 10)).place(x=20, y=120)
        entry_user_pwd_confirm = tkinter.Entry(window_signup, textvariable=new_pwd_confirm, show='*')
        entry_user_pwd_confirm.place(x=130, y=120)
        button_comfirm_signup = tkinter.Button(window_signup, text='注册', font=('', 10), command=signup)
        button_comfirm_signup.place(x=180, y=180)

    def name_check(self, name):
        """
        用户名核对
        :param name: 用户名
        :return: 
        @result:用户名核对结果
        @mes_result:弹窗中的提示信息
        """
        result = False
        mes_result = ''
        if name.isdigit():
            mes_result = '用户名不能是纯数字!'
        else:
            if name.isalnum():
                result = True
            else:
                mes_result = '用户名只能是中文，纯字母，字母和数字的组合!'
        return result, mes_result

    def pwd_check(self, pwd):
        """
        密码核对
        :param pwd:密码
        :return: 
        @result:密码核对结果
        @mes_result:弹窗中的提示信息
        """
        result = False
        mes_result = ''
        '''正则表达式，检验字符串中是否含有中文'''
        zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
        word = pwd.encode('utf-8').decode('utf-8')
        if zh_pattern.search(word):
            mes_result = '密码中不能有中文!'
        else:
            if len(pwd) < 8:
                mes_result = '密码至少要8位!'
            else:
                if not pwd.isalnum():
                    mes_result = '密码必须是字母和数字的组合!'
                else:
                    result = True
        return result, mes_result
