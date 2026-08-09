---
topic: "树论"
category: "08-graph"
source: "图论 Graph.md"
---

# 树论

## Trick

* 树上集合的划分（组合数学/容斥）

	把“与某条路径/某些节点有关的所有连通子集”按在路径上最**靠近某固定点**（例如 LCA、端点或路径上第一个交点）的节点划分，每个子集都有唯一的代表点，从而把复杂的全局计数化成若干个“在某条边/某个子树内且必须包含某点”的局部计数之和，做到不重不漏。

* 两个数的关系如果是 $a_i = \lfloor \frac{a_{i + 1}}{2} \rfloor$  OR $a_{i + 1} = \lfloor \frac{a_{i}}{2} \rfloor$

	可以看作树 也就是 $a_{i + 1} = \lfloor \frac{a_{i}}{2} \rfloor, 2a_i$, or $2a_{i+1}$.

	$a_i → a_{i+1}$ 实质是在满二叉树上走了一条边，eg: $3 → 9$

	在满二叉树上求解LCA的函数模板如下：

```C++
vector<int> path(int x, int y) {
    vector<int> L, R;
    while (__lg(x) > __lg(y)) {
        L.push_back(x);
        x >>= 1;
    }
    while (__lg(y) > __lg(x)) {
        R.push_back(y);
        y >>= 1;
    }
    while (x != y) {
        L.push_back(x); R.push_back(y);
        x >>= 1; y >>= 1;
    }
    L.push_back(x);
    reverse(R.begin(), R.end());
    for (auto x : R) L.push_back(x);
    return L;
}
```

* 树上的每条路径唯一地用“两个端点”来表示，重新排列路径上的所有点，因为一条路径在树中是唯一的，所以只要保证 **两个端点都不在原位置**，路径就不会和别的方案重叠；同时，每条路径都会被这种端点对表示法覆盖一次，不会漏。

* 求解 树上 **k 条路经的公共路径**，树上的路径交集是有传递性的，说白了就是按照顺序两条两条地维护就行，求解 **两条路径的相交关系可以枚举他们端点的四组 LCA**。


## 前序`pre-order`和中序`in-order` / 后序`post-order`和中序`in-order` 建二叉树

```C++
vector<int> pre(n + 1), in(n + 1), post(n + 1);
map<int, int> pos, l, r;
for (int i = 1; i <= n; i++) cin >> pre[i];
for (int i = 1; i <= n; i++) cin >> in[i], pos[in[i]] = i;
for (int i = 1; i <= n; i++) cin >> post[i];

auto build_post = [&](auto && self, int il, int ir, int postl, int postr) -> int {
    int root = post[postr];
    int k = pos[root];
    int len = k - il;
    if (k > il) l[root] = self(self, il, k - 1, postl, postl + len - 1);
    if (k < ir) r[root] = self(self, k + 1, ir, postl + len, postr - 1);
    return root;
};

auto build_pre = [&](auto && self, int il, int ir, int prel, int prer) -> int {
    int root = pre[prel];
    int k = pos[root];
    int len = k - il;
    if (k > il) l[root] = self(self, il, k - 1, prel + 1, prel + len);
    if (k < ir) r[root] = self(self, k + 1, ir, prel + len + 1, prer);
    return root;
};
int root = build_post(build_post, 1, n, 1, n);
```

## 判断一个点 x 是否在路径 (u, v) 上

```C++
auto get_dist = [&](int u, int v) {
	if (u == 0 || v == 0) return 0LL;
	return dep[u] + dep[v] - 2 * dep[lca(u, v)];
};

auto is_on_path = [&](int x, int u, int v) {
	if (x == 0) return false;
	// 点 x 在路径 u-v 上的充要条件
	return get_dist(u, x) + get_dist(x, v) == get_dist(u, v);
};
```

## 树上倍增求 lca

