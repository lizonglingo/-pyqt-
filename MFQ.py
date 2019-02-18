# 多级反馈队列调度算法
from builtins import range, len, float


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
        self.pre_queue = 0  # 定义现在所在的队列
        self.pre_queue_tb = 0
        self.used_time = 0
        self.ready = ready
        self.over = over

class MFQ:
    def __init__(self, processes, class_time_block):
        self.processes = processes # 这是就绪以及未就绪的所有队列
        self.class_time_block = class_time_block  # 时间递增量级

    def mfq(self):
        sum_processes = self.processes
        # 我们这里使用三队列，将到达的队列放入
        f_processes = []
        s_processes = []
        t_processes = []
        # 规定每个队列的时间片，这里我们直接计算
        f_time_block = 1
        s_time_block = 2
        t_time_block = 4
        flag = 0 # 完成进程计数
        running_time = 0 # 时钟模拟
        processes_number = len(sum_processes)
        current_process = -1 # 当前进行进程，如果没有置为-1
        f_processes.append(sum_processes[0])
        while(flag != processes_number):
                # 判断在哪一个队列进行操作,选择当前要处理的进程
                if f_processes:
                    current_process = f_processes[0]
                    current_process.pre_queue_tb = 1
                    current_process.pre_queue = 1
                elif s_processes:
                    current_process = s_processes[0]
                    current_process.pre_queue = 2
                    current_process.pre_queue_tb = 2
                elif t_processes:
                    # 轮转法，重写
                    pre_processes = t_processes
                    sum = len(t_processes)
                    over_processes = []  # 完成队列
                    t_flag = 0  # 记录完成的进程数
                    # running_time = running_time
                    time_block = 4
                    while (t_flag != sum):
                        # 是否进程入队的优先级高于进程从队首切换到队尾的优先级？
                        # 执行当前队首进程，如果一个时间片内不能执行完，则放入队列尾部
                        # 判断时间片是否大于剩余服务时间
                        if time_block >= pre_processes[0].left_serve_time:
                            for i in range(pre_processes[0].left_serve_time):
                                pre_processes[0].left_serve_time -= 1
                                running_time += 1
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
                            t_flag += 1
                            over_processes.append(pre_processes.pop(0))  # 进程结束从就绪队列出队进完成队列
                            continue  # 直接结束此次循环，下面内容不执行
                        else:  # 剩余服务时间大于一个时间片
                            for i in range(time_block):
                                pre_processes[0].left_serve_time -= 1
                                running_time += 1
                            # 一个时间片结束进程从队头切换至队尾
                            pre_processes.append(pre_processes.pop(0))
                    break
                # 在一个时间片内操作
                for i in range(current_process.pre_queue_tb):
                    current_process.left_serve_time -= 1
                    running_time += 1
                    out_ = 0
                    # 判断此时是否完成
                    if current_process.left_serve_time == 0:
                        # 如果完成，弹出
                        # 计算完成时间
                        current_process.finish_time = running_time
                        # 计算周转时间
                        current_process.cycling_time = current_process.finish_time \
                                                        - current_process.arrive_time
                        # 计算带权周转时间
                        current_process.w_cycling_time = float(current_process.cycling_time) / \
                                                          current_process.serve_time
                        # 打印
                        print('%s 进程已完成的进程，详细信息如下：' % current_process.name)
                        print('进程名称：%s  ，完成时间： %d    ，周转时间：%d  ，带权周转时间： %.2f' % (
                            current_process.name, current_process.finish_time,
                            current_process.cycling_time, current_process.w_cycling_time))
                        flag += 1
                        if current_process.pre_queue == 1:
                            f_processes.pop(0)
                        elif current_process.pre_queue == 2:
                            s_processes.pop(0)
                        else:
                            t_processes.pop(0)
                        current_process = -1
                        out_ = 1
                    elif i == current_process.pre_queue_tb-1 and current_process.left_serve_time != 0:
                        # 一个时间片内未完成，进入下一队列
                        if current_process.pre_queue == 1:
                            current_process.pre_queue = 2
                            current_process.pre_queue_tb = 2
                            s_processes.append(f_processes.pop(0))
                        elif current_process.pre_queue == 2:
                            current_process.pre_queue = 3
                            current_process.pre_queue_tb = 4
                            t_processes.append(s_processes.pop(0))
                    # 判断此时有没有新进程入队，如果有，入队退出循环
                    for j in range(len(sum_processes)):
                        if running_time == sum_processes[j].arrive_time:
                            # 如果有新就绪队列
                            out = 1
                            # 判断当前是否有正在进行的进程
                            if current_process != -1:
                                # 如果1队不空，加入一队
                                if f_processes:
                                    sum_processes[j].pre_queue = 1
                                    sum_processes[j].pre_queue_tb = 1
                                    f_processes.append(sum_processes[j])
                                    break
                                else: # 如果一队空
                                    if current_process.pre_queue == 2:
                                        s_processes.append(s_processes.pop(0))
                                    elif current_process.pre_queue == 3:
                                        t_processes.append(t_processes.pop(0))
                                    current_process = sum_processes[j]
                                    current_process.pre_queue = 1
                                    current_process.pre_queue_tb = 1
                                    f_processes.append(current_process)
                                    break
                                    # 将此时进入进程置为当前处理的进程
                            else:
                                # 如果没有，直接将新入队进程置为当前进程
                                sum_processes[j].pre_queue = 1
                                sum_processes[j].pre_queue_tb = 1
                                current_process = sum_processes[j]
                                f_processes.append(current_process)
                                break
                        else:
                            out = 0
                    if out == 1 or out_ == 1:
                        break


if __name__ == '__main__':
    p1 = Process('A', 0, 3)
    p2 = Process('B', 2, 6)
    p3 = Process('C', 4, 4)
    p4 = Process('D', 6, 5)
    p5 = Process('E', 8, 2)

    processes = [p1, p2, p3, p4, p5]

    working = MFQ(processes, 2)
    working.mfq()

