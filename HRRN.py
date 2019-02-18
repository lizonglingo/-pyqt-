# 最高响应比优先算法
from builtins import range, len, float


class Process:
    def __init__(self, name, arrive_time, serve_time, ready=False, over=False):
        self.name = name  # 进程名
        self.arrive_time = arrive_time  # 到达时间
        self.serve_time = serve_time  # 需要服务的时间
        self.left_serve_time = serve_time  # 剩余需要服务的时间
        self.finish_time = 0  # 完成时间
        self.cycling_time = 0  # 周转时间
        self.w_cycling_time = 0  # 带权周转时间
        self.response_ratio = 0
        self.pre_queue = 0  # 定义现在所在的队列
        self.pre_queue_tb = 0
        self.used_time = 0
        self.ready = ready
        self.over = over


class HRRN:
    def __init__(self, processes):
        self.sum_processes = processes

    def hrrn(self):
        pre_processes = []
        over_processes = []
        running_time = 0
        flag = 0
        pre_processes.append(self.sum_processes[0])
        while(flag!=len(self.sum_processes)):
            # 计算响应比
            for j in range(len(pre_processes)):
                pre_processes[j].response_ratio = (running_time - pre_processes[j].arrive_time + \
                                                pre_processes[j].serve_time) / pre_processes[j].serve_time
            # 找到响应比最大的进程
            max_rr = 0
            for i in range(len(pre_processes)):
                if pre_processes[i].response_ratio >= pre_processes[max_rr].response_ratio:
                    max_rr = i
            for i in range(pre_processes[max_rr].serve_time):
                running_time += 1
                for k in range(len(self.sum_processes)):  # 就绪队列入队
                    if self.sum_processes[k].arrive_time == running_time:
                        pre_processes.append(self.sum_processes[k])
            over_processes.append(pre_processes.pop(max_rr))
            flag += 1
        for i in range(len(over_processes)):
            print(over_processes[i].name)


if __name__ == '__main__':
    p1 = Process('A', 0, 3)
    p2 = Process('B', 2, 6)
    p3 = Process('C', 4, 4)
    p4 = Process('D', 6, 5)
    p5 = Process('E', 8, 2)

    processes = [p1, p2, p3, p4, p5]

    working = HRRN(processes)
    working.hrrn()