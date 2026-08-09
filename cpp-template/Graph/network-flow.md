---
topic: "网络流"
category: "08-graph"
source: "图论 Graph.md"
---

# 网络流

## **可行流 f**（不考虑反向边）

* **可行流** 表示的其实是一种方案，表示每条边的一种取值，一个流网络中有无数种可行流

* 给网络流中每条边都设定一个值，满足以下两个条件的方案就是 **可行流**：

	1.  **容量限制 $$0 \le f(u, v) \le c(u, v)$$
	2.  **流量守恒（除了S, T）$$ \forall x \in V - \{S,T\}, \sum_{(c,x)\in E} f(v, x)  = \sum_{(x,c)\in E} f(x, v)$$
* $\mid$ f $\mid$ 表示可行流 f 的值（从源点流出去的 **净流量**）

* **最大流**：**最大可行流**，即所有的可行方案中 | f | 最大的值

## **残留网络**（针对某一条可行流 f 来说）$G_f$ $=$ $(V_f,E_f)$

* $V_f$ $=$ $V$

* $E_f$ $$E_f = E + E中所有反向边$$
* 残存容量：对于流网络 $G$ $=$ $(V, E)$, 设 $f$ 为图 $G$ 的一个流，考虑节点对 $u, v$ $\in$ $V$,有：

$$
c_f(u, v) =
\begin{cases}
c(u, v) - f(u, v),  & \text{if $(u, v)$ $\in$ E} \\[2ex]
f(v, u), & \text{if $(v, u)$ $\in$ E} \\[2ex]
0, & \text{else}
\end{cases}$$

* 定理：**对于可行流 f 来说，其残留网络中的可行流为 f '，则 f + f ‘ 也是原网络G的一个可行流。**

## 最大流最小切割定理（以下三个条件是等价的）

1. $f$ 是 $G$ 的一个最大流
2. 残留网络 $G_f$ 不包含任何增广路径
3. $|f|$ $= c (S, T)$ , 其中$(S, T)$ 是流网络 $G$ 的某个割

则存在以下描述：
*  *给定我们一个流网络 $G$，以及 $G$ 中的一个可行流 $f$（从源点 $S$ 到汇点 $T$ 的可行流），构造出一个关于 $f$ 的残留网络 $G_f$，若 $G_f$ 中不含增广路，则 $f$ 为**原网络**的最大可行流。

## 最大流 (MaxFlow)

```C++
// O(E·V²)
template<class T>
struct MaxFlow {
  public:
    struct _Edge {
        int v;
        T cap;
        _Edge(int v = 0, T cap = 0): v(v), cap(cap) { }
    };

    int n;
    vector<_Edge> edge;
    vector<vector<int>> e;
    vector<int> cur, level;

    MaxFlow() {}
    MaxFlow(int n_) { init(n_); }
    void init(int n_) {
        n = n_;
        edge.clear();
        e.assign(n + 1, { });
        cur.resize(n + 1);
        level.resize(n + 1);
    }

    bool bfs(int s, int t) {
        level.assign(n + 1, -1);
        queue<int> q;
        q.push(s);
        level[s] = 0;
        while (q.size()) {
            const int u = q.front();
            q.pop();
            for (auto idx : e[u]) {
                auto [v, c] = edge[idx];
                if (c > 0 && level[v] == -1) {
                    level[v] = level[u] + 1;
                    if (v == t) return 1;
                    q.push(v);
                }
            }
        }
        return 0;
    }
    T dfs(int u, int t, T f) {
        if (u == t) return f;
        auto r = f;
        for (int &i = cur[u]; i < e[u].size(); i++) {
            const int j = e[u][i];
            auto [v, c] = edge[j];
            if (c > 0 && level[v] == level[u] + 1) {
                auto a = dfs(v, t, min(r, c));
                if (a > 0) {
                    edge[j].cap -= a;
                    edge[j ^ 1].cap += a;
                    r -= a;
                    if (!r) return f;
                }
            }
        }
        return f - r;
    }

    void addEdge(int u, int v, T c) {
        e[u].push_back(edge.size());
        edge.emplace_back(v, c);
        e[v].push_back(edge.size());
        edge.emplace_back(u, 0);
    }
    T flow(int s, int t) {
        T ans = 0;
        int idx = 0;
        while (bfs(s, t)) {
            cur.assign(n + 1, 0);
            ans += dfs(s, t, numeric_limits<T>::max());
        }
        return ans;
    }
    vector<bool> minCut() {
        vector<bool> c(n + 1);
        for (int i = 1; i <= n; i++) {
            c[i] = (level[i] != -1); 
        }
        return c;
    }
    struct Edge {
        int u, v;
        T cap, flow;
    };

    vector<Edge> edges() {
        vector<Edge> a;
        for (int i = 0; i + 1 < edge.size(); i += 2) {
            Edge x;
            x.u = edge[i + 1].v;
            x.v = edge[i].v;
            x.cap = edge[i].cap + edge[i + 1].cap;
            x.flow = edge[i + 1].cap;
            a.push_back(x);
        }
        return a;
    }
};

int orig_n = n;            // 你的原始节点数
int S = orig_n + 1;        // 虚拟源
int T = orig_n + 2;        // 虚拟汇
mf.init(orig_n + 2);       // 注意 init 使用新的总节点数（1-based）

// 把原图的边按原样加：假设你已经做过这些 addEdge( u, v, cap );

// 把每个原始“源”节点连到 S（S -> ai），容量通常设为 INF 或该源的限制
for (int ai : A) {
    mf.addEdge(S, ai, INF); // INF 代表“够大”，见下面的关于INF的说明
}
// 把每个原始“汇”节点连到 T（bi -> T）
for (int bi : B) {
    mf.addEdge(bi, T, INF);
}
// 计算最大流：注意使用虚拟源和虚拟汇
long long maxflow = mf.flow(S, T);
```


