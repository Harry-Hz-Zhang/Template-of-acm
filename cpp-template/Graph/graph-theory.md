---
topic: "图论"
category: "08-graph"
source: "图论 Graph.md"
---

# 图论

* **图论定理**：任何无向图中，“度数为奇的顶点数” 总是偶数。

- **Handshaking Lemma（握手引理）**（无向图）：

	图中所有节点的度数之和等于边数的两倍
    $\sum_{v\in V}\deg(v)=2|E|$.

    证明：每条无向边恰好为两个端点的度各贡献 1，自环贡献 2，所以总和等于 $2|E|$。

- **有向图度和**：

    $\sum_v \mathrm{outdeg}(v)=\sum_v \mathrm{indeg}(v)=|E|$
    （每条有向边为总出度和入度各贡献 1）。

- 推论（奇偶性）：无向图中奇度顶点的数目一定是偶数（从握手引理模 2 推出）。 *判定欧拉性的关键之一*

* **欧拉回路** 指 走遍图中每条边恰好一次且**回到起点**.

* **欧拉路** 指 走遍每条边恰好一次但**起点和终点可不同**.

## 拓扑排序

可用于判断是否含有自环，解决字典序相关问题
```C++
vector<int> f(n + 1, 0), ind(n + 1, 0);
vector<vector<int>> e(n + 1);
for (int i = 0; i < m; i++) {
	int a, b;
	cin >> a >> b;
	e[a].push_back(b);
	ind[b]++;
}
//  点从 1 ~ n 
auto topsort = [&]() -> void {
	queue<int> q;
	for (int i = 1; i <= n; i++) {
		if (ind[i] == 0) {
			q.push(i);// 如果一个点的入度等于0，就入队
		}
	}
	vector<int> res;// 存储拓扑排序的结果
	while (!q.empty())
	{
		int t = q.front();
		q.pop();
		res.push_back(t);
		for (auto v : e[t]) {
			if (--ind[v] == 0) {// 入度等于0
				q.push(v);
			}
		}
	}
	if (res.size() == n) {  // 如果所有点都在res数组中证明可以toposort
		for (auto it : res) cout << it << ' ';
	}
	else    // 含有自环
		puts("Impossible");
};
```

* 字典序最小（将 queue 换成 Heap）
* 分轮次删／分优先级处理的 trick

## 关于 找环 / 环的长度 / 经过的边 / 断环

```C++
edges.push_back(make_pair(u, v));
DSU dsu(n + 1);
bool hasCircle = 0;   // 并查集判存在环

for (auto &[u, v] : edges){
	if (u == v) { hasCircle = 1; break; }
	if (!dsu.merge(u, v)) { hasCircle = 1; break; }
}
```


```C++
function<void(int, int)> dfs = [&](int u, int i) -> void {
	set<int> S;  // 环中的边
	++ cir_id;   // 环的编号 
	while(!bel[u][i]) {
		bel[u][i] = cir_id;   // 当前状态属于哪个环
		S.insert(id[u][i]);
		auto [v, j] = nxt(u, i);  // 自动机转移
		u = v, i = j;
	}
	ans[cir_id] = S.size();
};
for (int u = 1; u <= n; u++) {
	for (int i = 0; i < e[u].size(); i++) {
		if (bel[u][i] != 0) continue;  // 该状态 没有所属的环
		dfs(u, i);   
	}
}
```

* 断环

```C++
cin >> n >> m;
vector<vector<PII>> e(n + 1);
for (int i = 1; i <= m; i++) {
	int u, v;
	cin >> u >> v;
	e[u].push_back({v, i});
}

vector<int> instk(n + 1, -1), res(m + 1);
bool cir = 0;
function<void(int u)> dfs = [&](int u) -> void {
	instk[u] = 1;
	for (const auto &[v, id] : e[u]) {
		if (instk[v] == -1) {
			dfs(v);
			res[id] = 1;
		} else if (instk[v] == 0) {
			res[id] = 1;
		} else if (instk[v] == 1) {
			res[id] = 2;
			cir = 1;
		}
	}
	instk[u] = 0;
};
for (int i = 1; i <= n; i++) {
	if (instk[i] == -1) {
		dfs(i);
	}
}
cout << (cir ? 2 : 1) << endl;
```

