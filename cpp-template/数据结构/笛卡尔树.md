---
topic: "笛卡尔树"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 笛卡尔树

* 每一个父节点等于子区间的最大值，可以 $O(1)$ 的复杂度解决RMQ问题
* 贪心，对一个数组中元素从大到小（或者从小到大）处理

* + 启发式合并
* 看左右子树的大小谁更小，则进行遍历，这样的复杂度就是 O(n logn)


```C++
// 大的为根
template <typename T, typename _Compare = greater<T>> // less<T>
struct descartes_tree {
  public:
    struct Node {
        int l = 0, r = 0;
        T val;
        Node() = default;
    };
    int n, root = 0, res = 0;
    vector<Node> v;
    vector<int> sz;
    _Compare comp;
 
    descartes_tree() = default;
    descartes_tree(const vector<T> &a) : n(a.size() - 1), v(n + 1), sz(n + 1, 1) {
        stack<int> st;
        for (int i = 1; i <= n; i++) {
            v[i].val = a[i];
            while (!st.empty()) {
                const auto &pos = st.top();
                if (comp(v[i].val, a[pos])) {
                    v[i].l = pos;
                    st.pop();
                } else { break; }
            }
            if (!st.empty()) {
                const auto &pos = st.top();
                v[pos].r = i;
            } else {
                root = i;
            }
            st.push(i);
        }
    }
    const T operator[](int i) const { return v[i].val; }
    void dfs_sz() {
        dfs_sz(root);
        return;
    }
    void dfs_sz(int u) {
        if (v[u].l) { dfs_sz(v[u].l); }
        if (v[u].r) { dfs_sz(v[u].r); }
        sz[u] += sz[v[u].l] + sz[v[u].r];
        return;
    }
    void dfs() {
        sz[0] = 0;
        dfs_sz(root);
        dfs(root, 1, n);
        return;
    }
    void dfs(int u, int dep, int cnt) {
        int L = u - sz[v[u].l];
        int R = u + sz[v[u].r];
        int mid = u;
        return;
    }
};

void solve()
{
    int n;
    cin >> n;
    vector<int> a(n + 1);
    cin >> a;
    descartes_tree<int> tr(a);

    tr.sz[0] = 0;
    tr.dfs_sz();

    vector<int> B(n + 1);
    unordered_map<int, vector<int>> pos;
    for (int i = 1; i <= n; i++) {
        B[i] = (a[i] % 2 == 0) ? a[i] : -a[i];
    }
    for (int i = 1; i <= n; i++) {
        pos[B[i]].push_back(i);
    }
    for (auto &[x, vec] : pos) {
        sort(range(vec));
    }

    int ans = 0;
    Y_combinator dfs = [&](auto &&self, int u) -> void {
        int L = u - tr.sz[tr.v[u].l];
		int R = u + tr.sz[tr.v[u].r];
		int mid = u;

        int k = a[u];
        vector<int> vec = {k + 1, -(k + 1), 0};

        int sum = (mid - L + 1) * (R - mid + 1);

        if (mid - L <= R - mid) {
            for (int i = mid; i >= L; i--) {
                for (auto &x : vec) {
                    int tar = x - B[i];

                    int lo = lower_bound(range(pos[tar]), mid) - pos[tar].begin();
                    int hi = upper_bound(range(pos[tar]), R) - pos[tar].begin();

                    int num = hi - lo;

                    sum -= num;
                }
            }
        } else {
            for (int i = R; i >= mid; i--) {
                for (auto &x : vec) {
                    int tar = x - B[i];

                    int lo = lower_bound(range(pos[tar]), L) - pos[tar].begin();
                    int hi = upper_bound(range(pos[tar]), mid) - pos[tar].begin();

                    int num = hi - lo;

                    sum -= num;
                }
            }
        }
        ans += sum;

        if (tr.v[u].l) self(tr.v[u].l);
        if (tr.v[u].r) self(tr.v[u].r);
    } ;

    dfs(tr.root);

    cout << ans * 2 - n << endl;
}

```
