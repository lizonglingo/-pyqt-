# 最短剩余时间优先
import copy

# 声明数据结构
from builtins import range, len


class Process:
    def __init__(self, name, arrive_time, serve_time, ready = False, over=False):
        self.name = name  # 进程名
        self.arrive_time = arrive_time  # 到达时间
        self.serve_time = serve_time  # 需要服务的时间
        self.left_serve_time = serve_time  # 剩余需要服务的时间
        self.finish_time = 0  # 完成时间
        self.cycling_time = 0  # 周转时间
        self.w_cycling_time = 0  # 带权周转时间
        self.response_ratio = 0
        self.used_time = 0
        self.ready = ready
        self.over = over
        self.pre_queue = 0  # 定义现在所在的队列
        self.pre_queue_tb = 0



class SRTF:
    def __init__(self, processes_):
        self.processes = processes_

    def srtf(self):
        processes = self.processes
        flag = 0 # 记录已经处理完成的进程
        time = 0 # 模拟时间计数器
        current_process = -1 # 记录当前进程的下表，如果为-1表示当前没有进程在执行
        # 主循环，已经操作完成的进程数不为4
        while(flag != len(processes)):
            if current_process != -1:
                # 表示有进程正在执行
                processes[current_process].left_serve_time -= 1
                if processes[current_process].left_serve_time == 0:
                    print('进程' + processes[current_process].name + '处理完毕！')
                    flag += 1
                    processes[current_process].over = True
                    current_process = -1    # 需要重置为-1
            # 判断此时刻是否有新的新的进程进入就绪队列等待处理
            for i in range(len(processes)):
                if time == processes[i].arrive_time:
                    processes[i].ready = True
            # 寻找剩余时间最少的程序并进行调度
            min_time_remain = 100
            for i in range(len(processes)):
                if processes[i].ready == True and processes[i].over == False:
                    if (processes[i].left_serve_time) < min_time_remain:
                        min_time_remain = processes[i].left_serve_time
                        current_process = i   # 将剩余时间最短的进程置为当前进程
            time += 1 # 每次循环完time加一


if __name__ == '__main__':
    # 数据
    p1 = Process('A', 0, 3)
    p2 = Process('B', 2, 6)
    p3 = Process('C', 4, 4)
    p4 = Process('D', 6, 5)
    p5 = Process('E', 8, 2)

    processes = [p1, p2, p3, p4, p5]

    working = SRTF(processes)
    working.srtf()