### 例题：

- 城市有 $n$ 个，第 $i$ 个出发时有 $a_i$​ 名士兵；希望最终第 $i$ 个有 $b_i$ 名士兵。
- 每个士兵可以要么原地不动，要么沿着一条相连的路走到某个**相邻**城市（最多走一条路）
- 问：能不能安排每个士兵去哪里，使得最后每个城市人数正好是 $b_i$​？如果能，给出每对城市之间从 $i$ 到 $j$ 走的人数（包含 $i=j$ 的“留在本城”）。

- **源点 S**（单个）。
- **左侧一组节点 L₁..Lₙ**：每个左侧节点 $L_i$ 表示“城市 $i$ 出发的士兵”，从 $L_i$ 发出去的总流不能超过 $a_i$（因为最多只有 $a_i$ 名士兵）。
- **右侧一组节点 R₁..Rₙ**：每个右侧节点 $R_j$ 表示“城市 $j$ 最终接收的位置”，流入 $R_j$ 的总量不能超过 $b_j$（最终最多只允许 $b_j$ 名士兵停在城市 $j$）。
- **汇点 T**（单个）。


```C++
void solve() {
    int n, m;
    cin >> n >> m;
    vector<int> a(n + 1), b = a;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= n; i++) cin >> b[i];

    if (accumulate(range(a), 0LL) != accumulate(range(b), 0LL)) {
        cout << "NO" << endl;
        return;
    }

    int orig_n = n;
    int S = 0;
    int T = orig_n * 2 + 1;
    MaxFlow<int> mf(T + 2);

    for (int i = 1; i <= n; i++) {
        mf.addEdge(i, i + n, INF);
    }
    for (int i = 1; i <= m; i++) {
        int u, v;
        cin >> u >> v;
        mf.addEdge(u, orig_n + v, INF);
        mf.addEdge(v, orig_n + u, INF);
    }

    for (int i = 1; i <= n; i++) {
        mf.addEdge(S, i, a[i]);
    }
    for (int i = 1; i <= n; i++) {
        mf.addEdge(i + n, T, b[i]);
    }
    int maxflow = mf.flow(S, T);
    
    if (maxflow != accumulate(range(a), 0LL)) {
        cout << "NO" << endl;
        return;
    }

    cout << "YES\n";
    auto edges = mf.edges();
    vector<vector<int>> ans(n + 1, vector<int>(n + 1));
    for (auto [u, v, c, f] : edges) {
        if (u >= 1 && u <= n && v > n && v <= 2 * n) {
            ans[u][v - n] = f;
        }
    }

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            cout << ans[i][j] << ' ';
        }
        cout << endl;
    }
}
```

## 最小费用可行流 (MCFGraph)

