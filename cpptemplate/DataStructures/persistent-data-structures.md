---
topic: "可持久化数据结构"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 可持久化数据结构

### 可持久化线段树（主席树）

#### 根据权值建树

```C++
namespace persistent_segment_tree {
    struct node {
        node *l = nullptr;
        node *r = nullptr;
        int cnt = 0;
    };
    
    node *insert(node *t, int l, int r, int x) {
        if (t) t = new node(*t);
        else t = new node;
        
        t->cnt++;
        if (r - l == 1) { return t; }
    
        int m = l + r >> 1;
        if (x <= m) {
            t->l = insert(t ? t->l : nullptr, l, m, x);
        } else {
            t->r = insert(t ? t->r : nullptr, m + 1, r, x);
        }
        return t;
    }

    inline int cnt(node* t) { return t ? t->cnt : 0; }
    //
    int count_leq(node* t1, node* t2, int l, int r, int x) {
        if (cnt(t2) - cnt(t1) == 0 || l > x) return 0;
        if (r <= x) {
            return cnt(t2) - cnt(t1);
        }

        int m = l + r >> 1;
        return count_leq(t1 ? t1->l : nullptr, t2 ? t2->l : nullptr, l, m, x)
             + count_leq(t1 ? t1->r : nullptr, t2 ? t2->r : nullptr, m + 1, r, x);
    }
    
    int kth(node* t1, node* t2, int l, int r, int k) {
        if (l == r) return l; 

        int m = l + r >> 1;
        int left = cnt(t2 ? t2->l : nullptr) - cnt(t1 ? t1->l : nullptr);
    
        if (k <= left) {
            return kth(t1 ? t1->l : nullptr, t2 ? t2->l : nullptr, l, m, k);
        }
        return kth(t1 ? t1->r : nullptr, t2 ? t2->r : nullptr, m+1, r, k - left);
    }
    
    int max_less(node* t1, node* t2, int l, int r, int x) {
        if (cnt(t2) - cnt(t1) == 0 || l >= x) return -1;
        if (l == r) return l;
        int m = l + r >> 1;
        int res = max_less(t1 ? t1->r : nullptr, t2 ? t2->r : nullptr, m+1, r, x);
        if (res == -1) {
            res = max_less(t1 ? t1->l : nullptr, t2 ? t2->l : nullptr, l, m, x);
        }
        return res;
    }

    int get_max(node* t, int l, int r) {
        if (!t || t->cnt == 0) return -1; 
        
        if (l == r) return l; 
        
        int m = l + r >> 1;
        if (cnt(t->r) > 0) {
            return get_max(t->r, m + 1, r);
        }  else {
            return get_max(t->l, l, m);
        }
    }
}
namespace pst = persistent_segment_tree;
```

#### (2) 根据原数组下标建树

