# 表格添加，数据获取，存储测试
from PyQt5.QtWidgets import QWidget,QLineEdit,QHBoxLayout,QTableWidget,QPushButton,QApplication,QVBoxLayout,QTableWidgetItem,QCheckBox,QAbstractItemView,QHeaderView,QLabel,QFrame
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from builtins import super, str, range
from PyQt5.QtGui import QFont,QColor
from faker import Factory
import random, sys, operator

#  引入数据结构
# 定义每个进程基本数据结构
class Process:
    def __init__(self, name, arrive_time, serve_time, static_class, ready=False, over=False):
        self.name = name                                    # 进程名称
        self.arrive_time = arrive_time                      # 到达时间
        self.serve_time = serve_time                        # 服务时间
        self.left_serve_time = serve_time                   # 剩余需要服务的时间
        self.finish_time = 0                                # 完成时间
        self.cycling_time = 0                               # 周转时间
        self.w_cycling_time = 0                             # 带权周转时间
        self.response_ratio = 0                             # 响应比
        self.pre_queue = 0                                  # 定义现在所在的队列
        self.pre_queue_tb = 0                               # 目前所在队列的时间片
        self.used_time = 0                                  # 已经使用的时间，也就是（服务时间 - 剩余服务时间）
        self.ready = ready                                  # 记录就绪状态
        self.over = over                                    # 记录完成状态
        self.static_class = static_class                    # 人为赋予静态优先级


def rr(processes_, time_block_):
    
    sum_cycling_time = 0
    sum_w_cycling_time = 0
    name_string = ''
    time_string = '平均周转时间：'
    number = len(processes_)
    last_info = []


    processes = processes_
    pre_processes = []    # running_time等于进程到达时间时会将其入队
    over_processes = []  # 完成队列
    flag = 0 # 记录完成的进程数
    running_time = 0
    time_block = time_block_
    pre_processes.append(processes[0]) # 先将第一个进程入队


    while(flag != len(processes)):
            # 是否进程入队的优先级高于进程从队首切换到队尾的优先级？
            # 执行当前队首进程，如果一个时间片内不能执行完，则放入队列尾部

            # 判断时间片是否大于剩余服务时间
            if time_block >= pre_processes[0].left_serve_time:
                for i in range(pre_processes[0].left_serve_time):
                    pre_processes[0].left_serve_time -= 1
                    running_time += 1

                    for i in range(len(processes)):
                        if running_time == processes[i].arrive_time:
                            pre_processes.append(processes[i])  # 就绪队列进入队尾

                    if pre_processes[0].left_serve_time == 0:
                        # 计算完成时间
                        pre_processes[0].finish_time = running_time
                        # 计算周转时间
                        pre_processes[0].cycling_time = pre_processes[0].finish_time \
                                                                    - pre_processes[0].arrive_time
                        sum_cycling_time += pre_processes[0].cycling_time
                        # 计算带权周转时间
                        pre_processes[0].w_cycling_time = float(pre_processes[0].cycling_time) / \
                                                                      pre_processes[0].serve_time
                        sum_w_cycling_time += pre_processes[0].w_cycling_time
                        # 打印
                        name_string += (pre_processes[0].name + '   ')
                        print('%s 进程已完成的进程，详细信息如下：' % pre_processes[0].name)
                        print('进程名称：%s  ，完成时间： %d    ，周转时间：%d  ，带权周转时间： %.2f' % (
                                        pre_processes[0].name, pre_processes[0].finish_time,
                                        pre_processes[0].cycling_time, pre_processes[0].w_cycling_time))

                flag += 1
                over_processes.append(pre_processes.pop(0))  # 进程结束从就绪队列出队进完成队列
                continue   # 直接结束此次循环，下面内容不执行
            else: # 剩余服务时间大于一个时间片
                for i in range(time_block):
                    pre_processes[0].left_serve_time -= 1
                    running_time += 1

                    for i in range(len(processes)):  # 判断此时有没有就绪队列加入队尾
                        if running_time == processes[i].arrive_time:
                            pre_processes.append(processes[i])

                # 一个时间片结束进程从队头切换至队尾
                pre_processes.append(pre_processes.pop(0))

    a_c_time = sum_cycling_time / number
    a_w_c_time = sum_w_cycling_time / number
    time_string += (str(a_c_time) + '    平均带权周转时间：' + str(a_w_c_time))

    last_info.append(name_string)
    last_info.append(time_string)

    return last_info




