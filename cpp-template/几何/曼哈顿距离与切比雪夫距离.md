---
topic: "曼哈顿距离 & 切比雪夫距离"
category: "06-geometry"
source: "几何 Geometry.md"
---

# 曼哈顿距离 & 切比雪夫距离

- **曼哈顿距离**：只能走直线（网格），距离是 $|x_1 - x_2| + |y_1 - y_2|$

- **切比雪夫距离**：可以走斜线（八向），距离是 $\max(|x_1 - x_2|, |y_1 - y_2|)$

它们之间的代数恒等式：

$$\max(|a|, |b|) = \frac{|a+b| + |a-b|}{2}$$

如果把 $a$ 当作两点的横坐标差 $(x_1 - x_2)$，把 $b$ 当作纵坐标差 $(y_1 - y_2)$，代入上面的公式

* ***切比雪夫距离就成了全新的曼哈顿距离。**

* ***曼哈顿距离的巨大优势：X 和 Y 可以完全独立排序、独立计算**

### 相互转化：

原坐标系中所有的点 $(x, y)$，全部映射为新坐标系中的点 **$(x+y, x-y)$**。

原坐标系中任意两点的**切比雪夫距离**，就等于新坐标系中对应两点的**曼哈顿距离的一半**

给定二维平面上的 $N$ 个点，求这 $N$ 个点之间，两两组成的 $\frac{N(N-1)}{2}$ 对点的**切比雪夫距离之和**

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// 输入一个升序排序好的数组，返回所有两点间的绝对值差之和
long long calc_1D_distance_sum(const vector<long long>& arr) {
    long long sum = 0;
    long long current_prefix_sum = 0;
    long long n = arr.size();
    for (long long i = 0; i < n; ++i) {
        sum += i * arr[i] - current_prefix_sum;
        current_prefix_sum += arr[i];
    }
    return sum;
}

int main() {
    int n;
    if (!(cin >> n)) return 0;
    
    vector<long long> X(n);
    vector<long long> Y(n);
    
    for (int i = 0; i < n; ++i) {
        long long x, y;
        cin >> x >> y;
        // 切比雪夫坐标 -> 曼哈顿坐标
        X[i] = x + y;
        Y[i] = x - y;
    }
    
    // 曼哈顿距离的巨大优势：X 和 Y 可以完全独立排序、独立计算！
    sort(X.begin(), X.end());
    sort(Y.begin(), Y.end());
    
    // 分别计算 X 轴的曼哈顿距离和，以及 Y 轴的曼哈顿距离和
    long long total_manhattan = calc_1D_distance_sum(X) + calc_1D_distance_sum(Y);
    
    // 记得最后除以 2，才是原来的切比雪夫距离之和
    cout << total_manhattan / 2 << "\n";
    
    return 0;
}
```

### 二维平面中以某一个点中心的切比雪夫距离之和

* 不需要考虑方位

* 无论这个 $A \times B$ 的矩形是在中心点的左上、左下、右上还是右下，只要它的长宽是 $A$ 和 $B$，里面所有点到中心点（某一个角）的距离集合是**一模一样**的

$$dist(A,B)=max(∣i_A​−i_B​∣,∣j_A​−j_B​∣)$$

```cpp
	 // d1,d2 不表示矩形的边长，而是边长-1，也就是距离
    auto get_dist = [&](int d1, int d2) -> int {
        if (d1 > d2) swap(d1, d2);
        __int128_t A = (__int128_t)d1 * (d1 + 1) * (d1 + 2) / 6LL;
        __int128_t B = (__int128_t)d2 * (d2 + 1) * (d1 + 1) / 2LL;
        return (int)A + (int)B;
    };
    
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            int u1 = i - 1, u2 = n - i;
            int v1 = j - 1, v2 = m - j;
            int res = get_dist(u1, v1) + get_dist(u1, v2) 
                    + get_dist(u2, v1) + get_dist(u2, v2);
            res -= (v1 + 1) * v1 / 2 + (v2 + 1) * v2 / 2;
            res -= (u1 + 1) * u1 / 2 + (u2 + 1) * u2 / 2;
            
            // res 就是对于所有元素的切比雪夫距离之和
        }
    }
```