## 欧拉

	在离散数学中，当看到“把一堆东西分成相等的两份（且总数是偶数）”时，第一反应应该将其等价转化为：“给图中的边定向，使得每个节点的入度等于出度”。

**欧拉路径（Eulerian path）是经过图中每条边恰好一次的路径，欧拉回路（Eulerian circuit）是经过图中每条边恰好一次的回路。

**对于无向图,其可以构造出欧拉回路的充要条件是所有点的度数都是偶数**.

要有欧拉路，奇度顶点数必须是 0 或 2
### 无向图

- **存在 Euler 回路（闭合） 的充要条件**：图的每个顶点的度都是偶数，且所有具有正度的顶点属于同一个连通分量（即非孤立边在同一连通块中）。

- **存在 Euler 路（开） 的充要条件**：恰好 **0 或 2 个顶点为奇度**，且所有非孤立顶点在同一连通分量中；若有 2 个奇度顶点，任一欧拉路从一个奇度顶点开始，到另一个奇度顶点结束。

### 有向图

- **有向欧拉回路**：每个顶点的入度等于出度，并且所有有边的顶点在同一个强连通分量（或更细的表述：若把边视为弧，删去零度顶点后，图为强连通）。

- **有向欧拉路**：至多一个顶点满足 $\mathrm{outdeg}=\mathrm{indeg}+1$，至多一个顶点满足 $\mathrm{indeg}=\mathrm{outdeg}+1$，其他顶点入度等于出度；并且把方向忽略后的图在非零度顶点上连通。

    （有向版的等价条件与无向类似，但需区分 in/out）

### 模板

```C++
function<void(int)> euler = [&](int u) -> void {
	while (e[u].size()) {
		auto[v, id] = e[u].back();
		e[u].pop_back();
		if (del[id]) continue;
		del[id] = 1;
		euler(v);
	}
	cout << u << ' ';
};
```


```cpp
	e[u].push_back({v, idx});
	e[v].push_back({u, idx});
	dir[idx++] = {u, v}; // 每条边的连接顶点
	vector<int> del(2 * sum + 10);
	function<void(int)> euler = [&](int u) -> void {
		while (e[u].size()) {
			auto[v, id] = e[u].back();
			e[u].pop_back();
			if (del[id]) continue;
			del[id] = 1;
	
			if (u >= alls.size()) {
				// u -> v
			} else {
				// v -> u
			}
			euler(v);
		}
	};
	for (int i = 1; i <= n; i++) {
		euler(i);
	}
```

对于无向图来讲，由于每条边只能跑一次，所以最后会确定下一个有向图，本质上就是给无向图的每一条边“定向”的过程。

### de_bruijn_sequence

```cpp
vector<int> de_bruijn_sequence(int n, int k) {  // n 位 k 进制
    int m = 1;
    for (int i = 1; i < n; i++) {
        m *= k;
    } // m = n^k-1
    vector<int> cur(m, 0), res;
    Y_combinator eular = [&](auto &&self, int u, int edge) -> void {
        while (cur[u] < k) {
            int edge_ = cur[u]++;
            self((u * k + edge_) % m, edge_);
        }
        if (edge != -1) res.push_back(edge);
    };
    eular(0, -1);
    res.insert(res.end(), n - 1, 0);
    reverse(range(res));
    return res;
}
```


## 哈密顿图

$Dirac$ 定理 (充分条件)：
	设一个无向图中有 $N$ 个顶点，若所有顶点的度数大于等于 $N/2$ ，则哈密顿回路一定存在( $N/2$ 指的是 $⌈N/2⌉$，向上取整)

## 最短路

### BFS 最短路

* 时间复杂度最低，首选，只有当边权不一致时候再往下考虑

```C++
vector<int> dist(n + 1), vis(n + 1);
auto bfs = [&](int start) -> void {
    fill(dist.begin() + 1, dist.end(), INF);
    fill(vis.begin() + 1, vis.end(), 0);
    queue<int> q;
    dist[start] = 0;
    vis[start] = 1;
    q.push(start);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        
        // 注意：不要在这里写 vis[u] = 1; ！！
        for (int v : e[u]) {
            if (!vis[v]) {
                dist[v] = dist[u] + 1;
                vis[v] = 1;
                q.push(v);
            }
        }
    }
};
```

### 0_1_BFS

* 边权只有 0 和 1

