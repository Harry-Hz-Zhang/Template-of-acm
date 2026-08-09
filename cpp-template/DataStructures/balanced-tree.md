---
topic: "平衡树"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 平衡树

### (0) PBDS (处理 set 中比某个数大的数字的个数)

```C++
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace std;
namespace gp = __gnu_pbds;
template <typename T, typename Comp = less<>>
struct ordered_multiset {
  public:
    using pii = pair<T, int>;
    gp::tree<pii, gp::null_type, Comp,
             gp::rb_tree_tag,
             gp::tree_order_statistics_node_update>
        st;
    int _s = 0;
    auto insert(const T &x) {
        return st.insert({x, _s++});
    }
    bool erase_one(const T &x) {
        auto it = st.lower_bound({x, 0});
        if (it != st.end() && it->first == x) {
            st.erase(it);
            return true;
        }
        return false;
    }
    int erase_all(const T &x) {
        auto L = st.lower_bound({x, 0});
        auto R = st.upper_bound({x, _s});
        int cnt = distance(L, R);
        for (auto it = L; it != R;)
            it = st.erase(it);
        return cnt;
    }

    // 统计与 x 相等的元素个数
	auto count(const T &x) const {
		auto L = st.order_of_key({x, 0});
		auto R = st.order_of_key({x, numeric_limits<int>::max()});
		return R - L;
	}

    // 有序 multiset 大小
    auto size() const { return st.size(); }
    bool empty() const { return st.empty(); }

    // 返回严格小于 x 的元素个数
    auto order_of_key(const T &x) const {
        return st.order_of_key({x, 0});
    }
    // 0-based，第 k 小元素的值
    T find_by_order(int k) const {
        return st.find_by_order(k)->first;
    }
    auto lower_bound(const T &x) const {
        return st.lower_bound({x, 0});
    }
    auto upper_bound(const T &x) const {
        return st.upper_bound({x, _s});
    }
};

#define int long long
```

### (1) Splay

```C++
#include <cstdio>
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

const int maxn = 1e5 + 50, INF = 0x3f3f3f3f;  // 最大节点数和无穷大常量
int n, root, nodent;

struct Tree {
    int fa, ch[2], val, cnt, size;  // fa: 父节点，ch: 左右子节点，val: 节点值，cnt: 节点重复次数，size: 子树大小
} tree[maxn];

// 快速读取整数
inline int read() {
    int x = 0, w = 1;
    char ch = getchar();
    while (ch < '0' || ch > '9') {
        if (ch == '-') w = -1;
        ch = getchar();
    }
    while (ch >= '0' && ch <= '9') {
        x = x * 10 + ch - '0';
        ch = getchar();
    }
    return x * w;
}

// 更新节点的信息，计算节点子树的大小和重复次数
inline void Pushup(int rt) {
    int lch = tree[rt].ch[0], rch = tree[rt].ch[1];
    tree[rt].size = tree[lch].size + tree[rch].size + tree[rt].cnt;  // 节点的大小是左右子树的大小之和
}

// 旋转操作，用于平衡树结构
inline void Rotate(int x) {
    int y = tree[x].fa, z = tree[y].fa, k = tree[y].ch[1] == x;
    tree[z].ch[tree[z].ch[1] == y] = x;
    tree[y].ch[k] = tree[x].ch[k ^ 1];
    tree[tree[x].ch[k ^ 1]].fa = y;
    tree[x].ch[k ^ 1] = y;
    tree[x].fa = z;
    tree[y].fa = x;
    Pushup(y);
    Pushup(x);
}

// Splay 操作，将节点 x 移动到根
inline void Splay(int x, int aim) {
    while (tree[x].fa != aim) {
        int y = tree[x].fa, z = tree[y].fa;
        if (z != aim) {
            if (tree[z].ch[0] == y && tree[y].ch[0] == x || tree[z].ch[1] == y && tree[y].ch[1] == x)
                Rotate(y);  // 双重旋转
            else
                Rotate(x);  // 单旋转
        }
        Rotate(x);
    }
    if (!aim) root = x;
}

// 插入操作
inline void Insert(int x) {
    int u = root, fa = 0;
    while (u && x != tree[u].val) {
        fa = u;
        u = tree[u].ch[x > tree[u].val];
    }
    if (u) tree[u].cnt++;  // 插入已存在的值，增加次数
    else {
        u = ++nodent;
        tree[fa].ch[x > tree[fa].val] = u;
        tree[u].val = x;
        tree[u].fa = fa;
        tree[u].cnt = tree[u].size = 1;
    }
    Splay(u, 0);
}

// 查找操作
inline void Find(int x) {
    int u = root;
    while (tree[u].ch[x > tree[u].val] != 0) u = tree[u].ch[x > tree[u].val];
    Splay(u, 0);
}

// 删除操作
inline void Delete(int x) {
    int pre = Pre(x), nxt = Nxt(x);
    Splay(pre, nxt);
    Splay(nxt, pre);
    tree[nxt].ch[0] = 0;
    Pushup(nxt);
    Splay(nxt, 0);
}

// 查找某节点的前驱节点
inline int Pre(int x) {
    Find(x);
    if (!tree[root].ch[0]) return -1;
    int u = tree[root].ch[0];
    while (tree[u].ch[1]) u = tree[u].ch[1];
    return u;
}

// 查找某节点的后继节点
inline int Nxt(int x) {
    Find(x);
    if (!tree[root].ch[1]) return -1;
    int u = tree[root].ch[1];
    while (tree[u].ch[0]) u = tree[u].ch[0];
    return u;
}

// 查找第 k 小的元素
inline int Findkth(int k) {
    int u = root;
    if (tree[u].size < k) return -1;
    while (true) {
        if (tree[tree[u].ch[0]].size >= k) u = tree[u].ch[0];
        else if (tree[tree[u].ch[0]].size + tree[u].cnt < k) {
            k -= tree[tree[u].ch[0]].size + tree[u].cnt;
            u = tree[u].ch[1];
        } else return u;
    }
}

// 获取某节点的秩（在中序遍历中的位置）
inline int Getrank(int x) {
    return Find(x) - tree[tree[root].ch[0]].size;
}

int main() {
    n = read();
    Insert(INF), Insert(-INF);
    while (n--) {
        int opt = read(), x = read();
        if (opt == 1) Insert(x);
        else if (opt == 2) Delete(x);
        else if (opt == 3) printf("%d\n", Getrank(x));
        else if (opt == 4) printf("%d\n", tree[Findkth(x + 1)].val);
        else if (opt == 5) printf("%d\n", tree[Pre(x)].val);
        else printf("%d\n", tree[Nxt(x)].val);
    }
    return 0;
}

```