```C++
namespace persistent_segment_tree {
    const int MAX_NODE = 1200000;
    struct Node {
        int l = 0;
        int r = 0;
        i64 max_a = -INF;
        i64 max_b = -INF;
    } tr[MAX_NODE];
    
    int idx = 0;
    int n_ = 0;
    
    inline void pull(int p) {
        int l = tr[p].l, r = tr[p].r;
        tr[p].max_a = max(l ? tr[l].max_a : -INF, r ? tr[r].max_a : -INF);
        tr[p].max_b = max(l ? tr[l].max_b : -INF, r ? tr[r].max_b : -INF);
    }

    int build(int l, int r, const vector<int>& b) {
        int p = ++idx; // 申请新节点
        if (l == r) {
            tr[p].max_a = -INF;
            tr[p].max_b = b[l];
            return p;
        }
        int m = (l + r) >> 1LL;
        tr[p].l = build(l, m, b);
        tr[p].r = build(m + 1, r, b);
        pull(p);
        return p;
    }

    int init(const vector<int>& b) {
        n_ = b.size() - 1; 
        idx = 0; 
        return build(1, n_, b);
    }
    
    int update(int p, int l, int r, int pos, i64 v) {
        int q = ++idx; 
        tr[q] = tr[p];
        if (l == r) {
            tr[q].max_a = v;
            tr[q].max_b = -INF;
            return q;
        }
        int m = (l + r) >> 1LL;
        if (pos <= m) {
            tr[q].l = update(tr[p].l, l, m, pos, v);
        } else {
            tr[q].r = update(tr[p].r, m + 1, r, pos, v);
        }
        pull(q);
        return q;
    }

    pair<i64, i64> query(int p, int l, int r, int ql, int qr) {
        if (!p || ql > r || qr < l) {
            return {-INF, -INF};
        }
        if (ql <= l && r <= qr) {
            return {tr[p].max_a, tr[p].max_b};
        }
        
        int m = (l + r) >> 1LL;
        auto L = query(tr[p].l, l, m, ql, qr);
        auto R = query(tr[p].r, m + 1, r, ql, qr);

        return {max(L.first, R.first), max(L.second, R.second)};
    }
}
namespace pst = persistent_segment_tree;


vector<int> tr(n + 1, 0); 
tr[0] = pst::init(b);

for (int i = 1; i <= n; i++) {
    auto [ai, bi, it] = vec[i];
    tr[i] = pst::update(tr[i - 1], 1, n, it, ai);
}

vector<int> ans(q + 1);
for (int i = 1; i <= q; i++) {
    int l, r, X, Y;
    cin >> l >> r >> X >> Y;
    int x = X ^ ans[i - 1], y = Y ^ ans[i - 1];

    int k = lower_bound(range_(d), y - x) - d.begin() - 1;

    auto [A, B] = pst::query(tr[k], 1, n, l, r);
    int res = -INF;
    if (A != -INF) res = max(res, A + x);
    if (B != -INF) res = max(res, B + y);

    ans[i] = res;
    cout << ans[i] << '\n';
}
```

### 分块
#### (1) 区间加 + 单点查询
```C++
template<class T>
struct block {
  public:
    int n, siz, cnt;
    vector<int> bel;
    vector<T> a, tag;

    block() {}
    block(const vector<T>& init_) {
        init(init_);
    }
    void init(const vector<T>& init_) {
        n = init_.size() - 1;
        siz = sqrt(n);
        cnt = (n + siz - 1) / siz;
        a.resize(n + 1);
        tag.assign(cnt + 1, 0);
        bel.resize(n + 1);
        for (int i = 1; i <= n; i++) {
            bel[i] = (i - 1) / siz + 1;
            a[i] = init_[i];
        }
    }
    
    void set(int i, T val) {
        a[i] = val;
    }
    void add(int l, int r, T d) {
        for (int i = l; i <= min(bel[l] * siz, r); i++) {   // 左
            a[i] += d;
        }
        if (bel[l] != bel[r]) {
            for (int i = (bel[r] - 1) * siz + 1; i <= r; i++) {   // 右
                a[i] += d;
            }
        }
        for (int i = bel[l] + 1; i <= bel[r] - 1; i++) {   // 中
            tag[i] += d;
        }
    }
    T query(int x) {
        return a[x] + tag[bel[x]];
    }
};
```

#### (2) Bitset 状压分块

