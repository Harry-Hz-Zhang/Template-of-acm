---
topic: "(2) 懒标记线段树（区间修改，区间查询 LazySegmentTree -> LSGT）"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

### 懒标记线段树（区间修改，区间查询 LazySegmentTree -> LSGT）
#### 区间 + / ×

```C++
template<class Info, class Tag> 
struct lazy_segment_tree {
  public:
    int n;
    std::vector<Info> info;
    std::vector<Tag> tag;

    lazy_segment_tree() : n(0) {}
    lazy_segment_tree(int _n, Info _v = Info()) {
        init(_n, _v);
    }
    template<class T>
    lazy_segment_tree(std::vector<T> _init) {
        init(_init);
    }
    void init(int _n, Info _v = Info()) {
        init(std::vector(_n + 1, _v));
    }
    template<class T>
    void init(std::vector<T> _init) {
        n = _init.size() - 1;
        info.assign(n * 4 + 1, Info());
        tag.assign(n * 4 + 1, Tag());
        auto build = [&](auto self, int p, int l, int r) {
                if (l == r)
                {
                    info[p] = _init[l];
                    return;
                }
                int mid = (l + r) >> 1;
                self(self, p << 1, l, mid);
                self(self, p << 1 | 1, mid + 1, r);
                pull(p);
            };
        build(build, 1, 1, n);
    }
    void pull(int p) {
        info[p] = info[p << 1] + info[p << 1 | 1];
    }
    void apply(int p, const Tag& v, int len) {
        info[p].apply(v, len);
        tag[p].apply(v);
    }
    void push(int p, int len) {
        apply(p << 1, tag[p], len + 1 >> 1);
        apply(p << 1 | 1, tag[p], len >> 1);
        tag[p] = Tag();
    }
    void modify(int p, int l, int r, int x, const Info& v) {
        if (l == r) {
            info[p] = v;
            return;
        }
        int mid = (l + r) >> 1;
        push(p, r - l + 1);
        if (x <= mid) {
            modify(p << 1, l, mid, x, v);
        } else {
            modify(p << 1 | 1, mid + 1, r, x, v);
        }
        pull(p);
    }
    void modify(int p, const Info& v) {
        modify(1LL, 1LL, n, p, v);
    }
    Info range_query(int p, int l, int r, int x, int y) {
        if (l > y || r < x) {
            return Info();
        }
        if (l >= x && r <= y) {
            return info[p];
        }
        int mid = (l + r) >> 1;
        push(p, r - l + 1);
        return range_query(p << 1, l, mid, x, y) + range_query(p << 1 | 1, mid + 1, r, x, y);
    }
    Info range_query(int l, int r) {
        if (n == 0) return Info();
        if (l > r) return Info();
        l = max(l, 1LL); 
        r = min(r, n); 
        return range_query(1, 1, n, l, r);
    }
    void range_apply(int p, int l, int r, int x, int y, const Tag& v) {
        if (l > y || r < x) {
            return;
        }
        if (l >= x && r <= y) {
            apply(p, v, r - l + 1);
            return;
        }
        int mid = l + r >> 1;
        push(p, r - l + 1);
        range_apply(p << 1, l, mid, x, y, v);
        range_apply(p << 1 | 1, mid + 1, r, x, y, v);
        pull(p);
    }
    void range_apply(int l, int r, const Tag& v) {
        if (n == 0) return; 
        if (l > r) return;
        l = max(l, 1LL); 
        r = min(r, n);
        return range_apply(1, 1, n, l, r, v);
    }
	template<class F>
    int find_first(int p, int l, int r, int x, int y, F pred) {
        if (l > y || r < x || !pred(info[p])) {
            return -1;
        }
        if (l == r) {
            return l;
        }
        int m = (l + r) >> 1;
        push(p, r - l + 1); // need to push lazy tags to children before recursing
        int res = find_first(p << 1, l, m, x, y, pred);
        if (res == -1) {
            res = find_first(p << 1 | 1, m + 1, r, x, y, pred);
        }
        return res;
    }
    template<class F>
    int find_first(int l, int r, F pred) {
        if (n == 0) return -1;
        if (l > r) return -1;
        l = max(l, 1LL); 
        r = min(r, n);
        return find_first(1, 1, n, l, r, pred);
    }

    // 修正 findLast（先查右子树，再查左子树；并传递正确的 child indices 和区间）
    template<class F>
    int find_last(int p, int l, int r, int x, int y, F pred) {
        if (l > y || r < x || !pred(info[p])) {
            return -1LL;
        }
        if (l == r) {
            return l;
        }
        int m = l + r >> 1LL;
        push(p, r - l + 1);
        // 先查右子树（最后一个通常在右边）
        int res = find_last(p << 1 | 1, m + 1, r, x, y, pred);
        if (res == -1) {
            res = find_last(p << 1, l, m, x, y, pred);
        }
        return res;
    }
    template<class F>
    int find_last(int l, int r, F pred) {
        if (n == 0) return -1;
        if (l > r) return -1;
        l = max(l, 1LL); r = min(r, n);
        return find_last(1LL, 1LL, n, l, r, pred);
    }
};

/* 
	注意 Info 区间和 Tag 区间默认构造函数的设置与赋值，一定是空集合
	即：不能对原本合并区间产生实际影响
	如：Min = INF， Max = -INF， sum = 0 ...
*/
struct Tag {
  public:
    int mul, add;
    Tag(int _mul = 1LL, int _add = 0): mul(_mul), add(_add) { }
    void apply(const Tag &t) {
        mul = mul * t.mul % mod;
        add = (add * t.mul % mod + t.add) % mod;
    }
};
struct Info {
  public:
    int sum = 0;
    Info() { }
    Info(int sum) : sum(sum) { }
    void apply(const Tag &t, int len) {
        sum = (sum * t.mul % mod + t.add * len % mod) % mod;
    }    
};
Info operator+(const Info &l, const Info &r) {
    Info u;
    u.sum = (l.sum + r.sum) % mod;
    return u;
}
```