```C++
vector<vector<pair<int, int>>> e(n + 1);
vector<int> dist(n + 1), vis(n + 1);
auto zero_one_bfs = [&](int start) -> void {
    fill(dist.begin() + 1, dist.end(), INF);
    fill(vis.begin() + 1, vis.end(), 0);
    deque<int> dq; 
    
    dist[start] = 0;
    dq.push_back(start);
    while (!dq.empty()) {
        int u = dq.front();
        dq.pop_front();
        // 0-1 BFS 的 vis 处理逻辑和 Dijkstra 一样
        // 在出队 (pop) 时判重并打标记，而不是入队时。
        if (vis[u]) continue; 
        vis[u] = 1;
        
        for (auto [v, w] : e[u]) {
            // w 只能是 0 或者 1
            if (dist[v] > dist[u] + w) {
                dist[v] = dist[u] + w;
                if (w == 0) {
                    // 如果花费为 0 直接插到队头优先处理
                    dq.push_front(v);
                } else {
                    // 如果花费为 1 放到队尾排队
                    dq.push_back(v);
                }
            }
        }
    }
};
```

### Heap 优化 Dijkstra

* 边权不一致无奈才选 dijkstra

```C++
// O(Elog E) or O(Elog V)
vector<vector<pii>> e(n + 1);
vector<int> dist(n + 1), st(n + 1);


auto dijkstra = [&]() -> void {
	fill(dist.begin() + 1, dist.end(), INF);
	fill(st.begin() + 1, st.end(), 0LL);
	priority_queue<pii, vector<pii>, greater<pii>> heap;
	dist[1] = 0;
	heap.push({0, 1});
	while(!heap.empty()) {
		auto [_, u] = heap.top();
		heap.pop();
		if (st[u]) continue;
		
		st[u] = 1;
		for (auto [v, w] : e[u]) {
			if (dist[v] > dist[u] + w) {
				dist[v] = dist[u] + w;
				heap.push({dist[v], v});
			}
		}
	}
};
```

### SPFA 判负环
```C++
auto spfa = [&]() -> bool {
	queue<int> q;
	vector<int> dist(n + 1, INF), st(n + 1), cnt(n + 1, 0);
	st[1] = 1, dist[1] = 0;
	q.push(1);
	cnt[1] ++;
	while(q.size()) {
		auto t = q.front();
		q.pop();
		st[t] = 0;
		for (auto [v, w] : e[t]) {
			if (dist[v] > dist[t] + w) {
				dist[v] = dist[t] + w;
				if (!st[v]) {
					if (cnt[v]++ >= n) return 1;  // 存在负环
					q.push(v);
					st[v] = 1;
				}
			}
		}
	}
	return 0;
};
```

## 最小生成树
### Prim 算法 O(mlog(n)) + O(n^2)

```C++
// O(mlog(n))
struct prim {
    using PII = pair<int, int>;
    int n;
    vector<vector<PII>> e; 
    vector<int> dis;    // 存储节点到当前生成树的最短距离
    vector<bool> vis;   // 标记节点是否已经加入生成树
    int tot;   // 最小生成树总权值
    bool f;    // 是否连通
    prim() { }
    prim(int n) { init(n); }
    void init(int n) {
        this->n = n;
        e.assign(n + 1, { });
        dis.assign(n + 1, numeric_limits<int>::max());
        vis.assign(n + 1, false);
        tot = 0;
        f = false;
    }
    void add_edge(int u, int v, int w) {
        e[u].push_back({v, w});
        e[v].push_back({u, w});
    }
    // 返回MST的总权值，如果图不连通返回 -1
    int work(int star = 1) {
        priority_queue<PII, vector<PII>, greater<PII>> pq;
        dis[star] = 0LL;
        pq.push({0LL, star});
        int cnt = 0LL; // 记录已加入生成树的节点数

        while (!pq.empty()) {
            auto [d, u] = pq.top();
            pq.pop();
            if (vis[u]) continue;
            vis[u] = true;
            tot += d;
            cnt++;
            for (auto& [v, w] : e[u]) {
                // v 还没进树
                if (!vis[v] && w < dis[v]) {
                    dis[v] = w;   // 更新最短距离
                    pq.push({dis[v], v});  // 将更新后的距离推入堆
                }
            }
        }
        if (cnt == n) {
            f = true; return tot;
        } else {
            f = false; return -1;
        }
    }
};
```