**0-base**
```C++
struct BitInfo {  // 16
  public:
    int pre = 0;  // 前缀1
    int suf = 0;  // 后缀1
    int len = 0;  // 中间的贡献
    BitInfo(): pre(0), suf(0), len(0) { }
    BitInfo(int pre_, int suf_, int cnt_): pre(pre_), suf(suf_), len(cnt_) { }
};
vector<BitInfo> info(1 << 16);

void init() { // 预处理某个16位二进制串中的前缀1，后缀1，以及中间子段1 的贡献
    for (int x = 0; x < (1 << 16); x++) {
        for (int i = 0; i < 16; i++) {
            if (x >> i & 1) info[x].pre++;
            else break;
        }
        for (int i = 15; i >= 0; i--) {
            if (x >> i & 1) info[x].suf++;
            else break;
        }
        for (int i = 0, j = 0; i < 16; i++) {
            j = (x >> i & 1) ? j + 1 : 0;
            info[x].len += j;
        }
    }
}

void update(int cur, int &suffix, u64 &ans) {
// 线性处理某个 01 串中有多少个贡献
    ans += suffix * info[cur].pre + info[cur].len;
    suffix = suffix * (info[cur].suf >> 4LL) + info[cur].suf;
}

struct Bitset: vector<u64> {
  public:
    int n, ptr;
    Bitset(): Bitset(0) { }
    Bitset(int sz_): std::vector<u64>((sz_ + 63) >> 6, 0), n(sz_), ptr(0) { }
    
    static inline u64 mask(int l, int r) {   // 64 位内掩码
        u64 res = (r == 63) ? ~0ULL : (1ULL << (r + 1)) - 1;
        res ^= (1ULL << l) - 1;
        return res;
    }
    void add(int len, u64 val) {   // 相当于push_back()
        if (len <= 64 - (ptr & 63)) {
            (*this)[ptr >> 6] |= val << (ptr & 63);
        } else {
            u64 m = mask(0, 64 - (ptr & 63) - 1);
            (*this)[ptr >> 6] |= (val & m) << (ptr & 63);
            (*this)[(ptr >> 6) + 1] = val >> (64 - (ptr & 63));
        }
        ptr += len;
    }
	// 从某个 01 串中扣出来 l ~ r 的部分
    static Bitset extract(const Bitset &cur, int l, int r) {
        Bitset res(r - l + 1);
        if ((l >> 6) == (r >> 6)) {
            u64 val = (cur[l >> 6] & mask(l & 63, r & 63)) >> (l & 63);
            res.add(r - l + 1, val);
        } else {
            u64 val = (cur[l >> 6] & mask(l & 63, 63)) >> (l & 63);
            res.add(63 - (l & 63) + 1, val);
            for (int i = (l >> 6) + 1; i < (r >> 6); i++) res.add(64, cur[i]);
            val = cur[r >> 6] & mask(0, r & 63);
            res.add((r & 63) + 1, val);  //  从本块第 0 位到 (r&63) 位，共 (r&63)+1 位
        }
        return res;
    }

    void equal(const Bitset &cur) {  // 相等取 1，不等取 0
        int m = min((*this).size(), cur.size());
        for (int i = 0; i < m; i++) {
            (*this)[i] ^= ~cur[i];
        }
        m = min(cur.n, n);
        for (int i = n >> 6; i < (*this).size(); i++) {
            int l = max(0LL, m - (i << 6LL));
            int r = 63;
            (*this)[i] &= ~mask(l, r);
        }
    }

    u64 calc() const {
    // 线性处理某个 01 串中有多少个贡献
        u64 res = 0;
        int M = 1 << 16;
        for (int i = 0, ri = 0; i < (*this).size(); i++) {
        
            update((*this)[i] & (M - 1), ri, res);
            update((*this)[i] >> 16 & (M - 1), ri, res);
            update((*this)[i] >> 32 & (M - 1), ri, res);
            update((*this)[i] >> 48 & (M - 1), ri, res);
        }
        return res;
    }

    friend std::ostream& operator<<(std::ostream& os, const Bitset& bs) {
        for (int i = 0; i < bs.n; i++) {
            int block = i >> 6;
            int off = i & 63;
            os << (((bs[block] >> off) & 1) ? '1' : '0');
        }
        return os;
    }
};
```

**Flip 翻转字符串 使用前缀和异或来标记**
```C++
	l--, r --;
	if ((l >> 6) == (r >> 6)) {
		b[l >> 6] ^= Bitset::mask(l & 63, r & 63); 
	} else {
		b[l >> 6] ^= Bitset::mask(l & 63, 63);
		b[r >> 6] ^= Bitset::mask(0, r & 63);
		tag[(l >> 6) + 1] ^= 1;
		tag[r >> 6] ^= 1;
	}
```

**更新懒标记 不断下传**
```C++
	for (int i = 0, pre = 0; (i << 6) < n; i++) {
		tag[i] ^= pre;
		if (tag[i]) b[i] ^= -1ULL;
		pre = tag[i];
		tag[i] = 0;
	}
```
