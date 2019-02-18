# 先到先处理和静态优先权优先
from builtins import range, len, max, min


# 定义数据结构
class Process:
    def __init__(self, name, arrive_time, serve_time, static_class=0, ready=False, over=False):
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
        self.static_class = static_class


class FCFS:
    def __init__(self, processes_):
        self.processes = processes_


    def fcfs(self): # 到达时间小的优先
        processes = self.processes
        # 新建输出队列
        over_list = []
        min_key = 0
        while processes:
            for i in range(len(processes)):
                min = processes[0].arrive_time
                if processes[i].arrive_time <= min:
                    min = processes[i].arrive_time
                    min_key = i

            over_list.append(processes.pop(min_key))
        for i in range(len(over_list)):
            print(over_list[i].name)


class SCF:
    def __init__(self, processes_):
        self.processes = processes_

    def scf(self): # 静态优先级高的优先，人为赋予
        # 新建输出队列
        processes = self.processes
        over_list = []
        while processes:
            max = processes[0].static_class
            max_key = 0
            for i in range(len(processes)):
                if processes[i].static_class > max:
                    max = processes[i].static_class
                    max_key = i
            over_list.append(processes.pop(max_key))
        for i in range(len(over_list)):
            print(over_list[i].name)


if __name__=='__main__':
    # 定义进程结构
    # 数据
    p1 = Process('A', 0, 3, 4)
    p2 = Process('B', 2, 6, 2)
    p3 = Process('C', 4, 4, 1)
    p4 = Process('D', 6, 5, 5)
    p5 = Process('E', 8, 2, 3)

    processes = [p1, p2, p3, p4, p5]
    processes_ = processes[:]

    working = FCFS(processes)
    working.fcfs()

    working_ = SCF(processes_)
    working_.scf()

