---
topic: "Trie 树"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## Trie 树

### (1) 异或树

```C++
template<unsigned int sz, typename T = int>
struct Binary_trie {
  public:
    using Bit = typename conditional<sz <= 32, unsigned int, unsigned long long>::type;
    struct node {
        T cnt;
        array<int, 2> nxt;
        node(): cnt(0), nxt({-1, -1}) { }
    };
    vector<node> v;
    int root;
    Binary_trie() { 
        v.emplace_back(); root = 0; 
    }
    // 插入一个数 x
    void insert(Bit x) { add(x, 1); }
    // 删除一个数 x，需保证确实插入过
    void erase(Bit x) { add(x, -1); }
    // 通用的 add：把 x 在字典树中出现次数加上 k
    void add(Bit x, T k) {
        assert(0 <= x && (x >> sz) == 0);
        int p = 0;
        v[p].cnt += k;
        for (int i = sz; i--; ) {
            int j = x >> i & 1;
            if (v[p].nxt[j] == -1) {
                v[p].nxt[j] = v.size();
                v.emplace_back();
            }
            p = v[p].nxt[j];
            v[p].cnt += k;
        }
        // 叶节点也会有 cnt 增加
    }

    // count(x, xor_val) 返回 trie 中满足 (y xor xor_val) < x 的 y 的个数
    T count(Bit x, Bit xor_val = 0) const {
        assert(0 <= xor_val && (xor_val >> sz) == 0);
        if (x < 0) return 0;
        else if (x >> sz) return v[0].cnt;
        T ans = 0;
        int p = root;
        for (int i = sz; i--; ) {
            int j = x >> i & 1;
            int k = xor_val >> i & 1;
            if (j == 0) {
                p = v[p].nxt[k];
            } else {
                if (v[p].nxt[k] >= 0) ans += v[v[p].nxt[k]].cnt;
                p = v[p].nxt[!k];
            }
            if (p == -1) break;
        }
        return ans;
    }

    // max(xor_val)：返回 max_{y in trie} (y xor xor_val)
    // 返回的是最大值（按数值），范围 [0, 2 ^ sz)
    Bit max(Bit xor_val = 0) const {
        assert(0 <= xor_val && (xor_val >> sz) == 0);
        int p = 0;
        Bit ans = 0;
        for (int i = sz; i--; ) {
            ans <<= 1;
            int k = xor_val >> i & 1;
            if (v[p].nxt[!k] >= 0 && v[v[p].nxt[!k]].cnt > 0) {
                p = v[p].nxt[!k];
                ans |= 1;
            } else {
                p = v[p].nxt[k];
            }
        }
        return ans;
    }
    // min(xor_val)：返回 min_{y in trie} (y xor xor_val)
    Bit min(Bit xor_val = 0) const {
        assert(0 <= xor_val && (xor_val >> sz) == 0);
        int p = 0;
        Bit ans = 0;
        for (int i = sz; i--; ) {
            ans <<= 1;
            int k = xor_val >> i & 1;
            if (v[p].nxt[k] >= 0 && v[v[p].nxt[k]].cnt > 0) p = v[p].nxt[k];
            else {
                p = v[p].nxt[!k];
                ans |= 1;
            }
        }
        return ans;
    }
    // find_by_order(ord, xor_val)：返回按 (value xor xor_val) 排序的第 ord 个元素（0-based）
    // 返回的是该元素的 (value xor xor_val) 值（不是原始 y），范围 [0, 2^sz)
    Bit find_by_order(T ord, Bit xor_val = 0) const {
        assert(0 <= xor_val && (xor_val >> sz) == 0);
        assert(0 <= ord && ord < v[0].cnt); // ord 必须小于元素总数
        int p = 0;
        Bit ans = 0;
        for (int i = sz; i--; ) {
            ans <<= 1;
            int k = xor_val >> i & 1;
            // 先看 v[p].nxt[k]（使当前位为0的那侧）有多少元素
            if (v[p].nxt[k] >= 0) {
                if (ord >= v[v[p].nxt[k]].cnt) {
                    // 第 ord 个元素不在这侧，跳过这侧的所有元素数量
                    ord -= v[v[p].nxt[k]].cnt;
                    p = v[p].nxt[!k];
                    ans |= 1;
                } else {
                    // 第 ord 个就在这侧
                    p = v[p].nxt[k];
                }
            } else {
                // 没有这侧，必然去另一侧
                p = v[p].nxt[!k];
                ans |= 1;
            }
        }
        return ans;
    }
    // 返回小于 x 的元素个数（按 y^xor_val 比较）
    T order_of_key(Bit x, Bit xor_val = 0) const { return count(x, xor_val); }
};

```

```C++
// 例：经典 —— 统计 i<j 且 (ai xor aj) < K 的对数
// 遍历数组，当前元素与已插入元素配对
void solve() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; long long K;
    cin >> n >> K;
    binarytrie<30, long long> P;
    long long ans = 0;
    for (int i = 0; i < n; ++i) {
        int a; cin >> a;
        // 统计已有的 y 满足 (y xor a) < K
        ans += P.count((unsigned)K, (unsigned)a);
        // 然后把当前 a 插入（供后续元素配对）
        P.insert((unsigned)a);
    }
    cout << ans << '\n';
}
```

