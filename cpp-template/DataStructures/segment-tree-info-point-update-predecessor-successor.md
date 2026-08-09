---
topic: "(1) SegmentTree Info 区间+ 单点修改 +查找前驱后继 (左闭右闭)"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

### SegmentTree Info 区间+ 单点修改 +查找前驱后继 (左闭右闭)

```C++
template<class Info>
struct segment_tree {
  public:
	int n;
    vector<Info> info;
    segment_tree() { }
    segment_tree(int _n, Info _v = Info()) {
        init(_n, _v);
    }
    template<class T>
    segment_tree(vector<T> _init) {
        init(_init);
    }

    void init(int _n, Info _v = Info()) {
        init(vector(_n + 1, _v));
    }
    template<class T>
    void init(vector<T> _init) {
        n = _init.size() - 1;
        info.assign(4 * n + 1, Info());
        auto build = [&](auto self, int p, int l, int r) {
                if (l == r) {
                    info[p] = _init[l];
                    return;
                }
                int mid = l + r >> 1;
                self(self, p << 1, l, mid);
                self(self, p << 1 | 1, mid + 1, r);
                pull(p);
            };
        build(build, 1, 1, n);
    }
    void pull(int p) {
        info[p] = info[p << 1] + info[p << 1 | 1];
    }
    void modify(int p, int l, int r, int x, const Info& v) {
        if (l == r) {
            info[p] = v;
            return;
        }
        int mid = l + r >> 1;
        if (x <= mid) {
            modify(p << 1, l, mid, x, v);
        }
        else {
            modify(p << 1 | 1, mid + 1, r, x, v);
        }
        pull(p);
    }
    void modify(int x, const Info& v) {
        modify(1, 1, n, x, v);
    }

    Info range_query(int p, int l, int r, int x, int y) {
        if (l > y || r < x) {
            return Info();
        }
        if (l >= x && r <= y) {
            return info[p];
        }
        int mid = l + r >> 1;
        return range_query(p << 1, l, mid, x, y) + range_query(p << 1 | 1, mid + 1, r, x, y);
    }
    Info range_query(int x, int y) {
        return range_query(1, 1, n, x, y);
    }

    template<class F>
    int find_first(int p, int l, int r, int x, int y, F pred) {
        if (l > y || r < x || !pred(info[p])) {
            return -1;
        }
        if (l == r) {
            return l;
        }
        int m = l + r >> 1;
        int res = find_first(p << 1, l, m, x, y, pred);
        if (res == -1) {
            res = find_first(p << 1 | 1, m + 1, r, x, y, pred);
        }
        return res;
    }

    template<class F>
    int find_first(int l, int r, F pred) {
        return find_first(1, 1, n, l, r, pred);
    }

    template<class F>
    int find_last(int p, int l, int r, int x, int y, F pred) {
        if (l > y || r < x || !pred(info[p])) {
            return -1;
        }
        if (l == r) {
            return l;
        }
        int m = l + r >> 1;
        int res = find_last(p << 1, m + 1, r, x, y, pred);
        if (res == -1) {
            res = find_last(p << 1 | 1, l, m, x, y, pred);
        }
        return res;
    }
    template<class F>
    int find_last(int l, int r, F pred) {
        return find_last(1, 1, n, l, r, pred);
    }

    int search(int p, int l, int r, int x) {   // 二分搜索不需要处理前缀和一类的
        int mid = l + r >> 1;
        if (info[p].sum == x) {
            if (l == r) return l;
            if (info[p << 1 | 1].sum == 0) return search(p << 1, l, mid, x);
            else return search(p << 1 | 1, mid + 1, r, x - info[p << 1].sum);
        }
        if (info[p].sum > x) {
            if (info[p << 1].sum < x) return search(p << 1 | 1, mid + 1, r, x - info[p << 1].sum);
            return search(p << 1, l, mid, x);
        }
    }
    int search(int x) {   // 返回第一个值大于等于 x 的下标（第几个数字）
        return search(1, 1, n, x);
    }
};

struct Info {
    int sum = 0;
    Info() { }
    Info(int _) : sum(_) { };
};

Info operator+(const Info &l, const Info &r) {
    Info u;
    u.sum = l.sum + r.sum;
    return u;
};
```
#### **`pred(info[p])`**
- `pred` 是调用者传入的一个函数对象或函数指针。
- `info[p]` 是线段树当前节点存储的信息。
- `pred(info[p])` 表示用当前节点的信息 `info[p]` 调用函数对象 `pred`，以判断这个节点是否满足某个条件。
- 如果 `pred(info[p])` 返回 `true`，说明节点满足条件；如果返回 `false`，则不满足。

```C++
Segment_tree<Info> segTree({0, 5, 8, 12, 3, 7}); // 下标从 1 开始存储
int X = 10;
// 使用 lambda 表达式定义 pred
auto pred = [&](const Info& info) {
    return info.sum > X; // 条件：节点的 sum 值大于 X
};
int result = segTree.find_first(1, 5, pred);
if (result != -1) {
    cout << "第一个满足条件的下标是: " << result << endl;
} else {
    cout << "没有节点满足条件" << endl;
}
```

简单来说，findFirst函数无法靠前缀和来维护信息，只能借助区间的最大值，最小值一类的信息来找寻某个数字。