class ui(QWidget):
    def __init__(self):
        super(ui, self).__init__()
        self.setupUI()
        self.id = 1
        self.lines = []
        self.editable = True
        self.des_sort = True
        self.faker = Factory.create()

        self.btn_add.clicked.connect(self.add_line)
        self.btn_del.clicked.connect(self.del_line)
        self.btn_modify.clicked.connect(self.modify_line)
        self.btn_set_middle.clicked.connect(self.middle)
        self.btn_get_info.clicked.connect(self.g_info)

        self.table.cellChanged.connect(self.cellchange)

        global original_processes                           # 这里我们定义全局变量 - 原始进程列表，是一个二维列表


    def setupUI(self):
        self.setWindowTitle('数据测试')
        self.resize(720,420)

        self.table = QTableWidget(self)

        self.btn_add = QPushButton('增加')
        self.btn_del = QPushButton('删除')
        self.btn_modify = QPushButton('可以编辑')
        self.btn_set_middle = QPushButton('文字居中')
        self.btn_get_info = QPushButton('生成调度序列')
    
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
        self.vbox.addWidget(self.btn_get_info)
        self.vbox.addSpacerItem(self.spacerItem)            
        
        self.txt = QLabel()                             # 这是进行操作时显示在最左下角的提示信息
        self.txt.setMinimumHeight(50)                   # 限定控件大小

        self.hbox1 = QHBoxLayout()
        self.lab_time_block = QLabel('时间片大小：')
        self.lab_time_block.setMaximumWidth(300)
        self.time_block_edit = QLineEdit(self)
        self.time_block_edit.setMaximumWidth(100)
        self.hbox1.addWidget(self.lab_time_block)
        self.hbox1.addWidget(self.time_block_edit)
        

        self.lab_over = QLabel('调度顺序')               # 输出队列顺序
        self.lab_over.setMinimumHeight(20)
        self.over_Edit = QLineEdit(self)
        self.over_Edit.setMinimumHeight(25)

        self.lab_time = QLabel('平均周转时间和平均带权周转时间')
        self.avrtime_edit = QLineEdit(self)

        # 垂直布局
        # 把表格和下面的操作提示文本信息按照垂直布局设置，作为嵌套布局方式的另一部分
        self.vbox2 = QVBoxLayout()                         
        self.vbox2.addWidget(self.table)                    # 将表格和下面的操作提示放入垂直布局，先放表格
        self.vbox2.addLayout(self.hbox1) 
        self.vbox2.addWidget(self.lab_over)                 # 放输出队列
        self.vbox2.addWidget(self.over_Edit)
        self.vbox2.addWidget(self.lab_time)
        self.vbox2.addWidget(self.avrtime_edit)

        self.vbox2.addWidget(self.txt)                      # 再放文本框

        # 水平布局
        # 这是将上述两个布局方式作为整体布局的元素，vbox和vbox2共同放入水平布局
        self.hbox = QHBoxLayout()                          
        self.hbox.addLayout(self.vbox2)                     # 将这样就会自左向右，先放表格，
        self.hbox.addLayout(self.vbox)                      # 再放按钮

        # 将水平布局放入总体布局
        self.setLayout(self.hbox)

        # 表格基本属性设置   
        self.table.setColumnCount(6)                                    # 设置列数
        self.table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignCenter)
        self.headers = ['ID','选择','进程名', '到达时间', '服务时间', '静态优先级']      # 设置每列标题
        self.table.setHorizontalHeaderLabels(self.headers)              # 导入
        self.table.verticalHeader().setVisible(False)                   # 隐藏垂直表头
        self.show()

    # 添加行
    def add_line(self):
        self.table.cellChanged.disconnect()
        row = self.table.rowCount()                                     # 获取目前所有行的数量
        self.table.setRowCount(row + 1)
        id = str(self.id)

        # 生成复选框， 并设置居中显示
        ck = QCheckBox()
        h = QHBoxLayout()
        h.setAlignment(Qt.AlignCenter)
        h.addWidget(ck)
        w = QWidget()
        w.setLayout(h)

        # 变量由faker自动生成
        name = self.faker.name()
        arr_time = str(random.randint(0,9))
        ser_time = str(random.randint(0,9))
        sta_class = str(random.randint(0,9))

        # 设置新建行的数据
        self.table.setItem(row,0,QTableWidgetItem(id))
        self.table.setCellWidget(row,1,w)
        self.table.setItem(row,2,QTableWidgetItem(name))
        self.table.setItem(row,3,QTableWidgetItem(arr_time))
        self.table.setItem(row,4,QTableWidgetItem(ser_time))
        self.table.setItem(row,5,QTableWidgetItem(sta_class))

        self.id += 1                                                        # 设置完不要忘记id加一
        self.lines.append([id,ck,name,arr_time,ser_time,sta_class])
        self.settext('自动生成随机一行数据！,checkbox设置为居中显示')
        self.table.cellChanged.connect(self.cellchange)

    # 删除行
    def del_line(self):
        removeline = []
        for line in self.lines:
            if line[1].isChecked():
                row = self.table.rowCount()
                for x in range(row,0,-1):
                    if line[0] == self.table.item(x - 1,0).text():
                        self.table.removeRow(x - 1)
                        removeline.append(line)
        for line in removeline:
            self.lines.remove(line)
        self.settext('删除checkbox中选中状态的行')

    def modify_line(self):
        if self.editable == True:
            self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.btn_modify.setText('禁止编辑')
            self.editable = False
        else:
            self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
            self.btn_modify.setText('可以编辑')
            self.editable = True
        self.settext('设置是否可以编辑表格信息')

    def middle(self):
        row = self.table.rowCount()
        for x in range(row):
            for y in range(6):
                if y != 1:
                    item = self.table.item(x,y)
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    pass
        self.settext('将文字居中显示')  

    def cellchange(self,row,col):
        item = self.table.item(row,col)
        txt = item.text()
        self.settext('第%s行，第%s列 , 数据改变为:%s'%(row,col,txt))

    def g_info(self):
        # 我们每次使用这个功能时先把全变量原始进程列表 -- original_processes --清空好吧
        original_processes = []
        row = self.table.rowCount()

        for j in range(row):                            # 有几行就有几个进程
            na = self.table.item(j,2).text()
            at = int(self.table.item(j,3).text())
            st = int(self.table.item(j,4).text())
            sc = int(self.table.item(j,5).text())
            p = Process(na, at, st, sc)
            original_processes.append(p)
            print(na+' '+str(at)+' '+str(st)+' '+str(sc))
       
        '''
        由于第一个进程不一定就是到达时间最小的进程，所以
        我们先按照到达时间排个序
        '''
        _sorted_processes = original_processes[:]
        _sorted_processes.sort(key=operator.attrgetter('arrive_time'))

        t_b = int(self.time_block_edit.text()) 

        infor_list = rr(_sorted_processes, t_b)
        self.avrtime_edit.setText(str(infor_list[1]))
        self.over_Edit.setText(str(infor_list[0]))
        self.settext('获取表格信息，生成调度序列，计算平均、平均带权周转时间，并显示')
    
    def settext(self,txt):
        font = QFont('微软雅黑',10)
        self.txt.setFont(font)
        self.txt.setText(txt)  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ui()
    sys.exit(app.exec_())