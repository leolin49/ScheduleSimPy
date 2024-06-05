# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/4/2 16:58
# Author  : linyf49@qq.com
# File    : test.py.py
import simpy


# 定义一个函数
def my_function(env):
    # 记录开始时间
    start_time = env.now

    # 这里是您的函数代码
    # 例如，这里我们模拟一些计算操作
    result = 0
    for i in range(1000000):
        result += i

    # 记录结束时间
    end_time = env.now

    # 计算函数执行时间
    execution_time = end_time - start_time
    print("Function execution time:", execution_time, "seconds")


# 创建SimPy环境
env = simpy.Environment()

# 启动仿真
env.process(my_function(env))

# 运行仿真，直到仿真时间达到5个时间单位
env.run(until=5)