```C++
// 朴素 Prim (O(n^2))
struct Prim_dense {
    int n;
    vector<vector<int>> g;
    vector<int> dis;
    vector<bool> vis;
    int tot;
    bool f;

    Prim_dense() {}
    Prim_dense(int n) { init(n); }
    void init(int n) {
        this->n = n;
        // 邻接矩阵初始化为 INF，自环初始化为 0
        g.assign(n + 1, vector<int>(n + 1, INF));
        for (int i = 1; i <= n; i++) g[i][i] = 0;
        dis.assign(n + 1, INF);
        vis.assign(n + 1, false);
        tot = 0;
        f = false;
    }

    // 重边留最小权值
    void add_edge(int u, int v, int w) {
        if (u < 1 || u > n || v < 1 || v > n) return;
        if (w < g[u][v]) {
            g[u][v] = g[v][u] = w;
        }
    }

    int work(int star = 1) {
        dis[star] = 0;
        int cnt = 0;
        for (int i = 1; i <= n; i++) {
            int u = -1;
            for (int j = 1; j <= n; j++) {
                if (!vis[j] && (u == -1 || dis[j] < dis[u])) {
                    u = j;
                }
            }
            if (u == -1 || dis[u] == INF) break;
            vis[u] = true;
            tot += dis[u];
            cnt++;
            for (int v = 1; v <= n; v++) {
                if (!vis[v] && g[u][v] < dis[v]) {
                    dis[v] = g[u][v];
                }
            }
        }
        if (cnt == n) {
            f = true; return tot;
        } else {
            f = false; return -1;
        }
    }
};
```
### Boruvka 算法 O(T logn)

```text
    bool is_connected = 0;
    while (!is_connected) {
        for (auto i : DSU) {
            minw[i]; // i 连出去的最短边 -> T 处理好这里的复杂度
            // 从 i 连出去的最短的边
        }
        for (auto i : DSU) {
            merge(i, minw[i]);
        }
    }
```

* 在一个由 n 个点组成的近似完全图中（每个点删除了几条边的完全图中），找出一个最小生成树，其中边权为两点点权之和 w_u_v = a[u] + a[v];

```C++
void solve()
{
    int n, m;
    cin >> n >> m;
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    vector<vector<int>> e(n + 1);
    while (m--) {
        int u, v;
        cin >> u >> v;
        e[u].push_back(v), e[v].push_back(u);
    }

    set<pair<int, int>> S;
    DSU dsu(n + 1);
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        S.insert(pii(a[i], i));
    }

    auto boruvka = [&]() -> bool {
        bool RES = 0;
        vector<vector<int>> vec(n + 1);

        for (int i = 1; i <= n; i++) {
            vec[dsu.find(i)].push_back(i);
        }

        for (int i = 1; i <= n; i++) {
            for (auto v : vec[i]) {
                S.erase({a[v], v});
            }
            int Min = INF, p = -1;
            for (auto u : vec[i]) {
                for (auto v : e[u]) {
                    if (dsu.same(u, v)) continue;
                    S.erase({a[v], v});
                }
                if (S.size()) {
                    auto it = *S.begin();
                    if (a[u] + it.first < Min) {
                        Min = a[u] + it.first, p = it.second;
                    }
                }
                for (auto v : e[u]) {
                    if (dsu.same(u, v)) continue;
                    S.insert({a[v], v});
                }
            }
            if (p != -1 && !dsu.same(i, p)) {
                RES = 1;
                ans += Min;
                dsu.merge(i, p);
            }
            for (auto v : vec[i]) {
                S.insert({a[v], v});
            }
        }
        return RES;
    };

    while (boruvka());

    for (int i = 1; i <= n; i++) {
        if (!dsu.same(1, i)) {
            cout << -1 << endl;
            return;
        }
    }
    cout << ans << endl;
}
```

## SCC

* **一个 SCC（强连通分量）并不一定是“一个简单环”**，而是“任意复杂的强连通子图”，可能包含很多交织的环、回路、跨条路径