```c++
vector<int> p(n + 1), dep(n + 1);
vector<array<int, 22>> st(n + 1);
Y_combinator dfs = [&](auto &&dfs, int u, int fa) -> void {
	p[u] = fa;
	dep[u] = dep[fa] + 1;
	st[u][0] = p[u];
	for (int i = 1; i <= __lg(dep[u]); i++) {
		st[u][i] = st[st[u][i - 1]][i - 1];
	}
	for (auto v : e[u]) {
		if (v == fa) continue;
		dfs(v, u);
	}
};
dfs(1, 0);

auto lca = [&](int u, int v) -> int {
	if (dep[u] < dep[v]) { swap(u, v); }
	while (dep[u] > dep[v]) {
		u = st[u][__lg(dep[u] - dep[v])];
	}
	if (u == v) { return u; }
	for (int i = __lg(dep[u]); i >= 0; i--) {
		if (st[u][i] != st[v][i]) {
			u = st[u][i]; v = st[v][i];
		}
	}
	return p[u];
};

```


## 欧拉序列

```C++
    vector<int> path, in(n + 1), out(n + 1);
    vector<vector<int>> up(n + 1, vector<int>(25, 0));
    int cur = 1;
    g[0] = 0;
    Y_combinator dfs_2 = [&](auto &&self, int u) -> void {
        in[u] = path.size();
        cur++;
        up[u][0] = p[u];
        for (int i = 1; i <= 20; i++) {   // 倍增
            up[u][i] = up[up[u][i - 1]][i - 1];
        }
        g[u] = g[p[u]] + f[u];
        path.push_back(u);
        for (auto v : e[u]) {
            self(v);
            path.push_back(u);
        }
    };
    dfs_2(1);
```

## 重链剖分 (Heavy-Light Decomposition, HLD)

* 可解决 **LCA** 问题
* 可解决 **Kth 祖先** 问题

```C++
int n;                      // 节点总数（节点编号范围为 1 ~ n）
vector<int> siz;            // siz[u]: 以 u 为根的子树大小
vector<int> top;            // top[u]: u 所在链的顶端节点（链顶）
vector<int> dep;            // dep[u]: u 的深度（根的深度为 0）
vector<int> parent;         // parent[u]: u 的父节点（根的 parent 为 -1）
vector<int> in;             // in[u]: 节点 u 在 DFS（欧拉）序中的序号（1-based）
vector<int> out;            // out[u]: 节点 u 子树在 DFS 序中的结束序号（区间 [in[u], out[u]]）
vector<int> seq;            // seq[i]: DFS 序中第 i 个节点的编号（1-based i）
vector<vector<int>> e;      // 邻接表，e[u] 为 u 的所有邻接节点（节点编号均为 1-based）
int cur;                    // 当前 DFS 序号计数器，初始值设为 1
```