```C++
// 例：最大异或对 (maximum xor pair)
// 给定数组，求 i<j 使 ai xor aj 最大的值
void solve() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    binarytrie<30, long long> P;
    long long best = 0;
    if (n == 0) { cout << 0 << '\n'; return; }
    int a; cin >> a;
    P.insert((unsigned)a); // 插入第一个
    for (int i = 1; i < n; ++i) {
        cin >> a;
        // P.max(a) 返回已插入元素 y 中最大 (y xor a)
        best = max(best, (long long)P.max((unsigned)a));
        P.insert((unsigned)a);
    }
    cout << best << '\n';
}

```

### (2) 字典树

```C++
#undef int
// 用 -1 表示 "no_child"
struct Trie {
  public:
    int MAXN = 2000010;
    vector<array<int, 26>> tr;
    vector<int> cnt, tail, chi_cnt; 
    // cnt[root] = 已插入字符串的总次数
    // tail 恰好在节点 p 结束的字符串数量
    // chi_cnt 节点 p 有多少个不同的子字母方向
    int idx;
    int root;
    vector<int> used;
    Trie(int MAXN_ = 2000010) {
        MAXN = MAXN_;
        tr.resize(MAXN);
        cnt.assign(MAXN, 0); tail.assign(MAXN, 0); chi_cnt.assign(MAXN, 0);
        used.clear();
        idx = 1; root = 0;
        used.push_back(root);
        memset(tr[root].data(), -1, 26 * sizeof(int));
        cnt[root] = tail[root] = chi_cnt[root] = 0;
    }
    ~Trie() {
        for (int x : used) {
            memset(tr[x].data(), -1, 26 * sizeof(int));
            cnt[x] = tail[x] = chi_cnt[x] = 0;
        }
        used.clear();
    }
    inline int new_node() {
        int id = idx++;
        if (id >= MAXN) {
            int old = MAXN;
            MAXN <<= 1;
            tr.resize(MAXN); cnt.resize(MAXN); tail.resize(MAXN); chi_cnt.resize(MAXN);
        }
        used.push_back(id);
        memset(tr[id].data(), -1, 26 * sizeof(int));
        cnt[id] = 0; tail[id] = 0; chi_cnt[id] = 0;
        return id;
    }
    void insert(const string &s) {
        int p = root;
        ++cnt[p];
        for (char ch : s) {
            int c = ch - 'a';
            if (tr[p][c] == -1) {
                tr[p][c] = new_node();
                chi_cnt[p]++;
            }
            p = tr[p][c];
            ++cnt[p];
        }
        tail[p]++;
    }
    int query(const string &s) {
        int p = root, ans = 0;
        for (char ch : s) {
            int c = ch - 'a';
            p = tr[p][c];
            if (p == -1) return ans;
            ans += cnt[p];
        }
        return ans;
    }
    inline array<int,26> & operator[](int p) { return tr[p]; }
    inline const array<int,26>& operator[](int p) const { return tr[p]; }
};
#define int long long
```

* 查询最长公共前缀的数组的模板

```C++
class Trie {
    static constexpr int MAXN = 2e6 + 10;
    static constexpr int S = 26;
  public:
    #undef int long long
    int n, idx;
    static int tr[MAXN][S];
    static int cnt[MAXN];
    Trie() {
        idx = 1;
    }
    ~Trie() {
        clear();
    }
    int newNode() {
        int x = ++idx;
        fill(tr[x], tr[x] + S, 0);
        cnt[x] = 0;
        return x;
    }
    void insert(vector<i64>& s) {
        int c, p = 1;
        for (int i = 1; i < s.size(); i++) {
            c = s[i];
            if (!tr[p][c]) {
                tr[p][c] = newNode();
            }
            p = tr[p][c];
        }
    }
    int query(vector<i64>& s) {
        int c, p = 1, ans = 0;
        for (int i = 1; i < s.size(); i++) {
            c = s[i];
            p = tr[p][c];
            if (!p) return ans;
            ans ++;
        }
        return ans;
    }
    void clear() {
        for (int i = 1; i <= idx; i++) {
            fill(tr[i], tr[i] + S, 0);
        }
        idx = 1;
    }
};
int Trie::tr[MAXN][S];
int Trie::cnt[MAXN];
#define int long long

void solve()
{
    int n, m;
    cin >> n >> m;
    vector<vector<int>> a(n + 1, vector<int>(m + 1));
    Trie trie;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> a[i][j];
        }
    }
    for (int i = 1; i <= n; i++) {
        vector<int> b(m + 1);
        for (int j = 1; j <= m; j++) b[a[i][j]] = j;  // 构造 a[i] 的逆
        trie.insert(b);
    }
    for (int i = 1; i <= n; i++) {
        int ans = trie.query(a[i]);
        cout << ans << ' ';
    }
    cout << endl;
}
```
