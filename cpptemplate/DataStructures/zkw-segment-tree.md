---
topic: "(4) ZKW 区间最大值 / 区间最小值 / 区间和"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

### ZKW 区间最大值 / 区间最小值 / 区间和

```C++
template<class Info>
struct ZKW_segment_tree {
  public:
    int N = 1;
    int n = 0;
    vector<Info> info;

    ZKW_segment_tree() { }
    template<class T>
    ZKW_segment_tree(vector<T> init_) {
        n = (int)init_.size() - 1;
        while (N < n) N <<= 1;
        info.assign((N << 1) + 2, Info());

        for (int i = 1; i <= n; i++) info[i + N - 1] = init_[i];
        for (int i = N - 1; i >= 1; --i) info[i] = info[i << 1] + info[i << 1 | 1];
    }

    void modify(int x, const Info& v) {
        int idx = x + N - 1;
        info[idx] = v;
        for (idx >>= 1; idx; idx >>= 1) info[idx] = info[idx << 1] + info[idx << 1 | 1];
    }
    Info range_query(int l, int r) {
        Info ans = Info();
        if (l > r) return ans;
        int L = N + l - 1, R = N + r - 1;
        while (L <= R) {
            if (L & 1) ans = ans + info[L++];
            if (!(R & 1)) ans = ans + info[R--];
            L >>= 1; R >>= 1;
        }
        return ans;
    }

    int find_first(int idx, int l, int r, int ql, int qr, int f) {
        if (l > qr || r < ql) return -1;
        if (info[idx].Max < f) return -1;
        if (l == r) {
            if (l <= n) return l;
            return -1;
        }
        int mid = l + r >> 1;
        int t = find_first(idx << 1, l, mid, ql, qr, f);
        if (t != -1) return t;
        return find_first(idx << 1 | 1, mid + 1, r, ql, qr, f);
    }

    int find_first(int ql, int qr, int f) {
        if (ql > qr) return -1;
        if (range_query(ql, qr).Max < f) return -1;
        return find_first(1, 1, N, ql, qr, f);
    }
};

struct Info {
    int Max = 0;
    Info() { }
    Info(int _) : Max(_) { };
};

Info operator+(const Info &l, const Info &r) {
    if (l.Max >= r.Max) return l;
    if (r.Max > l.Max) return r;
    return l;
};
```
