---
topic: "a,b,有序数列求和 取第k大"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# a,b,有序数列求和 取第k大

先把a，b中最大的放入优先队列（大根堆） ，a[n-1]+b[n]，a[n]+b[n-1]放入优先队列（下标不越界的情况下） ，并且每个取法只能放入一次优先队列，执行到k次的时候就是答案了

```C++
struct node{
    int v;
    vector<int> p;
    bool operator< (const node& t) const {
        return v < t.v;
    }
};

// 某种排列的大小以及具体方案，然后bfs
while(heap.size()) {
    auto [v, p] = heap.top();
    heap.pop();

    if (use[p]) continue;
    use[p] = 1;
    if (mp.count(p) == 0) {   // 如果不是非法排列
        for (int i = 1; i < p.size(); i++) {
            cout << p[i] << " \n"[i == p.size() - 1];
        }
        cout << endl;
        return;
    }
    int sum = v;
    for (int i = 1; i <= n; i++) {
        if (p[i] <= 1) continue;   // 是否已经枚举到了第一个元素
        sum -= a[i][p[i]];
        p[i] --;
        sum += a[i][p[i]];   // 放入这种情况
        if (use[p] == 0) {
            heap.push(node{sum, p});
        }
        p[i]++;   // 回溯
        sum = v;
    }
}
```

***