### (2)Treap

 https://loj.ac/p/104

```C++
#include <bits/stdc++.h>
using i64 = long long;

constexpr int inf = 1e7 + 10;
std::mt19937 rng(std::chrono::steady_clock::now().time_since_epoch().count());

struct Node {
    Node *l, *r;
    int cnt, siz, val, pri;

    Node() {}
    Node(int v) {
        init(v);
    }

    void init(int v) {
        l = nullptr;
        r = nullptr;
        cnt = 1;
        siz = 1;
        val = v;
        pri = rng();
    }

    int size() {
        siz = cnt;

        if (l) {
            siz += l->siz;
        }
        if (r) {
            siz += r->siz;
        }
        return siz;
    }
};

class Treap {
private:
    Node *root;

    void split(Node *t, int k, Node *&l, Node *&r) {
        if (!t) {
            l = nullptr;
            r = nullptr;
            return;
        }

        if (t->val <= k) {
            l = t;
            split(t->r, k, t->r, r);
        } else {
            r = t;
            split(t->l, k, l, t->l);
        }

        t->size();
    }

    Node *merge(Node *l, Node *r) {
        if (!l)
            return r;

        if (!r)
            return l;

        if (l->pri > r->pri) {
            l->r = merge(l->r, r);
            l->size();
            return l;
        } else {
            r->l = merge(l, r->l);
            r->size();
            return r;
        }
    }

    void _insert(Node *&t, int x) {
        Node *l, *r, *m;
        split(t, x, l, r);
        split(l, x - 1, l, m);

        if (m) {
            m->cnt++;
            m->size();
        } else {
            m = new Node(x);
        }

        t = merge(l, m);
        t = merge(t, r);
    }

    void _del(Node *&t, int x) {
        if (!t)
            return;

        if (t->val == x) {
            if (t->cnt > 1) {
                t->cnt--;
                t->size();
            } else {
                t = merge(t->l, t->r);
            }
        } else if (x < t->val) {
            _del(t->l, x);
            t->size();
        } else {
            _del(t->r, x);
            t->size();
        }
    }

    int _rank(Node *t, int x) {
        if (!t)
            return 1;

        if (x < t->val) {
            return _rank(t->l, x);
        } else if (x == t->val) {
            return (t->l ? t->l->siz : 0) + 1;
        } else {
            return (t->l ? t->l->siz : 0) + t->cnt + _rank(t->r, x);
        }
    }

    int _kth(Node *t, int k) {
        if (!t)
            return -1;

        int ls = t->l ? t->l->siz : 0;

        if (k <= ls) {
            return _kth(t->l, k);
        } else if (k <= ls + t->cnt) {
            return t->val;
        } else {
            return _kth(t->r, k - ls - t->cnt);
        }
    }

    int _prev(Node *t, int x) {
        if (!t)
            return -inf;

        if (t->val >= x) {
            return _prev(t->l, x);
        } else {
            int p = _prev(t->r, x);
            return p > t->val ? p : t->val;
        }
    }

    int _next(Node *t, int x) {
        if (!t)
            return inf;

        if (t->val <= x) {
            return _next(t->r, x);
        } else {
            int n = _next(t->l, x);
            return n < t->val ? n : t->val;
        }
    }

public:
    Treap() : root(nullptr) {}

    void insert(int x) {
        _insert(root, x);
    }

    void del(int x) {
        _del(root, x);
    }

    int rank(int x) {
        return _rank(root, x);
    }

    int kth(int k) {
        return _kth(root, k);
    }

    int prev(int x) {
        return _prev(root, x);
    }

    int next(int x) {
        return _next(root, x);
    }
};

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int n;
    std::cin >> n;

    Treap t;

    for (int i = 0; i < n; i++) {
        int op, x;
        std::cin >> op >> x;
        if (op == 1) {
            t.insert(x);
        } else if (op == 2) {
            t.del(x);
        } else if (op == 3) {
            std::cout << t.rank(x) << "\n";
        } else if (op == 4) {
            std::cout << t.kth(x) << "\n";
        } else if (op == 5) {
            std::cout << t.prev(x) << "\n";
        } else if (op == 6) {
            std::cout << t.next(x) << "\n";
        }
    }
    return 0;
}
```
