# 短作业优先
from builtins import len, min, max, range


# 定义数据结构
class Process:
    def __init__(self, name, arrive_time, serve_time, ready=False, over=False):
        self.name = name
        self.arrive_time = arrive_time
        self.handle_time = serve_time
        self.left_serve_time = serve_time  # 剩余需要服务的时间
        self.finish_time = 0  # 完成时间
        self.cycling_time = 0  # 周转时间
        self.w_cycling_time = 0  # 带权周转时间
        self.response_ratio = 0 # 响应比
        self.pre_queue = 0  # 定义现在所在的队列
        self.pre_queue_tb = 0
        self.used_time = 0
        self.ready = ready
        self.over = over


class SPF:
    def __init__(self, processes_):
        self.processes = processes_

    def spf(self):
        processes = self.processes
        flag = 0 # 记录已完成的进程数量
        time = 0 # 模拟时钟技术
        current_process = -1 # 记录当前正在执行的进程下标

        while(flag!=5):
            if current_process != -1:  # 此时有进程在执行
                processes[current_process].used_time += 1
                if processes[current_process].used_time == processes[current_process].handle_time:
                    print('进程' + processes[current_process].name + '处理完毕！')
                    flag += 1
                    processes[current_process].over = True
                    # current_process = -1
            for i in range(len(processes)):
                if time == processes[i].arrive_time:
                    processes[i].ready = True
            min_handle = 100
            for i in range(len(processes)):
                if processes[i].ready == True and processes[i].over == False:
                    if current_process == -1:
                        min_handle = processes[0].handle_time
                        current_process = 0
                    else:
                        if processes[current_process].over == True:
                            for i in range(len(processes)):
                                if processes[i].ready == True and processes[i].over == False:
                                    if  processes[i].handle_time <= min_handle:
                                        current_process = i
                                        min_handle = processes[i].handle_time
            time += 1


if __name__ == '__main__':
    # 数据
    p1 = Process('A', 0, 3)
    p2 = Process('B', 2, 6)
    p3 = Process('C', 4, 4)
    p4 = Process('D', 6, 5)
    p5 = Process('E', 8, 2)

    processes = [p1, p2, p3, p4, p5]

    working = SPF(processes)
    working.spf()