```C++
struct HLD {
  public:
	int n;
	std::vector<int> siz, top, dep, parent, in, out, seq;
	std::vector<std::vector<int>> e;
	int32_t cur;
    HLD() noexcept : n(0), cur(1) { }
    explicit HLD(int _n) { init(_n); }
    void init(int n) {
        this->n = n;
        siz.assign(n + 1, 0); top.assign(n + 1, 0);
        dep.assign(n + 1, 0); parent.assign(n + 1, 0);
        in.assign(n + 1, 0); out.assign(n + 1, 0);
        seq.assign(n + 1, 0);
        cur = 1; // DFS 序号从 1 开始
        e.assign(n + 1, std::vector<int>());
    }
    void add_edge(int u, int v) {
        e[u].push_back(v); e[v].push_back(u);
    }
    void work(int root = 1) {
        top[root] = root;      // 根节点所在链的链顶就是根本身
        dep[root] = 0;         // 根节点深度为 0
        parent[root] = -1;
        dfs_1(root); dfs_2(root);
    }
    void dfs_1(int u) {
        if (parent[u] != -1) {
            e[u].erase(std::find(range(e[u]), parent[u]));
        }
        siz[u] = 1;
        for (auto &v : e[u]) {
            parent[v] = u;
            dep[v] = dep[u] + 1LL;
            dfs_1(v);
            siz[u] += siz[v];
            // e[u][0] 始终为 u 的重儿子（子树最大的儿子）
            if (siz[v] > siz[e[u][0]]) std::swap(v, e[u][0]);
        }
    }
    void dfs_2(int u) {
        in[u] = cur;
        seq[cur] = u;
        cur++;
        for (auto v : e[u]) {
            top[v] = (v == e[u][0] ? top[u] : v);
            dfs_2(v);
        }
        // u 子树内所有节点的 DFS 序号都在区间 [in[u], out[u]] 内
        out[u] = cur - 1LL;
    }
    int dfn(int u) { return in[u]; }
    // u 和 v 的 LCA
    int lca(int u, int v) {
        while (top[u] != top[v]) {
            if (dep[top[u]] > dep[top[v]]) { u = parent[top[u]]; } 
            else { v = parent[top[v]]; }
        }
        return dep[u] < dep[v] ? u : v;
    }
    //  u 与 v 之间的距离
    int dist(int u, int v) {
        return dep[u] + dep[v] - 2 * dep[lca(u, v)];
    }
    // 从节点 u 出发向上跳 k 个祖先，返回目标节点，返回 -1 表示不存在
    int jump(int u, int k) {
        if (dep[u] < k) {
            return -1;
        }
        int d = dep[u] - k;
        while (dep[top[u]] > d) { u = parent[top[u]]; }
        return seq[in[u] - (dep[u] - d)];
    }
    // 判断 u 是否是 v 的祖先
    bool is_ancester(int u, int v) {
        return in[u] <= in[v] && in[v] <= out[u];
    }
    // rooted_parent(u, v): 返回 u 和 v 在以某节点为根的树中，u 的父节点
    int rooted_parent(int u, int v) {
        std::swap(u, v);
        if (u == v) {
            return u;
        }
        if (!is_ancester(u, v)) {
            return parent[u];
        }
        auto it = upper_bound(range(e[u]), v, [&](int x, int y) {
            return in[x] < in[y];
        }) - 1;
        return *it;
    }
    // rootedSize(u, v): 返回在以某节点为根的树中，v 所在子树的大小
    int rootedSize(int u, int v) {
        if (u == v) {
            return n;
        }
        if (!is_ancester(v, u)) {
            return siz[v];
        }
        return n - siz[rooted_parent(u, v)];
    }
    // rooted_Lca(a, b, c): 根据三个节点求一个特殊的 LCA 结果（异或操作）
    int rooted_Lca(int a, int b, int c) {
        return lca(a, b) ^ lca(b, c) ^ lca(c, a);
    }
};

auto update_path = [&](int u, int v, int w) -> void {
	while (tr.top[u] != tr.top[v]) {
		if (tr.dep[tr.top[u]] < tr.dep[tr.top[v]]) std::swap(u, v);
		seg.update(tr.in[tr.top[u]], tr.in[u], w);
		u = tr.parent[tr.top[u]];
	}
	if (tr.dep[u] > tr.dep[v]) std::swap(u, v);
	seg.update(tr.in[u], tr.in[v], w);
};
auto path_query = [&](int u, int v) -> int {
	int res = 0;
	while (tr.top[u] != tr.top[v]) {
		if (tr.dep[tr.top[u]] < tr.dep[tr.top[v]]) std::swap(u, v);
		res += seg.query(tr.in[tr.top[u]], tr.in[u]);
		u = tr.parent[tr.top[u]];
	}
	if (tr.dep[u] > tr.dep[v]) std::swap(u, v);
	res += seg.query(tr.in[u], tr.in[v]);
	return res;
};
```

#### 关于树上修改子树中的所有颜色 以及 查询子树中不同颜色的例题

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
};

