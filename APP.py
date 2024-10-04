from tkinter import *
from tkinter.messagebox import *
from ttkbootstrap import Style
import tkinter.ttk as ttk
import pickle

# 封装 tkinter
class APP:
    def __init__(self, filename):
        # 储存信息和选中索引
        self.filename = filename
        self.info = {}
        self.index = None

    # 初始化窗口
    def tkinit(self):
        # ttkbootstrap 风格美化
        style = Style(theme='sandstone')
        self.root = style.master
        self.root.title('密码管理器')

        # 注意要在窗口产生后定义 tk 变量
        self.Title = StringVar()
        self.Title.set('无标题')
        self.title = StringVar()
        self.account = StringVar()
        self.pwd = StringVar()
        self.detail = StringVar()

        # 获得窗口框架，设置对齐方式和窗口尺寸
        frame = Frame(self.root)
        frame.pack(fill=BOTH, expand=1, padx=100, pady=100)

        # 查看内容的框架
        viewFrame = Frame(frame)
        viewFrame.pack(side=LEFT, padx=5, fill=BOTH)

        # 输入内容的框架
        inputFrame = Frame(frame)
        inputFrame.pack(side=LEFT, padx=5, fill=BOTH)

        # 输入内容
        Label(inputFrame, textvariable=self.Title, font=('Consolas', 13)).grid(row=0, column=3)

        Label(inputFrame, text='标题', font=('Consolas', 12)).grid(row=1, column=1)
        Label(inputFrame, text='账户', font=('Consolas', 12)).grid(row=2, column=1)
        Label(inputFrame, text='密码', font=('Consolas', 12)).grid(row=3, column=1)
        Label(inputFrame, text='描述', font=('Consolas', 12)).grid(row=4, column=1)

        self.entryTitle = ttk.Entry(inputFrame, textvariable=self.title, width=30)
        self.entryAccount = ttk.Entry(inputFrame, textvariable=self.account, width=30)
        self.entryPwd = ttk.Entry(inputFrame, textvariable=self.pwd, width=30)
        self.entryDetail = ttk.Entry(inputFrame, textvariable=self.detail, width=30)

        self.entryTitle.grid(row=1, column=2, columnspan=3, padx=10, pady=5)
        self.entryAccount.grid(row=2, column=2, columnspan=3, padx=10, pady=5)
        self.entryPwd.grid(row=3, column=2, columnspan=3, padx=10, pady=5)
        self.entryDetail.grid(row=4, column=2, columnspan=3, padx=10, pady=5)

        ttk.Button(inputFrame, text='新增', width=6, command=self.insert).grid(row=5, column=2, pady=5)
        ttk.Button(inputFrame, text='提交', width=6, command=self.commit).grid(row=5, column=3, pady=5)
        ttk.Button(inputFrame, text='删除', width=6, command=self.delete).grid(row=5, column=4, pady=5)

        # 设置滚动条
        sb = ttk.Scrollbar(viewFrame)
        sb.pack(side=RIGHT, fill=Y)

        # 列表盒绑定鼠标按键
        self.titleBox = Listbox(viewFrame, yscrollcommand=sb.set, width=30, height=12, font=('Consolas', 12))
        self.titleBox.bind('<ButtonRelease-1>', self.update)
        self.titleBox.pack()

        sb.config(command=self.titleBox.yview)

    # 设置窗口居中
    def center(self):
        width = 800
        height = 450

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int(screen_width / 2 - width / 2)
        y = int(screen_height / 2 - height / 2)
        size = '{}x{}+{}+{}'.format(width, height, x, y)

        self.root.geometry(size)

    # 载入数据
    def load(self):
        try:
            fp = open(self.filename, 'rb')
            self.info = pickle.load(fp)
        except:
            self.info = {}
        else:
            for key in self.info:
                self.titleBox.insert(END, key)

            if len(self.info) > 0:
                self.index = 0
                self.titleBox.activate(0)
                title = self.titleBox.get(0)

                self.Title.set(title)
                self.title.set(title)
                self.account.set(self.info[title]['account'])
                self.pwd.set(self.info[title]['pwd'])
                self.detail.set(self.info[title]['detail'])

    # 开启消息循环
    def loop(self):
        self.root.mainloop()

    # 退出前保存数据
    def save(self):
        with open(self.filename, 'wb') as fp:
            pickle.dump(self.info, fp)

    # 插入输入的内容
    def insert(self):
        title = self.title.get()

        # 检查标题
        if title == '':
            showwarning('错误', '标题不能为空！')
            return
        if title in self.titleBox.get(0, END):
            showwarning('错误', '标题不能重复！')
            return

        # 增加数据，通过 string var 用于修改列表项
        self.info[title] = {'account': self.account.get(), 'pwd': self.pwd.get(), 'detail': self.detail.get()}

        # 插入数据，同时激活数据
        self.titleBox.insert(END, title)
        self.titleBox.activate(END)

        self.Title.set(title)
        self.index = len(self.info) - 1

    # 提交修改的内容
    def commit(self):
        Title = self.Title.get()
        title = self.title.get()

        if title != '' and Title in self.titleBox.get(0, END):
            # 不允许改成与“其它”项重复的标题
            if title != Title and title in self.titleBox.get(0, END):
                showwarning('错误', '标题与其它项重复！')
                return
            
            if askyesno('提示', f'是否要覆盖 "{self.titleBox.get(self.index)}" 及其数据？'):
                self.info.pop(Title)
                self.Title.set(title)
                self.info[title] = {'account': self.account.get(), 'pwd': self.pwd.get(), 'detail': self.detail.get()}

                # 删除原先的数据，插入新数据
                self.titleBox.delete(self.index)
                self.titleBox.insert(self.index, title)

    # 删除锚定的项
    def delete(self):
        if self.index is not None and askyesno('提示', f'是否要删除 "{self.titleBox.get(self.index)}" 及其数据？'):
            title = self.titleBox.get(self.index)
            self.titleBox.delete(self.index)
            self.info.pop(title)

            self.index = None
            self.Title.set('无标题')

    # 获得当前锚定的项，从 info 中提取信息，更新输入框内容
    def update(self, event):
        title = self.titleBox.get(ANCHOR)

        if title == '':
            self.Title.set('无标题')
        else:
            info = self.info[title]

            self.title.set(title)
            self.account.set(info['account'])
            self.pwd.set(info['pwd'])
            self.detail.set(info['detail'])
            self.Title.set(title)

            # 获得选择的项的索引
            self.index = self.titleBox.curselection()[0]

        