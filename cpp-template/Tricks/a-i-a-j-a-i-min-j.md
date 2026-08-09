---
topic: "对于一个数组找寻 a[i] < a[j] 且 a[i] 为 Min，j和i之间不存在  a[i] <= a[k] <= a[j]"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 对于一个数组找寻 a[i] < a[j] 且 a[i] 为 Min，j和i之间不存在  a[i] <= a[k] <= a[j]

不用DP找长度为2的上升子序列，直接维护一个最小值和次小值，然后计数就可以了。

```c++
void solve() {
    int n, m1, m2, c;
    cin >> n;
    vector<int> p(n + 1);
    for (int i = 1; i <= n; i++) cin >> p[i];

    m1 = m2 = INF;
    c = 0;
    for (int i = 1; i <= n; i++) {
        if (p[i] < m1) m1 = p[i];
        else if (p[i] < m2) {
            m2 = p[i];
            c++;
        }
    }
    cout << c << endl;
}
```
***