struct HLD {
	int n;
	vector<int> siz, top, dep, parent, in, out, seq;
	vector<vector<int>> e;
	int cur;
    HLD() { }
    HLD(int n) {
        init(n);
    }
    void init(int n) {
        this->n = n;
        siz.assign(n + 1, 0); top.assign(n + 1, 0);
        dep.assign(n + 1, 0); parent.assign(n + 1, 0);
        in.assign(n + 1, 0); out.assign(n + 1, 0);
        seq.assign(n + 1, 0);
        cur = 1; // DFS 序号从 1 开始
        e.assign(n + 1, vector<int>());
    }
    void addEdge(int u, int v) {
        e[u].push_back(v);
        e[v].push_back(u);
    }
    void work(int root = 1) {
        top[root] = root;      // 根节点所在链的链顶就是根本身
        dep[root] = 0;         // 根节点深度为 0
        parent[root] = -1;     // 设为 -1
        dfs1(root);
        dfs2(root);
    }
    void dfs1(int u) {
        if (parent[u] != -1) {
            e[u].erase(find(e[u].begin(), e[u].end(), parent[u]));
        }
        // 初始化 u 的子树大小为 1（包含 u 自身）
        siz[u] = 1;
        for (auto &v : e[u]) {
            parent[v] = u;
            dep[v] = dep[u] + 1;
            dfs1(v);
            siz[u] += siz[v];
            // e[u][0] 始终为 u 的重儿子（子树最大的儿子）
            if (siz[v] > siz[e[u][0]])
                swap(v, e[u][0]);
        }
    }
    void dfs2(int u) {
        in[u] = cur;
        seq[cur] = u;
        cur++;
        for (auto v : e[u]) {
            top[v] = (v == e[u][0] ? top[u] : v);
            dfs2(v);
        }
        // u 子树内所有节点的 DFS 序号都在区间 [in[u], out[u]] 内
        out[u] = cur - 1;
    }
};

struct Tag {
    int f = 0;
    Tag(int _f = 0): f(_f) { }
    void apply(const Tag &t) {
        if (t.f == 0) return; 
        f = t.f;
    }
};

struct Info {
    int x;
    vector<bool> num;
    Info(int x_ = 0) : x(x_) { 
        num.resize(61);
        if (x_ > 0) num[x_] = 1;
    }
    void apply(Tag t, int len) {
        if (t.f) {
            x = t.f;
            fill(range(num), 0LL);
            num[t.f] = (bool)len;
        }
    }
};

Info operator+(const Info &l, const Info &r) {
    Info u;
    for (int i = 1; i <= 60; i++) {
        u.num[i] = l.num[i] + r.num[i];
    }
    return u;
}

void solve()
{
    int n, m;
    cin >> n >> m;
    vector<int> col(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> col[i];
    }
    
    HLD tr(n );
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        tr.addEdge(u, v);
    }
    tr.work();
    vector<Info> info(n + 1);
    for (int i = 1; i <= n; i++) {
        int p = tr.in[i];
        vector<int> res(61, 0);
        res[col[i]] = 1;
        info[p] = Info(col[i]);
    }
    lazy_segment_tree<Info, Tag> seg(info);
    while (m--) {
        int op;
        cin >> op;
        if (op == 1) {
            int v, c;
            cin >> v >> c;
            seg.range_apply(tr.in[v], tr.out[v], Tag(c));
        } else {
            int v;
            cin >> v;
            int sum = 0;
            for (auto x : seg.range_query(tr.in[v], tr.out[v]).num) {
                if (x > 0) {
                    sum ++;
                }
            }
            cout << sum << endl;
        }
    }
}
```

## 克鲁斯卡尔重构树

```C++
void solve() {
    int n, m;
    cin >> n >> m;  // n 点 m 边
    vector<tuple<int, int, int, int>> e;
    for (int i = 1; i <= m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        e.push_back({w, u, v, i});
        // 边权w 端点u 端点v 编号i
    }
    sort(range(e));
    int sum = 0;  // MST 的最小权重和
    DSU dsu(2 * n + 1);
    int cnt = n + 1;
    vector<int> ans(m + 1), wt(2 * n + 1);
    HLD tr(2 * n + 1);
    for (auto &[w, u, v, i] : e) {
        if (dsu.same(u, v)) continue;
        tr.addEdge(cnt, dsu.find(u));
        tr.addEdge(cnt, dsu.find(v));
        dsu.merge(u, cnt);
        dsu.merge(v, cnt);
        wt[cnt] = w;  // 第 cnt 个点的点权
        // 意味着连接 u，v 两个点的最小代价
        sum += w;
        cnt++;
    }
    int rt = cnt - 1;
    tr.work(rt);
    for (auto [w, u, v, i] : e) {
        // 寻找先连接 i 这条边之后的 MST
        ans[i] = sum - wt[tr.lca(u, v)] + w;
    }

    for (int i = 1; i <= m; i++) {
        cout << ans[i] << endl;
    }
}
```

## 树上启发式合并

```C++
cin >> n;
int m = n - 1;
vector<vector<int>> e(n + 1);
vector<int> c(n + 1);

