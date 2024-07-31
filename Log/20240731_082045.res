Welcome to the CBC MILP Solver 
Version: 2.10.3 
Build Date: Dec 15 2019 

command line - /usr/local/lib/python3.9/site-packages/pulp/solverdir/cbc/linux/64/cbc /tmp/f299aea7fe6e4013899f1ce46e4b0ca1-pulp.mps -timeMode elapsed -branch -printingOptions all -solution /tmp/f299aea7fe6e4013899f1ce46e4b0ca1-pulp.sol (default strategy 1)
At line 2 NAME          MODEL
At line 3 ROWS
At line 16 COLUMNS
At line 52 RHS
At line 64 BOUNDS
At line 65 ENDATA
Problem MODEL has 11 rows, 5 columns and 34 elements
Coin0008I MODEL read with 0 errors
Option for timeMode changed from cpu to elapsed
Presolve 11 (0) rows, 5 (0) columns and 34 (0) elements
0  Obj 0 Primal inf 0.9999999 (1)
7  Obj 0.045454545
Optimal - objective value 0.045454545
Optimal objective 0.04545454545 - 7 iterations time 0.002
Option for printingOptions changed from normal to all
Total time (CPU seconds):       0.00   (Wallclock seconds):       0.00

task data read finish.
node data read finish.
baseline DICS is running...
average completion time of dics: 2.371392460954238
baseline LRR is running...
now:10.694999999999512 1000 task is scheduled successfully.
now:20.722000000002343 2000 task is scheduled successfully.
now:30.64400000001447 3000 task is scheduled successfully.
now:40.68099999999589 4000 task is scheduled successfully.
now:50.881999999972116 5000 task is scheduled successfully.
now:61.196999999948076 6000 task is scheduled successfully.
now:71.89599999997924 7000 task is scheduled successfully.
now:82.0880000000279 8000 task is scheduled successfully.
now:92.15800000007599 9000 task is scheduled successfully.
average completion time of lrr: 2.2775390500283397
PGCS is running...
Best-Worst Method Weights =  [0.5  0.27 0.14 0.09]
1 id: 52, cpu: 16(25.00% used), mem: 120.0GB(25.00% used), disk: 1024.0GB(50.00% used), bandwidth: 100Mbps, running_task: 5, labels: Counter({'P100': 2})
3 id: 24, cpu: 96(25.00% used), mem: 768.0GB(25.00% used), disk: 1024.0GB(50.00% used), bandwidth: 100Mbps, running_task: 5, labels: Counter({'V100M32': 8})
2 id: 27, cpu: 96(25.00% used), mem: 384.0GB(25.00% used), disk: 1024.0GB(50.00% used), bandwidth: 100Mbps, running_task: 5, labels: Counter({'G2': 8})
First level group finish...
group_id: 1, second group keys: dict_keys(['P100', 'V100M16'])
group_id: 3, second group keys: dict_keys(['G3', 'V100M32'])
group_id: 2, second group keys: dict_keys(['G2', 'T4'])
Second level group finish...
now:7.639000000000886 1000 task is scheduled successfully.
now:14.331999999997496 2000 task is scheduled successfully.
now:21.085000000002786 3000 task is scheduled successfully.
now:27.806000000011 4000 task is scheduled successfully.
now:34.65300000000994 5000 task is scheduled successfully.
now:41.08399999999495 6000 task is scheduled successfully.
now:48.285999999978166 7000 task is scheduled successfully.
now:55.14899999996217 8000 task is scheduled successfully.
now:61.88499999994647 9000 task is scheduled successfully.
now:68.84799999996469 10000 task is scheduled successfully.
now:75.73399999999756 11000 task is scheduled successfully.
now:82.40300000002941 12000 task is scheduled successfully.
now:89.27900000006224 13000 task is scheduled successfully.
now:96.1620000000951 14000 task is scheduled successfully.
average completion time: 2.283078014769963
    {
        "timestamp": 104.60000000000095,
        "cluster_state": "cpu:25.00% mem:25.00% gpu:0.00% todo_num:0 finish_num:14587 total_num:16304"
    },
    {
        "avg_cpu_utilization:": "65.37%",
        "avg_mem_utilization:": "57.41%",
        "avg_gpu_utilization:": "51.94%"
    }
]    {
        "timestamp": 102.60000000000092,
        "cluster_state": "cpu:25.00% mem:25.00% gpu:0.00% todo_num:0 finish_num:449 total_num:16304"
    },
    {
        "avg_cpu_utilization:": "26.11%",
        "avg_mem_utilization:": "25.96%",
        "avg_gpu_utilization:": "1.37%"
    }
]