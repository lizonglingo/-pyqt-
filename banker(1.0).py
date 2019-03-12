# 表格添加，数据获取，存储测试
from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QTableWidget, QPushButton, QApplication, QDesktopWidget, \
    QVBoxLayout, QTableWidgetItem, QCheckBox, QAbstractItemView, QHeaderView, QLabel, QFrame
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from builtins import super, str, range
from PyQt5.QtGui import QFont
from builtins import range, len, int, str, super
from faker import Factory
import numpy as np
import sys, random


# ============================================ 算法部分 =====================================================#

# 安全性算法检查
def safeAlgorithm():
    # 安全性检查算法
    global safeList, system_security
    safeList = []

    work = Available
    Finish = [False] * length_progress

    # 在进程集合中找到一个 Finish[i] = false 且 need[i,j] < Work[j] 的进程
    while False in Finish:
        for i in range(0, length_progress):
            for j in range(0, length_Available):
                if (Finish[i] == False) and (Need[i] <= work).all():
                    for m in range(length_Available):
                        work[m] = work[m] + Allocation[i][m]
                    Finish[i] = True
                    safeList.append(i)
                else:
                    break

    # 如果所有进程的finish[i] = true 都满足，则表示系统处于安全状态；否则，系统处于不安全状态。
    if False in Finish:
        system_security = "不安全状态"
        print("*" * 45)
        print("您输入的请求资源数:{}".format(Request))
        print("您输入的请求进程是{}".format(Request_name))
        print("系统安全性：不安全状态")
        print("*" * 45)
    else:
        system_security = "系统安全"
        print("*" * 45)
        print("您输入的请求进程是{}".format(Request_name))
        print("您输入的请求资源数:{}".format(Request))
        print("系统安全性：系统安全")
        print("安全序列为：", safeList)
        print("*" * 45)


# 银行家算法的流程
def BankerAlgorithm():
    global Allocation, Available, Max, Need, safeList, Request, Request_name, system_security  # 注意均为全局变量
    if (Request <= Need[Request_name]).all():
        if (Request <= Available).all():  # vector.all()表示矩阵每一项都相等
            Available -= Request
            Need[Request_name] -= Request
            Allocation[Request_name] += Request
            safeAlgorithm()
        else:
            system_security = "请求超出可利用的资源，请等待"
            print("请求超出可利用的资源，请等待")
    else:
        system_security = "不合理请求"
        print("不合理请求")


# ================================================== 数据初始化 =======================================================#

# 初始化各数据结构
# 此处注意格式
# 可利用各资源总数
'''
Available = np.array([3, 3, 2])
length_Available = len(Available)
# 各进程最大需求资源数
Max = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
length_progress = len(Max)
print(length_Available)
# 已分配各进程的资源数
Allocation = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
# 各进程尚需的资源数
Need = np.array([[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]])
# 安全进程执行序列
safeList = []
# 各进程对各资源的请求
Request = []
# 进程名称
Request_name = ""
system_security = ""
'''
# 可利用资源
Available = np.array([0, 0, 0])
length_Available = len(Available)
# 各进程需要的最大资源数
Max = np.zeros((5, 3))
length_progress = len(Max)
print(length_Available)
# 已分配各进程的资源
Allocation = np.zeros((5, 3))
# 各进程尚需的资源
Need = Max - Allocation
# 安全进程执行序列
safeList = []
# 各进程对资源的请求
Request = []
# 进程名称
Request_name = ""
# 安全性状态
system_security = ""


# ================================================== 用户界面 =========================================================#

