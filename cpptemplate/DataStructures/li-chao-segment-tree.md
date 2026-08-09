---
topic: "(3) LiChaoSegmentTree 李超树"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

### LiChaoSegmentTree 李超树

```C++
#define double long double
template<class Op, typename T = i64>
struct lichao_segment_tree {
  public:
    struct Node { int lch = 0, rch = 0, id = 0; };
    struct Line {
        T k, b;
        T L, R;
        T inva;
        Line() : k(0), b((T)0), L(0), R((T)-1), inva((T)0) {}
        Line(T _k, T _b, T _L, T _R, T _inva) : k(_k), b(_b), L(_L), R(_R), inva(_inva) {}
        inline T f(T x) const { return (L <= x && x <= R) ? (k * x + b) : inva; }
    };
    std::vector<Node> tr;
    std::vector<Line> lines;
    Op cmp;
    T L, R;
    T InVa;

    // 构造器与原接口一致（不改变）
    lichao_segment_tree(i64 l, i64 r) : L((T)l), R((T)r) {
        InVa = (T)Op::inva(); // 要求 Op::inva() 可转换为 T
        tr.reserve(4096);
        lines.reserve(4096);
        tr.emplace_back(); // 0 无效
        tr.emplace_back(); // 1 根
        lines.emplace_back(Line((T)0, InVa, (T)0, (T)-1, InVa)); // 0 号虚线
    }
    inline int newNode() {
        tr.emplace_back();
        return (int)tr.size() - 1;
    }

    // insert 保持签名（参数类型为 T，可接受 long long/int 隐式转换）
    int insert(T k, T b, T l, T r) {
        lines.emplace_back(Line(k, b, l, r, InVa));
        int idx = (int)lines.size() - 1;
        update(1, L, R, l, r, idx);
        return idx;
    }

    // query_point 保持接口（返回 pair<T,int>，与原来 pair<i64,int> 行为一致当 T=long long）
    std::pair<T, int> query_point(i64 x) {
        return query(1, L, R, (T)x);
    }
    void update(int p, T l, T r, T ql, T qr, int idx) {
        if (qr < l || r < ql) return;
        if (ql <= l && r <= qr) {
            if (!tr[p].id) { tr[p].id = idx; return; }
            T mid = l + ((r - l) >> 1);
            auto A = std::make_pair(lines[idx].f(mid), idx);
            auto B = std::make_pair(lines[tr[p].id].f(mid), tr[p].id);
            if (cmp(A, B).second == idx) std::swap(idx, tr[p].id);
            if (l == r) return;

            A = { lines[idx].f(l), idx };
            B = { lines[tr[p].id].f(l), tr[p].id };
            if (cmp(A, B).second == idx) {
                if (!tr[p].lch) tr[p].lch = newNode();
                update(tr[p].lch, l, mid, ql, qr, idx);
            }

            A = { lines[idx].f(r), idx };
            B = { lines[tr[p].id].f(r), tr[p].id };
            if (cmp(A, B).second == idx) {
                if (!tr[p].rch) tr[p].rch = newNode();
                update(tr[p].rch, mid + 1, r, ql, qr, idx);
            }
            return;
        }
        T mid = l + ((r - l) >> 1);
        if (ql <= mid) {
            if (!tr[p].lch) tr[p].lch = newNode();
            update(tr[p].lch, l, mid, ql, qr, idx);
        }
        if (mid < qr) {
            if (!tr[p].rch) tr[p].rch = newNode();
            update(tr[p].rch, mid + 1, r, ql, qr, idx);
        }
    }

    std::pair<T, int> query(int p, T l, T r, T x) {
        if (!p) return { InVa, 0 };
        std::pair<T, int> res = { InVa, 0 };
        if (tr[p].id) res = { lines[tr[p].id].f(x), tr[p].id };
        if (l == r) return res;
        T mid = l + ((r - l) >> 1);
        if (x <= mid) return cmp(query(tr[p].lch, l, mid, x), res);
        else return cmp(query(tr[p].rch, mid + 1, r, x), res);
    }
};
struct OpMax {
    static i64 inva() { return -INF; }
    pair<i64, int> operator() (pair<i64, int> a, pair<i64, int> b) const {
        i64 t = a.first - b.first;
        if (t > 0) return a;
        if (t < 0) return b;
        return (a.second < b.second) ? a : b;
    }
};
struct OpMin {
    static i64 inva() { return INF; }  
    pair<i64, int> operator() (pair<i64, int> a, pair<i64, int> b) const {
        i64 t = a.first - b.first;
        if (t > 0) return b;
        if (t < 0) return a;
        return (a.second < b.second) ? a : b;
    }
};
```