```C++

struct MCFGraph {
    struct Edge {
        int v, c;
        i64 w;
        Edge(int v_ = 0, int c_ = 0, i64 w_ = 0) : v(v_), c(c_), w(w_) { }
    };
    int n;

    vector<Edge> edge;
    vector<vector<int>> e;
    vector<i64> h, dist;
    vector<int> pre;
    vector<int> cur;
    vector<char> vis;

    MCFGraph(int n_ = 0) { init(n_); }
    void init(int n_) {
        n = n_;
        edge.clear();
        h.assign(n + 1, 0);
        e.assign(n + 1, { });
        dist.assign(n + 1, INF);
        pre.assign(n + 1, -1);
        cur.assign(n + 1, 0);
        vis.assign(n + 1, 0);
    }

    bool dijkstra(int s, int t) {
        dist.assign(n + 1, INF);
        pre.assign(n + 1, -1);
        priority_queue<PII, vector<PII>, greater<PII>> heap;
        dist[s] = 0;
        heap.emplace(0, s);

        while (!heap.empty()) {
            auto [d, u] = heap.top();
            heap.pop();

            if (dist[u] < d) continue;

            for (int i : e[u]) {
                auto &[v, c, w] = edge[i];
                if (c > 0) {
                    i64 nd = d + h[u] - h[v] + w;
                    if (dist[v] > nd) {
                        dist[v] = nd;
                        pre[v] = i;
                        heap.emplace(dist[v], v);
                    }
                }
            }
        }
        return dist[t] != INF;
    }

    void addEdge(int u, int v, int c, int w) {
        if (w < 0) { //这是为了解决“初始有负边，Dijkstra 不安全”的一个工程性技巧
            e[u].push_back(edge.size());
            edge.emplace_back(v, 0, w);
            e[v].push_back(edge.size());
            edge.emplace_back(u, c, -w);
        } else { 
            e[u].push_back(edge.size());
            edge.emplace_back(v, c, w);
            e[v].push_back(edge.size());
            edge.emplace_back(u, 0, -w);
        }
    }

    int find_flow(int u, int t, int limit) {
        if (!limit || u == t) return limit;
        vis[u] = 1;
        int flowed = 0;
        for (int &idx = cur[u]; idx < e[u].size() && flowed < limit; idx++) {
            int i = e[u][idx];
            auto &[v, c, w] = edge[i];
            if (c > 0 && !vis[v]) {
                if (w + h[u] - h[v] == 0) {
                    int got = find_flow(v, t, min(limit - flowed, c));
                    if (got > 0) {
                        edge[i].c -= got;
                        edge[i ^ 1].c += got;
                        flowed += got;
                    }
                }
            }
        }
        vis[u] = 0;
        return flowed;
    }

    PII flow(int s, int t) {
        int flow = 0;
        i64 cost = 0;
        h.assign(n + 1, 0);

        // h.assign(n + 1, INF);
        // h[s] = 0;
        // for (int it = 0; it < n - 1; it++) {
        //     bool changed = false;
        //     for (int u = 0; u <= n; u++) { /* 包含 0 */
        //         if (h[u] == INF) continue;
        //         for (int id : e[u]) {
        //             auto &ed = edge[id];
        //             if (ed.c > 0 && h[ed.v] > h[u] + ed.w) {
        //                 h[ed.v] = h[u] + ed.w;
        //                 changed = true;
        //             }
        //         }
        //     }
        //     if (!changed) break;
        // }
        // for (int i = 0; i <= n; i++) if (h[i] == INF) h[i] = 0;

        for (int i = 0; i <= n; i++) if (h[i] == INF) h[i] = 0;
        i64 last_dist_t = INF;
        while (dijkstra(s, t)) {
            for (int i = 0; i <= n; i++) {
                if (dist[i] < INF) h[i] += dist[i];
            }

            for (int i = 0; i <= n; ++i) cur[i] = 0;
            int Spush = 0;
            while (1) {
                int push = find_flow(s, t, INF);
                if (!push) break;
                Spush += push;
                flow += push;
                cost += push * h[t];
            }

            if (Spush == 0 && dist[t] == last_dist_t) break;
            last_dist_t = dist[t];
        }
        return make_pair(flow, cost);
    }
};


```

## 最小费用最大流 (MCFGraph)

* 建边时候注意一下就行
```C++
void addEdge(int u, int v, int c, int w) { // 最大流
	e[u].push_back(edge.size());
	edge.emplace_back(v, c, w);
	e[v].push_back(edge.size());
	edge.emplace_back(u, 0, -w);
}
```