```C++
struct SCC {
    int n;
    vector<vector<int>> e;
    vector<int> stk;
    vector<int> dfn, low, bel;
    int cur, cnt;

    SCC() { }
    SCC(int n) {
        init(n);
    }
    void init(int n) {
        this->n = n;
        e.assign(n + 1, { });
        dfn.assign(n + 1, -1);
        low.resize(n + 1);
        bel.assign(n + 1, -1);
        stk.assign(n + 1, -1);
        stk.clear();
        cur = cnt = 1;
    }
    void add_edge(int u, int v) {
        e[u].push_back(v);
    }
    void dfs(int u) {
        dfn[u] = low[u] = cur++;
        stk.push_back(u);
        for (auto v : e[u]) {
            if (dfn[v] == -1) {
                dfs(v);
                low[u] = min(low[u], low[v]);
            } else if (bel[v] == -1) {
                low[u] = min(low[u], dfn[v]);
            }
        }
        if (dfn[u] == low[u]) {
            int v;
            do {
                v = stk.back();
                bel[v] = cnt;
                stk.pop_back();
            } while(v != u);
            cnt++;
        }
    }
    vector<int> work() {
        for (int i = 1; i <= n; i++) {
            if (dfn[i] == -1) {
                dfs(i);
            }
        }
        return bel;
    }
    int num() {
        return cnt - 1;
    }
};
```
* 多与所谓的 **汇点** 有联系：这个块内的所有点相互可达，且有向边 ind = 0.

## 判割点

```C++
struct cut_vertex { // 无向图
    int n;
    vector<vector<int>> e;
    vector<int> dfn, low;
    vector<bool> is_cut;
    int cur;

    cut_vertex(int n) : n(n) {
        e.assign(n + 1, {});
        dfn.assign(n + 1, -1);
        low.assign(n + 1, 0);
        is_cut.assign(n + 1, false);
        cur = 0;
    }

    void add_edge(int u, int v) {
        e[u].push_back(v); e[v].push_back(u);
    }
    void dfs(int u, int fa = -1) {
        dfn[u] = low[u] = ++cur;
        int ch_cnt = 0;

        for (auto v : e[u]) {
            if (v == fa) continue;
            if (dfn[v] == -1) {
                ch_cnt++;
                dfs(v, u);
                low[u] = min(low[u], low[v]);
                if (fa != -1 && low[v] >= dfn[u]) {
                    is_cut[u] = true;
                }
            } else {
                low[u] = min(low[u], dfn[v]);
            }
        }
        if (fa == -1 && ch_cnt > 1) {
            is_cut[u] = true;
        }
    }
    bool is_Cut(int x)  {
        return is_cut[x];
    }
    void work() {
        for (int i = 1; i <= n; i++) {
            if (dfn[i] == -1) dfs(i);
        }
    }
};
```

##  二分图

* 树一定是二分图
* 二分图一定没奇环
* **二分图的充分必要条件是 <==> G至少有两个顶点,且图所有回路的长度均为偶数**
* **二分图的必要条件之一：边数 ≤ n-1 时才是树，否则有环。**

* 最小顶点覆盖：选出最少的点，构成一个集合，使得每条边都有一个顶点在这个集合里面。

* 最小顶点覆盖数等于：二分图的最大匹配数。

* 最少边覆盖：选最少的边，覆盖所有点。

* 最大独立集：
	选最多的点，两两之间没有边：

**题目中有两个维度的约束，且一个元素同时受到这两个维度的限制**

### 染色：

* 最终颜色为 1 / 2
```C++
pair<bool, vector<int>> is_bipartite(int n, const vector<vector<int>> &e) {
    vector<int> col(n + 1, 0);
    bool f = 1;
    function<void(int)> dfs = [&](int u) -> void {
        for (int v : e[u]) {
            if (!col[v]) {
                col[v] = col[u] ^ 3;
                dfs(v);
            } else if (col[v] == col[u]) {
                f = 0;
            }
        }
    };
    
    for (int i = 1; i <= n; ++i) {
        if (!col[i]) {
            col[i] = 1;
            dfs(i);
            if (!f) return {0, vector<int>({})};
        }
    }
    return {1, col};
}
vector<vector<int>> S(3);
for (int i = 1; i <= n; i++) {
	S[col[i]].push_back(i);
}
```