class ui(QWidget):
    def __init__(self):
        super(ui, self).__init__()
        self.setupUI()
        self.id = 1
        self.lines = []
        self.editable = True
        self.des_sort = True

        self.btn_add.clicked.connect(self.add_line)
        self.btn_del.clicked.connect(self.del_line)
        self.btn_modify.clicked.connect(self.modify_line)
        self.btn_set_middle.clicked.connect(self.middle)
        self.btn_safe_check.clicked.connect(self.function)
        self.table.cellChanged.connect(self.cellchange)

    #     # Sess = sessionmaker(bind = engine)

    def setupUI(self):
        self.setWindowTitle('银行家算法')
        self.resize(800, 420)

        self.table = QTableWidget(self)

        self.btn_add = QPushButton('增加')
        self.btn_del = QPushButton('删除')
        self.btn_modify = QPushButton('可以编辑')
        self.btn_set_middle = QPushButton('文字居中')
        self.btn_safe_check = QPushButton('安全性检查')

        # 弹簧控件
        self.spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        # 垂直布局，使用嵌套布局方式
        # 我们把所有按钮按照盒布局-垂直布局方式，构成嵌套布局的一个块
        # 按照设置的方式依此从上到下
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.btn_add)
        self.vbox.addWidget(self.btn_del)
        self.vbox.addWidget(self.btn_modify)
        self.vbox.addWidget(self.btn_set_middle)
        self.vbox.addWidget(self.btn_safe_check)
        self.vbox.addSpacerItem(self.spacerItem)

        self.vbox0 = QVBoxLayout()
        self.safe_list_zt = QLabel('安全状态：')
        self.safe_list_zt.setMinimumHeight(25)
        self.safe_list_zt.setMinimumWidth(50)
        self.safe_list_zt_edit = QLineEdit(self)
        self.safe_list_zt_edit.setMaximumWidth(300)
        self.vbox0.addWidget(self.safe_list_zt)
        self.vbox0.addWidget(self.safe_list_zt_edit)

        self.vbox1 = QVBoxLayout()
        self.safe_list = QLabel('安全序列：')
        self.safe_list.setMinimumHeight(25)
        self.safe_list.setMinimumWidth(50)
        self.safe_list_edit = QLineEdit(self)
        self.safe_list_edit.setMaximumWidth(300)
        self.vbox1.addWidget(self.safe_list)
        self.vbox1.addWidget(self.safe_list_edit)

        # 这是进行操作时显示在最左下角的提示信息
        self.txt = QLabel()
        # 限定控件大小
        self.txt.setMinimumHeight(25)

        self.lab_request_name = QLabel('请求进程序号（从0开始）：')
        self.lab_request_name.setMaximumWidth(200)
        self.lab_request_name.setMinimumHeight(25)
        self.lab_request_name_edit = QLineEdit(self)
        self.lab_request_name_edit.setMaximumWidth(30)

        self.lab_requesta = QLabel('请求资源A')
        self.lab_requesta.setMaximumWidth(60)
        self.lab_requesta.setMinimumHeight(25)
        self.requesta_edit = QLineEdit(self)
        self.requesta_edit.setMaximumWidth(100)

        self.lab_requestb = QLabel('请求资源B')
        self.lab_requestb.setMaximumWidth(60)
        self.lab_requestb.setMinimumHeight(25)
        self.requestb_edit = QLineEdit(self)
        self.requestb_edit.setMaximumWidth(100)

        self.lab_requestc = QLabel('请求资源C')
        self.lab_requestc.setMaximumWidth(60)
        self.lab_requestc.setMinimumHeight(25)
        self.requestc_edit = QLineEdit(self)
        self.requestc_edit.setMaximumWidth(100)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addWidget(self.lab_request_name)
        self.hbox2.addWidget(self.lab_request_name_edit)
        self.hbox2.addWidget(self.lab_requesta)
        self.hbox2.addWidget(self.requesta_edit)
        self.hbox2.addWidget(self.lab_requestb)
        self.hbox2.addWidget(self.requestb_edit)
        self.hbox2.addWidget(self.lab_requestc)
        self.hbox2.addWidget(self.requestc_edit)

        # 垂直布局
        # 把表格和下面的操作提示文本信息按照垂直布局设置，作为嵌套布局方式的另一部分
        self.vbox2 = QVBoxLayout()
        self.vbox2.addWidget(self.table)  # 将表格和下面的操作提示放入垂直布局，先放表格
        self.vbox2.addLayout(self.hbox2)
        self.vbox2.addLayout(self.vbox0)
        self.vbox2.addLayout(self.vbox1)
        self.vbox2.addWidget(self.txt)  # 再放文本框

        # 水平布局
        # 这是将上述两个布局方式作为整体布局的元素，vbox和vbox2共同放入水平布局
        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.vbox2)  # 将这样就会自左向右，先放表格
        self.hbox.addLayout(self.vbox)  # 再放按钮

        # 将水平布局放入总体布局
        self.setLayout(self.hbox)

        # 表格基本属性设置
        self.table.setColumnCount(15)  # 设置列数
        for i in range(15):
            self.table.setColumnWidth(i, 45)
        self.headers = ['id','选择', '进程', 'MA', 'MB', 'MC', 'AllA', 'AllB', 'AllC', 'NA', 'NB', 'NC', 'AvA', 'AvB',
                        'AvC']  # 设置每列标题
        self.table.setColumnHidden(0, True)  # 将第一列隐藏
        self.table.setHorizontalHeaderLabels(self.headers)  # 导入
        self.table.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.show()

    # 添加行
    def add_line(self):
        self.table.cellChanged.disconnect()
        row = self.table.rowCount()  # 获取目前所有行的数量
        self.table.setRowCount(row + 1)
        id = str(self.id)
        # 生成复选框， 并设置居中显示
        ck = QCheckBox()
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(ck)
        w = QWidget()
        w.setLayout(h)

        # 设置新建行的数据
        self.table.setCellWidget(row, 1, w)
        self.table.setItem(row, 0, QTableWidgetItem(id))
        info = [id, ck]
        self.table.setItem(row, 2, QTableWidgetItem(str(int(id)-1)))
        for i in range(3, 15):
            numb = str(0)
            info.append(numb)
            self.table.setItem(row, i, QTableWidgetItem(numb))
        self.id += 1  # 设置完不要忘记id加一
        self.lines.append(info)
        self.settext('自动生成随机一行数据！,checkbox设置为居中显示')
        self.table.cellChanged.connect(self.cellchange)

    # 删除行
    def del_line(self):
        removeline = []
        for line in self.lines:
            if line[1].isChecked():
                row = self.table.rowCount()
                for x in range(row, 0, -1):
                    if line[0] == self.table.item(x - 1, 0).text():
                        self.table.removeRow(x - 1)
                        removeline.append(line)
        for line in removeline:
            self.lines.remove(line)
        self.settext('删除在左边checkbox中选中的行，使用了一个笨办法取得行号\n，不知道有没有其他可以直接取得行号的方法！')

    def modify_line(self):
        if self.editable == True:
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.btn_modify.setText('禁止编辑')
            self.editable = False
        else:
            self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
            self.btn_modify.setText('可以编辑')
            self.editable = True
        self.settext('设置，是否可以编辑整个表格')

    def middle(self):
        row = self.table.rowCount()
        for x in range(row):
            for y in range(15):
                if y != 1:
                    item = self.table.item(x, y)
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    pass
        # self.btn_set_middle.setStyleSheet('background-color:lightblue')
        self.settext('将文字居中显示')  # 设置颜色按钮已被注释，这样不会再加颜色只是居中

    def cellchange(self, row, col):
        item = self.table.item(row, col)
        txt = item.text()
        self.settext('第%s行，第%s列 , 数据改变为:%s' % (row, col, txt))

    def settext(self, txt):
        font = QFont('微软雅黑', 10)
        self.txt.setFont(font)
        self.txt.setText(txt)

    # 获取屏幕信息并进行计算
    def function(self):
        global Request_name, Request, safeList, system_security, Need, Allocation, Max, Available, length_Available, length_progress
        Request_name = [int(self.lab_request_name_edit.text())]
        Request = np.array(
            [int(self.requesta_edit.text()), int(self.requestb_edit.text()), int(self.requestc_edit.text())])
        row = self.table.rowCount()

        Available[0] = int(self.table.item(0, 12).text())
        Available[1] = int(self.table.item(0, 13).text())
        Available[2] = int(self.table.item(0, 14).text())

        Max = np.zeros((row, 3))
        Allocation = np.zeros((row, 3))
        for r in range(row):
            for m in range(3):
                Max[r][m] = int(self.table.item(r, m + 3).text())
                Allocation[r][m] = int(self.table.item(r, m + 6).text())
        Need = Max - Allocation
        # 根据已有信息自动设置Need
        for i in range(row):
            for j in range(3):
                self.table.setItem(i, (j+9), QTableWidgetItem(str(int(Need[i][j]))))
        length_progress = len(Max)
        length_Available = len(Available)
        BankerAlgorithm()
        for k in range(row):
            self.table.setItem(row, 12, QTableWidgetItem(str(int(Available[0]))))
            self.table.setItem(row, 13, QTableWidgetItem(str(int(Available[1]))))
            self.table.setItem(row, 14, QTableWidgetItem(str(int(Available[2]))))

        self.safe_list_zt_edit.setText(system_security)
        self.safe_list_edit.setText(str(safeList))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ui()
    sys.exit(app.exec_())