## 最大费用最大流 (MCFGraph)

```C++
struct MCFGraph {
    struct Edge {
        int v, c;
        i64 w;
        Edge(int v_ = 0, int c_ = 0, i64 w_ = 0) : v(v_), c(c_), w(w_) { }
    };
    int n;

    vector<Edge> edge;
    vector<vector<int>> e;
    vector<i64> h, dist;
    vector<int> pre;
    vector<int> cur;
    vector<char> vis;

    MCFGraph(int n_ = 0) { init(n_); }
    void init(int n_) {
        n = n_;
        edge.clear();
        h.assign(n + 1, 0);
        e.assign(n + 1, { });
        dist.assign(n + 1, INF);
        pre.assign(n + 1, -1);
        cur.assign(n + 1, 0);
        vis.assign(n + 1, 0);
    }

    bool dijkstra(int s, int t) {
        dist.assign(n + 1, INF);
        pre.assign(n + 1, -1);
        priority_queue<PII, vector<PII>, greater<PII>> heap;
        dist[s] = 0;
        heap.emplace(0, s);

        while (!heap.empty()) {
            auto [d, u] = heap.top();
            heap.pop();

            if (dist[u] < d) continue;

            for (int i : e[u]) {
                auto &[v, c, w] = edge[i];
                if (c > 0) {
                    i64 nd = d + h[u] - h[v] + w;
                    if (dist[v] > nd) {
                        dist[v] = nd;
                        pre[v] = i;
                        heap.emplace(dist[v], v);
                    }
                }
            }
        }
        return dist[t] != INF;
    }

    //把正向边权取负（存为 -w），这是将“最大费用”转成“最小费用”的最小工程化改动
    void addEdge(int u, int v, int c, int w) {
        e[u].push_back(edge.size());
        edge.emplace_back(v, c, -w);  // <<< 存 -w
        e[v].push_back(edge.size());
        edge.emplace_back(u, 0, w);   // <<< 反向边存 +w
    }

    int find_flow(int u, int t, int limit) {
        if (!limit || u == t) return limit;
        vis[u] = 1;
        int flowed = 0;
        for (int &idx = cur[u]; idx < e[u].size() && flowed < limit; idx++) {
            int i = e[u][idx];
            auto &[v, c, w] = edge[i];
            if (c > 0 && !vis[v]) {
                if (w + h[u] - h[v] == 0) {
                    int got = find_flow(v, t, min(limit - flowed, c));
                    if (got > 0) {
                        edge[i].c -= got;
                        edge[i ^ 1].c += got;
                        flowed += got;
                    }
                }
            }
        }
        vis[u] = 0;
        return flowed;
    }

    PII flow(int s, int t) {
        int flow = 0;
        i64 cost = 0;
        h.assign(n + 1, 0);
        
        // h.assign(n + 1, INF);
        // h[s] = 0;
        // for (int it = 0; it < n - 1; it++) {
        //     bool changed = false;
        //     for (int u = 0; u <= n; u++) { /* 包含 0 */
        //         if (h[u] == INF) continue;
        //         for (int id : e[u]) {
        //             auto &ed = edge[id];
        //             if (ed.c > 0 && h[ed.v] > h[u] + ed.w) {
        //                 h[ed.v] = h[u] + ed.w;
        //                 changed = true;
        //             }
        //         }
        //     }
        //     if (!changed) break;
        // }
        // for (int i = 0; i <= n; i++) if (h[i] == INF) h[i] = 0;

        for (int i = 0; i <= n; i++) if (h[i] == INF) h[i] = 0;
        i64 last_dist_t = INF;
        while (dijkstra(s, t)) {
            for (int i = 0; i <= n; i++) {
                if (dist[i] < INF) h[i] += dist[i];
            }

            for (int i = 0; i <= n; ++i) cur[i] = 0;
            int Spush = 0;
            while (1) {
                int push = find_flow(s, t, INF);
                if (!push) break;
                Spush += push;
                flow += push;
                cost += push * h[t];
            }

            if (Spush == 0 && dist[t] == last_dist_t) break;
            last_dist_t = dist[t];
        }
        return make_pair(flow, -cost);
    }
};

```

# 在有上下界的流网络中求最大流

### 无源汇上下界可行流

# 待补充