```C++
vector<int> col(2 * n + 1);
auto dye = [&](auto &&self, int u, int c, int fa) -> bool {
	if (col[u] && col[u] != c) return 0;
	col[u] = c;
	for (auto v : e[u]) {
		if (v == fa) continue;
		if (col[v]) {
			if (col[v] != (c == 1 ? 2 : 1)) return 0;
			continue;
		}
		if (!self(self, v, (c == 1 ? 2 : 1), u)) return 0;
	}
	return 1;
};
```

### 匈牙利算法

```C++

```

## 求闭包 （带环的有向图需要先SCC缩点）

```C++
// 假设在你的主函数 solve() 中，已经读入了 n 和闭包矩阵 g
// n 是节点数
// g 是 vector<string>，下标从 1 开始，g[i][j] == '1' 表示 i 能到达 j

auto build_direct_edges = [&]() -> vector<vector<int>> {
    vector<vector<int>> ed(n + 1); // 最终的直接连边邻接表
    vector<int> cnt(n + 1, 0);     // 统计每个点的出度（能到达的节点数）

    // 1. 统计出度
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) {
            if (g[i][j] == '1') {
                cnt[i]++;
            }
        }
    }

    // 2. 生成节点编号并按出度降序排序
    vector<int> id(n);
    iota(id.begin(), id.end(), 1); // 填充 1, 2, ..., n
    ranges::sort(id, [&](int a, int b) {
        return cnt[a] > cnt[b]; // 出度大的排前面 (大老板优先)
    });

    vector<int> vis(n + 1, 0);
    for (int u = 1; u <= n; ++u) {
        vis[u] = u; // 绝妙的时间戳：把 vis 的值设为当前的 u，代表"被 u 覆盖"

        for (int v : id) {
            // 如果 v 没有被当前的 u 覆盖过，且 u 能到达 v
            if (vis[v] != u && g[u][v] == '1') {
                ed[u].push_back(v);
                for (int w = 1; w <= n; ++w) {
                    if (g[v][w] == '1') {
                        vis[w] = u; 
                    }
                }
            }
        }
    }
    
    return ed; 
};
// vector<vector<int>> tree_edges = build_direct_edges();
```


## color_coding

```C++
struct Rand {
public:
    mt19937_64 eng;
    Rand() : eng(random_device{}()) {}
    explicit Rand(uint64_t seed) : eng(seed) {}
    template <typename T>
    T gen(T l, T r) {
        if constexpr (is_integral_v<T>) return uniform_int_distribution<T>(l, r)(eng);
        else return uniform_real_distribution<T>(l, r)(eng);
    }
    template <typename T>
    T operator()(T l, T r) { return gen(l, r); }
#if __cplusplus > 202002L
    template <typename T>
    T operator[](T l, T r) { return gen(l, r); }
#endif
    double operator()() { return uniform_real_distribution<double>()(eng); }
    // 随机 bool，p 为 true 的概率
    bool bernoulli(double p = 0.5) {
        return bernoulli_distribution(p)(eng);
    }
    // 打乱容器
    template <typename Container>
    void shuffle(Container& c) {
        std::shuffle(range_(c), eng);
    }
} R;

int color_coding_max_path(int n, int k, const vector<vector<pii>>& e, int iter_count = 300) {
    int ans = -INF;
    int mask = 1 << k;

    vector<int> color(n + 1);
    vector<vector<int>> f(mask, vector<int>(n + 1, -INF));
    for (int it = 0; it < iter_count; it++) {
        for (int i = 1; i <= n; i++) { color[i] = R(0LL, k - 1);  }
        for (int s = 0; s < mask; s++) { fill(range(f[s]), -INF); }
        for (int i = 1; i <= n; i++) { f[1 << color[i]][i] = 0; }
        for (int s = 1; s < mask; s++) {
            for (int u = 1; u <= n; u++) {
                if (f[s][u] == -INF) continue; 
                for (auto [v, w] : e[u]) {
                    int c_v = color[v];
                    // 只有当邻居 v 的颜色 c_v 还没有包含在当前路径状态 s 中时，才能走过去
                    if ((s & (1 << c_v)) == 0) {
                        int next_s = s | (1 << c_v);
                        if (f[s][u] + w > f[next_s][v]) {
                            f[next_s][v] = f[s][u] + w;
                        }
                    }
                }
            }
        }
        for (int i = 1; i <= n; i++) {
            if (f[mask - 1][i] > ans) {
                ans = f[mask - 1][i];
            }
        }
    }
    return ans;
}
```
