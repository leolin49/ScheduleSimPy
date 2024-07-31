Welcome to the CBC MILP Solver 
Version: 2.10.3 
Build Date: Dec 15 2019 

command line - /usr/local/lib/python3.9/site-packages/pulp/solverdir/cbc/linux/64/cbc /tmp/5737b52b37594046bec03e7d3763c576-pulp.mps -timeMode elapsed -branch -printingOptions all -solution /tmp/5737b52b37594046bec03e7d3763c576-pulp.sol (default strategy 1)
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
average completion time of dics: 2.265198446854634
baseline LRR is running...
now:10.648999999999537 1000 task is scheduled successfully.
now:20.617000000002214 2000 task is scheduled successfully.
now:30.748000000014596 3000 task is scheduled successfully.
now:41.206999999994665 4000 task is scheduled successfully.
now:51.929999999969674 5000 task is scheduled successfully.
now:62.05399999994608 6000 task is scheduled successfully.
now:71.47299999997722 7000 task is scheduled successfully.
now:81.90800000002704 8000 task is scheduled successfully.
now:91.8480000000745 9000 task is scheduled successfully.
average completion time of lrr: 2.260598845261257
PGCS is running...
1 id: 52, cpu: 16(25.00% used), mem: 120.0GB(25.00% used), disk: 1024.0GB(50.00% used), bandwidth: 100Mbps, running_task: 5, labels: Counter({'P100': 2})
3 id: 24, cpu: 96(25.00% used), mem: 768.0GB(25.00% used), disk: 1024.0GB(50.00% used), bandwidth: 100Mbps, running_task: 5, labels: Counter({'V100M32': 8})
2 id: 27, cpu: 96(25.00% used), mem: 384.0GB(25.00% used), disk: 1024.0GB(50.00% used), bandwidth: 100Mbps, running_task: 5, labels: Counter({'G2': 8})
First level group finish...
group_id: 1, second group keys: dict_keys(['P100', 'V100M16'])
group_id: 3, second group keys: dict_keys(['G3', 'V100M32'])
group_id: 2, second group keys: dict_keys(['G2', 'T4'])
Second level group finish...
now:7.703000000000907 1000 task is scheduled successfully.
now:14.083999999997634 2000 task is scheduled successfully.
now:20.845000000002493 3000 task is scheduled successfully.
now:27.753000000010935 4000 task is scheduled successfully.
now:34.52100000001025 5000 task is scheduled successfully.
now:41.763999999993366 6000 task is scheduled successfully.
now:48.52099999997762 7000 task is scheduled successfully.
now:55.331999999961745 8000 task is scheduled successfully.
now:62.063999999946056 9000 task is scheduled successfully.
now:68.51299999996309 10000 task is scheduled successfully.
now:75.4689999999963 11000 task is scheduled successfully.
now:82.3790000000293 12000 task is scheduled successfully.
now:89.13300000006154 13000 task is scheduled successfully.
now:95.71200000009296 14000 task is scheduled successfully.
average completion time: 2.2571434618058497
    {
        "timestamp": 104.60000000000095,
        "cluster_state": "cpu:25.00% mem:25.00% gpu:0.00% todo_num:0 finish_num:14620 total_num:16304"
    },
    {
        "avg_cpu_utilization:": "64.93%",
        "avg_mem_utilization:": "57.09%",
        "avg_gpu_utilization:": "51.63%"
    }
]    {
        "timestamp": 104.20000000000094,
        "cluster_state": "cpu:25.00% mem:25.00% gpu:0.00% todo_num:0 finish_num:478 total_num:16304"
    },
    {
        "avg_cpu_utilization:": "26.05%",
        "avg_mem_utilization:": "25.89%",
        "avg_gpu_utilization:": "1.30%"
    }
]