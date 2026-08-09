---
topic: "树状数组 Fenwick"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 树状数组 Fenwick

* 维护可差分信息( sum **√** pro **√** Min **×** )
### 单点修改 + 区间查询

```C++
template <typename T>
struct fenwick_tree {
  public:
    int n;
    std::vector<T> a;
    fenwick_tree(int n_ = 0): n(n_) { init(n_); }
    void init(int n_) {
        n = n_;
        a.assign(n + 1, T { });
    }
    void add(int x, const T &v) {
        assert(1 <= x && x <= n);
	    if (x <= 0) return;
        for (int i = x; i <= n; i += i & -i) {
            a[i] = (a[i] + v);
        }
    }
    // [1, x]前缀和
    T sum(int x) {
		if (x <= 0) return T{ };
		if (x > n) x = n;
        T ans{};
        for (int i = x; i > 0; i -= i & -i) {
            ans = (ans + a[i]);
        }
        return ans;
    }
    T range_sum(int l, int r) {
        return sum(r) - sum(l - 1);
    }
    int select(const T &k) {
        int x = 0LL;
        T cur{};
        for (int i = 1 << std::__lg(n); i; i /= 2LL) {
            if (x + i <= n && cur + a[x + i] <= k) {
                x += i;
                cur = cur + a[x];
            }
        }
        return x;
    }
};
```
