# 时间片轮转
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
        self.used_time = 0
        self.ready = ready
        self.over = over
        self.pre_queue = 0  # 定义现在所在的队列
        self.pre_queue_tb = 0

class RR:
    def __init__(self, processes, time_block, running_time = 0):
        self.processes = processes
        self.time_block = time_block
        self.running_time = running_time

    def rr(self):
        pre_processes = []    # running_time等于进程到达时间时会将其入队
        over_processes = []  # 完成队列
        flag = 0 # 记录完成的进程数
        running_time = self.running_time
        time_block = self.time_block
        pre_processes.append(self.processes[0]) # 先将第一个进程入队


        while(flag != len(self.processes)):
                # 是否进程入队的优先级高于进程从队首切换到队尾的优先级？
                # 执行当前队首进程，如果一个时间片内不能执行完，则放入队列尾部

                # 判断时间片是否大于剩余服务时间
                if time_block >= pre_processes[0].left_serve_time:
                    for i in range(pre_processes[0].left_serve_time):
                        pre_processes[0].left_serve_time -= 1
                        running_time += 1

                        for i in range(len(self.processes)):
                            if running_time == self.processes[i].arrive_time:
                                pre_processes.append(self.processes[i])  # 就绪队列进入队尾

                        if pre_processes[0].left_serve_time == 0:
                            # 计算完成时间
                            pre_processes[0].finish_time = running_time
                            # 计算周转时间
                            pre_processes[0].cycling_time = pre_processes[0].finish_time \
                                                                    - pre_processes[0].arrive_time
                            # 计算带权周转时间
                            pre_processes[0].w_cycling_time = float(pre_processes[0].cycling_time) / \
                                                                      pre_processes[0].serve_time
                            # 打印
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

                        for i in range(len(self.processes)):  # 判断此时有没有就绪队列加入队尾
                            if running_time == self.processes[i].arrive_time:
                                 pre_processes.append(self.processes[i])

                    # 一个时间片结束进程从队头切换至队尾
                    pre_processes.append(pre_processes.pop(0))


if __name__ == '__main__':
    p1 = Process('A', 0, 3)
    p2 = Process('B', 2, 6)
    p3 = Process('C', 4, 4)
    p4 = Process('D', 6, 5)
    p5 = Process('E', 8, 2)
    processes = [p1, p2, p3, p4, p5]
    working = RR(processes, 1)
    working.rr()

