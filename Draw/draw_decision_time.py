# Copyright 2024 The FCAV Authors. All rights reserved.
# Use of this source code is governed by a Apache2.0-style
# license that can be found in the LICENSE file.
#
# Time    : 2024/9/26 18:28
# Author  : linyf49@qq.com
# File    : draw_decision_time.py

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

import util

nodes = [100, 300, 500, 1000, 1500, 2000, 3000]

bra = [7.154e-05, 2.134e-04, 3.317e-04, 6.647e-04, 1.010e-03, 1.364e-03, 2.055e-03]
lrp = [4.507e-05, 1.283e-04, 2.058e-04, 4.041e-04, 6.518e-04, 8.239e-04, 1.264e-03]
dics = [9.912e-04, 2.935e-03, 4.879e-03, 9.986e-03, 1.552e-02, 2.158e-02, 3.520e-02]
kcss = [1.401e-03, 4.152e-03, 6.876e-03, 1.423e-02, 2.120e-02, 3.027e-02, 4.637e-02]
odcs = [2.545e-04, 7.400e-04, 1.236e-03, 2.588e-03, 3.679e-03, 5.011e-03, 7.452e-03]
rccs = [1.181e-04, 3.326e-04, 3.697e-04, 6.769e-04, 1.138e-03, 1.163e-03, 2.083e-03]

plt.figure(figsize=(10, 6))

marker = "*"
marker_size = 15
idx = 6
lw = 3

plt.plot(
    nodes[:idx],
    bra[:idx],
    marker=".",
    ms=marker_size,
    label="BRA",
    c=util.BASELINE_COLORS[0],
    linewidth=lw,
)
plt.plot(
    nodes[:idx],
    lrp[:idx],
    marker="v",
    ms=marker_size,
    label="LRP",
    c=util.BASELINE_COLORS[1],
    linewidth=lw,
)
plt.plot(
    nodes[:idx],
    dics[:idx],
    marker="^",
    ms=marker_size,
    label="DICS",
    c=util.BASELINE_COLORS[2],
    linewidth=lw,
)
plt.plot(
    nodes[:idx],
    kcss[:idx],
    marker="h",
    ms=marker_size,
    label="KCSS",
    c=util.BASELINE_COLORS[3],
    linewidth=lw,
)
plt.plot(
    nodes[:idx],
    odcs[:idx],
    marker="*",
    ms=marker_size,
    label="ODCS",
    c=util.BASELINE_COLORS[4],
    linewidth=lw,
)
plt.plot(
    nodes[:idx],
    rccs[:idx],
    marker="d",
    ms=marker_size,
    label="RCCS",
    c=util.BASELINE_COLORS[5],
    linewidth=lw,
)

# plt.title('Execution Time Trends for Different Baselines')
fz = 20
plt.xlabel("Number of nodes", fontsize=fz)
plt.yscale("log")
plt.ylabel("Execution Time (log scale, base 10)", fontsize=fz)
plt.xticks(fontsize=fz - 4)
plt.yticks(fontsize=fz - 4)


# 设置y轴为科学计数法
formatter = ScalarFormatter(useOffset=False)
formatter.set_scientific(True)
formatter.set_powerlimits((-1, 1))
plt.gca().yaxis.set_major_formatter(formatter)

# 添加图例
plt.legend(loc="lower right", fontsize=20, ncol=3)

plt.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95)

# 显示图表
plt.grid(True)
plt.show()
