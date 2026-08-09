---
topic: "单调队列优化"
category: "10-dp"
source: "动态规划 DP.md"
---

# 单调队列优化

```C++
    vector<int> laq(n + 2);
    // laq 是上一个必须建立的地方
    
    laq[0] = 0;
    for (int i = 1; i <= n + 1; i++) {
        if (s[i] == '1') {
            laq[i] = i;
        } else {
            laq[i] = laq[i - 1];
        }
    }
    deque<int> q;
    vector<int> f(n + 2, INF);  // 最小的代价
    f[0] = 0;
    for (int i = 1; i <= n + 1; i++) {
        int j = i - 1;  // 因为当前的 i 没有计算，所以和上一个比较！
        while (q.size() && f[j] <= f[q.back()]) q.pop_back();
        q.push_back(j);
        
        int ll = max(i - k, laq[i - 1]);  // 超出范围的去掉
        while (q.size() && q.front() < ll) q.pop_front();
        f[i] = f[q.front()] + a[i];
    }
```