while (m--) {
	int u, v;
	cin >> u >> v;
	e[u].push_back(v); e[v].push_back(u);
}
for (int i = 1; i <= n; i++) {
	cin >> c[i];
}

vector<int> siz(n + 1), p(n + 1);
p[1] = -1;
Ycombinator([&](auto self, int u) -> void {
	if (p[u] != -1) {
		e[u].erase(find(range(e[u]), p[u]));
	}
	siz[u] = 1;
	for (auto &v : e[u]) {
		p[v] = u; 
		self(v);
		siz[u] += siz[v];
		if (siz[v] > siz[e[u][0]]) swap(v, e[u][0]);
	}
})(1);

int res = 0; 
vector<int> cnt(n + 1), ans(n + 1);

Ycombinator add = [&](auto self, int u) -> void {
	if (++cnt[c[u]] == 1) { res++; }
	for (auto &v : e[u]) { self(v); }
};

/*
    Ycombinator add = [&](auto self, int u, int h) -> void {
        cnt[c[u]]++;

        if (cnt[c[u]] == Max[h]) {
            ans[h] += c[u];
        } else if (cnt[c[u]] > Max[h]) {
            ans[h] = c[u];
            Max[h] = max(Max[h], cnt[c[u]]);
        }
        for (auto &v : e[u]) { self(v, h); }
    };
*/

Ycombinator sub = [&](auto self, int u) -> void {
	if (--cnt[c[u]] == 0) { res--; }
	for (auto &v : e[u]) { self(v); }
};

/*
    Ycombinator sub = [&](auto self, int u) -> void {
        cnt[c[u]] = Max[u] = 0;
        for (auto &v : e[u]) { self(v); }
    };
*/

Ycombinator([&](auto self, int u, int st) -> void {
	for (int i = 1; i < e[u].size(); i++) {
		auto &v = e[u][i];
		self(v, 0);
	}
	if (e[u].size()) self(e[u].front(), 1);
	if (++cnt[c[u]] == 1) {
		res++;
	}
	for (int i = 1; i < e[u].size(); i++) {
		auto &v = e[u][i];
		add(v);
	}
	ans[u] = res;
	if (st == 0) sub(u);

})(1, 0);

```

## 树的直径

### DP 写法
```C++
vector<int> d1(n + 1), d2 = d1;
int d = -INF;
auto dfs = [&](auto &&dfs, int u, int fa) -> void {
	for (auto v : e[u]) {
		if (v == fa) continue;
		dfs(dfs, v, u);
		int t = d1[v] + 1;
		if (t > d1[u]) d2[u] = d1[u], d1[u] = t;
		else if (t > d2[u]) d2[u] = t;
	}
	d = max(d, d1[u] + d2[u]);
};
dfs(dfs, 1, 0);
```

### 双dfs写法

```C++
struct tree_diameter {
  public:
	int x, y;
	int D;
	std::vector<int> dist, p, path;
	tree_diameter() { }
	tree_diameter(std::vector<std::vector<int>>& e) {
		dist.assign(e.size(), 0);
		p.assign(e.size(), 0);
		function<void(int, int)> dfs = [&](int u, int fa) -> void {
			p[u] = fa;
			for (auto v : e[u]) {
				if (v == fa) continue;
				dist[v] = dist[u] + 1;
				dfs(v, u);
			}
		};
		dfs(1, 0);
		x = std::max_element(range_(dist)) - dist.begin();
		fill(dist.begin(), dist.end(), 0);
		dfs(x, 0);
		y = std::max_element(range_(dist)) - dist.begin();
		D = dist[y];
  
		for (auto v = y; v != 0; v = p[v]) path.push_back(v);
		reverse(range(path));
	}
};
auto td = tree_diameter(e);
if (td.D == n - 1) {
	cout << -1 << endl;
	return;
}

