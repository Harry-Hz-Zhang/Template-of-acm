---
topic: "对顶堆 Dual Heap"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 对顶堆 Dual Heap

### (1) 维护中位数 + 双指针 + 子数组元素全部相等的最小代价

```C++
struct dual_heap {
  public:
    multiset<int> L, R;
    int64_t sumL, sumR;

    dual_heap(): sumL(static_cast<int>(0)), sumR(static_cast<int>(0)) { }
    void re_balance() {
        // ensure |L| >= |R| and |L| - |R| <= 1
        while (static_cast<int> (L.size()) > static_cast<int> (R.size()) + 1) {
            auto it = prev(L.end());
            int v = *it;
            sumL -= v; sumR += v;
            R.insert(v); L.erase(it);
        }
        while ((int)R.size() > (int)L.size()) {
            auto it = R.begin();
            int v = *it;
            sumL += v; sumR -= v;
            L.insert(v); R.erase(it);
        }
    }

    void insert(int x) {
        if (L.empty() || x <= *prev(L.end())) {
            L.insert(x);
            sumL += x;
        } else {
            R.insert(x);
            sumR += x;
        }
        re_balance();
    }

    void remove(int x) {
        auto it = L.find(x);
        if (it != L.end()) {
            sumL -= x;
            L.erase(it);
        } else {
            it = R.find(x);
            if (it != R.end()) {
                sumR -= x;
                R.erase(it);
            }
        }
        re_balance();
    }
    int size() { return static_cast<int>(L.size() + R.size()); }
    int median() {
        if (L.empty()) return 0LL;
        return *prev(L.end());
    }
};

void solve()
{
    int n, k;
    cin >> n >> k;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i], a[i] -= i;

    dual_heap heap;
    auto cost = [&]() -> int {
        if (heap.size() == 0) return 0;
        int mid = heap.median();
        return heap.L.size() * mid - heap.sumL + heap.sumR - heap.R.size() * mid;
    };

    int ans = 0;
    for (int i = 1, j = i + 1; i <= n; i++) {
        while (j <= n && a[j] == a[i]) j++;
        ans = max(j - i, ans);
        i = j - 1;
    }
    if (k == 0) {
        cout << ans << endl;
        return;
    }

    for (int i = 1, j = 0; i <= n; i++) {
        while (j < n && cost() <= k) {
            heap.insert(a[++j]);
        }
        if (cost() > k) heap.remove(a[j--]);
        ans = max(ans, j - i + 1);

        heap.remove(a[i]);
    }

    cout << ans << endl;
}
```

### (2) 第K大数

```C++
struct Top_K {
  public:
    multiset<int> top, rest;
    i64 sum_ = 0;
    int k;
    Top_K(int _k): k(_k) { }

    void insert(int x) {
        if (k == 0) {
            rest.insert(x);
            return;
        }
        if ((int)top.size() < k) {
            top.insert(x);
            sum_ += x;
        } else {
            auto it = top.begin(); // top.begin() 是 top 中最小的元素（即第 k 大）
            if (x > *it) {
                top.insert(x); sum_ += x;
                rest.insert(*it); sum_ -= *it;
                top.erase(it);
            } else {
                rest.insert(x);
            }
        }
    }

    void remove(int x) {
        auto it = top.find(x);
        if (it != top.end()) {
            top.erase(it);
            sum_ -= x;
            if (!rest.empty()) {
                it = prev(rest.end());
                top.insert(*it); sum_ += *it;
                rest.erase(it);
            }
        } else {
            it = rest.find(x);
            if (it != rest.end()) rest.erase(it);
        }
    }

    void changeK(int k_) {
        k = k_;
        // k 增大：从 rest 中取出最大的补到 top
        while ((int)top.size() < k && !rest.empty()) {
            auto it = prev(rest.end());
            top.insert(*it); sum_ += *it;
            rest.erase(it);
        }
        // k 减小：把 top 中最小的移入 rest
        while ((int)top.size() > k) {
            auto it = top.begin();
            rest.insert(*it); sum_ -= *it;
            top.erase(it);
        }
    }
    int Topk() {
        if (top.empty()) return numeric_limits<int>::min();
        return *top.begin();
    }
    int sum() { // 保持原接口名 sum()
        return sum_;
    }
};
```