#### 区间 Min

```C++
struct Tag {
  public:
    i64 cap = INF; // cap = 最终要把区间中的每个值变为 min(old, cap)
    Tag() = default;
    Tag(i64 v) : cap(v) {}
    void apply(const Tag &t) {
        // 组合两个 chmin：先 chmin by cap1 再 chmin by cap2 等价于 chmin by min(cap1, cap2)
        cap = std::min(cap, t.cap);
    }
};
// Info 记录区间内的最小值以及该最小值对应的一个位置（pos）
struct Info {
  public:
    long long min = INF; // 当前区间内的最小 b[i]
    int pos = 0;         // 使得 b[pos] = min 的一个下标（leaf 时为叶下标）
    Info() = default;
    Info(long long _min, int _pos) : min(_min), pos(_pos) {}
    // 当一个 chmin 标签作用到这个区间上（懒标），就把区间内的每个值 cap 为 tag.cap。
    // 对于维护的最小值来说，新的最小值为 min(old_min, tag.cap)。
    void apply(const Tag &t, int len) {
        if (t.cap == INF) return; // 无效标签
        if (min > t.cap) {
            // 注意：我们不知道区间内哪一个位置会成为新的最小值，
            // 但把 min 设置为 t.cap 可以保证 min 的数值是正确的。
            // pos 在需要时（下推至叶子时）会被正确修正，因为 push 会把标签下推到孩子。
            min = t.cap;
        }
        // 如果 min <= t.cap，则 min 不变。
    }
};

// 合并左右孩子信息：返回区间的 min 与其对应 pos（若相等则取较小下标）
Info operator+(const Info &l, const Info &r) {
    if (l.min < r.min) return {l.min, l.pos};
    if (r.min < l.min) return {r.min, r.pos};
    // 相等时取位置较小者（保证确定性）
    return {l.min, std::min(l.pos, r.pos)};
}
```

#### 最小值 + 下标

```C++
struct Tag {
  public:
	int add = 0;
	void apply(const Tag &t) {
		add += t.add;
	}
};
struct Info {
  public:
	int min = INF;
	int pos = 0;
	void apply(const Tag &t, int len) {
		min += t.add;
	}
};
Info operator+(const Info &l, const Info &r) {
	if (l.min < r.min) return {l.min, l.pos};
	if (r.min < l.min) return {r.min, r.pos};
	return {l.min, min(l.pos, r.pos)};
}
```

#### 最小值 + 个数

```C++
struct Tag {
  public:
    int add;
    Tag(int _add = 0): add(_add) { }
    void apply(const Tag &t) {
        add = add + t.add;
    }
};

struct Info {
  public:
    int Min;
    int cnt;
    Info(): Min(INF), cnt(0) { }
    Info(int min_, int c = 0): Min(min_), cnt(c) { }
    void apply(const Tag &t, int len = 1) {
        Min += t.add;
    }
};

Info operator+(const Info &l, const Info &r) {
    Info u;
    u.Min = std::min(l.Min, r.Min);
    u.cnt = 0;
    if (l.Min == u.Min) u.cnt += l.cnt;
    if (r.Min == u.Min) u.cnt += r.cnt;
    return u;
}
```

#### 最大值 + 下标

