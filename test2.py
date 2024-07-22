import numpy as np

np.set_printoptions(precision=2, suppress=True)
# 创建一个一维数组
arr = np.empty([1, 2])

# 在索引2的位置插入子数组[99, 100, 101]
new_arr = np.append(arr, np.array([99, 100]), axis=0)

print("原数组:", arr)
print("新数组:", new_arr)