```
* eg: 对整棵树进行剖分，按照链长，端点大小进行分治拆分
```C++
vector<int> del(n + 1, 0), pre(n + 1, 0);
auto dfsD = [&](auto &&dfsD, int u, int fa) -> PII {
	pre[u] = fa;
	PII res = PII(0, u);
	for (auto v : e[u]) {
		if (v != fa && !del[v]) {
			PII t = dfsD(dfsD, v, u);
			t.first ++;
			res = max(res, t);
		}
	}
	return res;
};
auto dfs = [&](auto &&dfs, int u) -> void {
	int D, U, V;
	U = dfsD(dfsD, u, 0).second;
	V = dfsD(dfsD, U, 0).second;

	U = max(U, V);   // 编号更大的端点
	auto t = dfsD(dfsD, U, 0);
	V = t.second, D = t.first;
	ans.push_back({D, U, V});
	while(V != 0) {
		del[V] = 1;
		for (auto v : e[V]) {
			if (!del[v] && v != pre[V]) dfs(dfs, v);
		}
		V = pre[V];
	}
};
dfs(dfs, 1);
```

* 结论一则：
	  求出树上距离任意一点最远的点的编号和距离，只需要对比直径的两个端点（必然是其中的一个点）。


## 点分治

### 子树大小与重心

```C++
auto dfs = [&](auto &&dfs, int u, int p = -1) -> void {  
//  以某点为根的子树大小
	siz[u] = 1;
	for (auto v : e[u]) {
		if (vis[v] || p == v) continue;
		dfs(dfs, v, u);
		siz[u] += siz[v];
	}
};
auto findg = [&](auto &&findg, int u,  int s, int p = -1) -> int {
//  找寻重心：小于等于子节点总数 1/2 的点就是 g
	for (auto v : e[u]) {
		if (vis[v] || v == p || siz[v] * 2 <= s) continue;
		return findg(findg, v, s, u);
	}
	return u;
};
auto work = [&](auto &&work, int u) -> int {
	dfs(dfs, u);
	int g = findg(findg, u, siz[u]);
	dfs(dfs, g);
	vis[g] = 1;    // 找到中心

	//debug(g)
	vector<int> a;
	for (auto v : e[g]) {
		if (vis[v]) continue;
		a.push_back(v);
	}
	// 找到所有与重心相邻的点
	
	if (a.empty()) {
		return g;
	}
	// 如果满足某种性质，就直接返回
	/* 	int tmp = query(a);
	change(g);
	if (abs(tmp - query(a)) == 2 * a.size()) {
		return g;
	} */

	while(a.size() > 1) {
		int sum = 0;
		for (auto x : a) {
			sum += siz[x];
		}

		// 依旧是二分
		// 把不同的子树分成两拨来进行判断（子树之间都通过重心g连接）
		int m = 0, res = 0;
		while(2 * (res + siz[a[m]]) <= sum) {
			res += siz[a[m++]];
		}
		
		if (2 * res + siz[a[m]] <= sum) m++;
		vector b(a.begin(), a.begin() + m);
		int tmp = query(b);
		change(g);
		
		if (abs(tmp - query(b)) == 2 * b.size()) {
			a = vector(a.begin() + m, a.end());
		} else {
			a = b;
		}
		// 分治 看符合要求的点在哪一半里面就赋值
	}
	return work(work, a.front());
};
```

## 树的性质积累

* 一个很重要的思想：**将任意两点之间的关系归结到各自与根节点之间的关系**。

* 边数 $= n − 1$.

- 度和 $=2(n−1)$.

* **树一定是二分图**

* 前缀异或（XOR）性质
	假设每条边有一个权值，定义 $xor(u)$ 为从根节点到 u 的所有边权的异或和，那么对于树中的任意两个节点 i 和 j，有 $xor(i,j)=xor(i)⊕xor(j)$
*