```C++
struct Tag {
  public:
	int add = 0;
	void apply(const Tag &t) {
		add += t.add;
	}
};
struct Info {
  public:
	int max = -INF;
	int pos = 0;
	void apply(const Tag &t, int len) {
		max += t.add;
	}
};
  
Info operator+(const Info &l, const Info &r) {
	if (l.max > r.max) return {l.max, l.pos};
	if (r.max > l.max) return {r.max, r.pos};
	return {l.max, min(l.pos, r.pos)};
}
```

* 查询区间中是否有两个相同的数字
#### 区间 异或 / 赋值 / 查找第k个1

```C++
template<class Info, class Tag> 
class lazy_segment_tree {
  public:
    int n;
    vector<Info> info;
    vector<Tag> tag;

    lazy_segment_tree(): n(0) { }
    lazy_segment_tree(int _n, Info _v = Info()) {
        init(_n, _v);
    }
    template<class T>
    lazy_segment_tree(vector<T> _init) {
        init(_init);
    }
    void init(int _n, Info _v = Info()) {
        init(vector(_n + 1, _v));
    }
    template<class T> 
    void init(vector<T> _init) {
        n = _init.size() - 1;
        info.assign(n * 4 + 1, Info());
        tag.assign(n * 4 + 1, Tag());
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
    void apply(int p, const Tag &v, int len) {
        info[p].apply(v, len);
        tag[p].apply(v);
    }
    void push(int p, int len) {
        apply(p << 1, tag[p], len + 1 >> 1);
        apply(p << 1 | 1, tag[p], len >> 1);
        tag[p] = Tag();
    }

    Info range_query(int p, int l, int r, int x, int y) {
        if (l > y || r < x) {
            return Info();
        }
        if (l >= x && r <= y) {
            return info[p];
        }
        int mid = l + r >> 1;
        push(p, r - l + 1);
        return range_query(p << 1, l, mid, x, y) + range_query(p << 1 | 1, mid + 1, r, x, y);
    }
    Info range_query(int l, int r) {
        return range_query(1, 1, n, l, r);
    }
    void range_apply(int p, int l, int r, int x, int y, const Tag &v) {
        if (l > y || r < x) {
            return;
        }
        if (l >= x && r <= y) {
            apply(p, v, r - l + 1);
            return;
        }
        int mid = l + r >> 1;
        push(p, r - l + 1);
        range_apply(p << 1, l, mid, x, y, v);
        range_apply(p << 1 | 1, mid + 1, r, x, y, v);
        pull(p);
    }
    void range_apply(int l, int r, const Tag &v) {
        return range_apply(1, 1, n, l, r, v);
    }
    int search(int p, int l, int r, int x) {   // 二分搜索不需要处理前缀和一类的
        if (l == r) return l;
        push(p, r - l + 1);
        int mid = l + r >> 1;
        if (info[p << 1].sum >= x) {
            return search(p << 1, l, mid, x);
        } else {
            return search(p << 1 | 1, mid + 1, r, x - info[p << 1].sum);
        }
    }
    int search(int x) {   // 返回第一个值大于等于 x 的下标（第几个数字）
        return search(1, 1, n, x);
    }
};

struct Tag {
  public:
    int f = 0;
    Tag(int _f = 0): f(_f) { }
    void apply(const Tag &t) {
        f ^= t.f;
    }
};

/*
struct Tag {
    int f = 0;
    Tag(int _f = 0): f(_f) { }
    void apply(const Tag &t) {
        if (t.f == 0) return;   // 小心 push 时候被空的 Tag 覆盖掉
        f = t.f;
    }
};
*/

struct Info {
  public:
    int sum;
    Info(int _sum = 0) : sum(_sum) { }
    void apply(Tag t, int len) {
        if (t.f) {
            sum = len - sum;
        }
    }
};
Info operator+(const Info &l, const Info &r) {
    Info u;
    u.sum = l.sum + r.sum;
    return u;
}

void solve()
{
    int n, m;
    cin >> n >> m;
    vector<Info> info(n + 1, Info(0));
    lazy_segment_tree<Info, Tag> seg(info);
    while(m--) {
        int op;
        cin >> op;
        if (op == 1) {
            int l, r;
            cin >> l >> r;
            l++;
            seg.range_apply(l, r, {1});
        } else {
            int k;
            cin >> k;
            k++;
            cout << seg.search(k) - 1 << endl;
        }
    }
}
```

#### 维护等差数列
* 可以加等差数列，原理如下： 维护差分数组，前缀和就是当前位置元素

