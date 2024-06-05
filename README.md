为了解拉格朗日函数并找到权重 ***ωj*** 的表达式，我们需要以下步骤：

### 1. 构造拉格朗日函数
我们构造的拉格朗日函数如下：

$$
L(\omega, \lambda) = \sum_{i=1}^m \sqrt{\sum_{j=1}^n \omega_j (x_{ij} - f_j^*)^2} + \lambda \left( \sum_{j=1}^n \omega_j - 1 \right)
$$


### 2. 对拉格朗日函数求导
为了找到最优权重w，我们需要对拉格朗日函数 ***L*** 关于 ***ωj*** 和 ***λ*** 求偏导数，并使这些导数等于零。

对 ***ωj*** 求偏导数：
$$
\frac{\partial L}{\partial \omega_j} = \frac{\partial}{\partial \omega_j} \left( \sum_{i=1}^m \sqrt{\sum_{j=1}^n \omega_j (x_{ij} - f_j^*)^2} + \lambda \left( \sum_{j=1}^n \omega_j - 1 \right) \right) = 0
$$
对 λ 求偏导数：

$$
\frac{\partial L}{\partial \lambda} = \sum_{j=1}^n \omega_j - 1 = 0
$$


### 3. 求解偏导数

$$
\frac{\partial L}{\partial \omega_j} = \sum_{i=1}^m \frac{(x_{ij} - f_j^*)^2}{2 \sqrt{\sum_{j=1}^n \omega_j (x_{ij} - f_j^*)^2}} + \lambda = 0
$$



### 4. 联立方程求解
我们得到的方程组为：

$$
\sum_{i=1}^m \frac{(x_{ij} - f_j^*)^2}{2 \sqrt{\sum_{j=1}^n \omega_j (x_{ij} - f_j^*)^2}} + \lambda = 0
$$

$$
\sum_{j=1}^n \omega_j = 1
$$



### 5. 具体求解方法
由于方程组复杂，通常使用数值方法求解。可以通过优化算法（如梯度下降、牛顿法等）进行求解。

### 示例代码
使用SciPy中的优化函数进行求解：

```python
import numpy as np
from scipy.optimize import minimize

def objective(weights, matrix, ideal):
    distances = np.sqrt(((matrix - ideal) ** 2 * weights).sum(axis=1))
    return distances.sum()

def constraint(weights):
    return np.sum(weights) - 1

matrix = np.array(
    [
        [1, 9, 8, 3],
        [5, 4, 2, 8],
        [9, 8, 7, 9],
        [4, 3, 5, 2],
        [6, 5, 9, 1],
        [7, 6, 3, 4],
        [2, 1, 6, 5],
        [3, 2, 1, 7],
        [8, 7, 4, 6],
    ]
)

norm_matrix = (matrix - matrix.min(axis=0)) / (matrix.max(axis=0) - matrix.min(axis=0))
ideal = norm_matrix.max(axis=0)
initial_weights = np.ones(matrix.shape[1]) / matrix.shape[1]

constraints = ({'type': 'eq', 'fun': constraint})
result = minimize(objective, initial_weights, args=(norm_matrix, ideal),
                  method='SLSQP', constraints=constraints, bounds=[(0, 1) for _ in range(matrix.shape[1])])

optimal_weights = result.x
print("最优权重:", optimal_weights)
```

通过这种方法，可以找到使每个方案到理想解的加权距离之和最小的权重 ***ωj*** 。在计算过程中，我们通过拉格朗日乘子法考虑了约束条件，最终求解了一个优化问题，从而得到了权重的具体表达式和数值解。