```c++
vector<int> d(n + 1, 0);
lazy_segment_tree<Info, Tag> seg(d);

int ans = 0;
for (int i = n; i >= k; i--) {
	int num = seg.range_query(1, i).sum;
	if (num < b[i]) {
		int dt = b[i] - num;
		int cnt = dt / k + (dt % k ? 1 : 0);
		ans += cnt;
		int x = cnt, dd = cnt;
		int l = i - k + 1, r = i;
		seg.range_apply(l, l, {x}), seg.range_apply(l + 1, r, {dd});
		if (r + 1 <= n) {
			seg.range_apply(r + 1, r + 1, {-x + (dd * (r - l))});
		}
	}
}
```

#### 区间 & 操作 / 查找某区间中第一个数字第 bit 位不为 1

```C++
template<class Info, class Tag> 
struct lazy_segment_tree {
  public:
    int n;
    std::vector<Info> info;
    std::vector<Tag> tag;

    lazy_segment_tree() : n(0) {}
    lazy_segment_tree(int _n, Info _v = Info()) {
        init(_n, _v);
    }
    template<class T>
    lazy_segment_tree(std::vector<T> _init) {
        init(_init);
    }
    void init(int _n, Info _v = Info()) {
        init(std::vector(_n + 1, _v));
    }
    template<class T>
    void init(std::vector<T> _init) {
        n = _init.size() - 1;
        info.assign(n * 4 + 1, Info());
        tag.assign(n * 4 + 1, Tag());
        auto build = [&](auto self, int p, int l, int r) {
                if (l == r)
                {
                    info[p] = _init[l];
                    return;
                }
                int mid = (l + r) >> 1;
                self(self, p << 1, l, mid);
                self(self, p << 1 | 1, mid + 1, r);
                pull(p);
            };
        build(build, 1, 1, n);
    }
    void pull(int p) {
        info[p] = info[p << 1] + info[p << 1 | 1];
    }
    void apply(int p, const Tag& v, int len) {
        info[p].apply(v, len);
        tag[p].apply(v);
    }
    void push(int p, int len) {
        apply(p << 1, tag[p], len + 1 >> 1);
        apply(p << 1 | 1, tag[p], len >> 1);
        tag[p] = Tag();
    }
    void modify(int p, int l, int r, int x, const Info& v) {
        if (l == r) {
            info[p] = v;
            return;
        }
        int mid = (l + r) >> 1;
        push(p, r - l + 1);
        if (x <= mid) {
            modify(p << 1, l, mid, x, v);
        } else {
            modify(p << 1 | 1, mid + 1, r, x, v);
        }
        pull(p);
    }
    void modify(int p, const Info& v) {
        modify(1, 1, n, p, v);
    }
    Info range_query(int p, int l, int r, int x, int y) {
        if (l > y || r < x) {
            return Info();
        }
        if (l >= x && r <= y) {
            return info[p];
        }
        int mid = (l + r) >> 1;
        push(p, r - l + 1);
        return range_query(p << 1, l, mid, x, y) + range_query(p << 1 | 1, mid + 1, r, x, y);
    }
    Info range_query(int l, int r) {
        return range_query(1, 1, n, l, r);
    }
    void range_apply(int p, int l, int r, int x, int y, const Tag& v) {
        if (l > y || r < x) {
            return;
        }
        if (l >= x && r <= y) {
            apply(p, v, r - l + 1);
            return;
        }
        int mid = (l + r) >> 1;
        push(p, r - l + 1);
        range_apply(p << 1, l, mid, x, y, v);
        range_apply(p << 1 | 1, mid + 1, r, x, y, v);
        pull(p);
    }
    void range_apply(int l, int r, const Tag& v) {
        return range_apply(1, 1, n, l, r, v);
    }

    template<class F>
    int find_first(int p, int l, int r, int x, int y, F pred) {
        if (l > y || r < x) {
            return -1;
        }
        if (l >= x && r <= y && !pred(info[p])) {
            return -1;
        }
        if (l == r) {
            return l;
        }

        int m = l + r >> 1;
        push(p, r - l + 1);   // 懒标记下传
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
};

const int M = (1LL << 63) - 1;
struct Tag {
  public:
    int x;
    Tag(int x_ = M): x(x_) { }
    void apply(const Tag &t) {
        x &= t.x;
    }
};
struct Info {
  public:
    int f = 0;
    int g = M;
    
    Info() { }
    Info(int _, int x) :f(_), g(x) { }
    void apply(const Tag &t, int len) {
        g &= t.x;
        if (len == 1) {   // 叶子节点
            f = ~g;
        } else {
            f &= t.x;
        }
    }
};
Info operator+(const Info &l, const Info &r) {
    Info u;
    u.g = l.g & r.g;
    u.f = (l.f & r.g) | (r.f & l.g);
    return u;
}
int i = seg.find_first(l, r, [&](const Info& v){
    int x = v.f;
    return (x >> bit & 1) == 1;
});
```
