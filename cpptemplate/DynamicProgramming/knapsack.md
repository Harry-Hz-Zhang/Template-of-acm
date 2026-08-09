---
topic: "背包问题"
category: "10-dp"
source: "动态规划 DP.md"
---

# 背包问题
## 常见板子

```C++
// 常见（State transitions）回顾：
// 0/1:   f[i][j] = max( f[i-1][j], f[i-1][j - v[i]] + w[i] )
// 完全:   f[i][j] = max( f[i-1][j], f[i][j - v[i]] + w[i] )
// 分组:   f[g][j] = max_{item in group g}( f[g-1][j - v_item] + w_item )
// 树形:   在 dfs 合并子树时做卷积：合并子 f 到父 dp（背包卷积）
// 依赖:   若选子必须选父 -> 初始化 f[u][v[u]] = w[u]（不填 0），合并子树时将子树作为可选增量
struct Bag {
    // ================= 0/1 背包（二维 DP + 回溯） =================
    // 输入：n, m, v[1..n], w[1..n]
    // 返回：{maxValue, st} 其中 st[i] = 1 表示选第 i 件物品（回溯恢复一种方案）
    // 地推：f[i][j] = max(f[i - 1][j], f[i - 1][j - v[i]] + w[i])
	static pair<int, vector<int>> zero_one_bag(int n, int m, const vector<int>& v, const vector<int>& w) {
	    vector<vector<int>> f(n + 1, vector<int>(m + 1, -INF));
	    for (int i = 0; i <= max(n, m); i++) f[min(n, i)][0] = f[0][min(m, i)] = 0;
	    for (int i = 1; i <= n; i++) {
	        for (int j = 0; j <= m; j++) {
	            f[i][j] = max(f[i][j], f[i - 1][j]);
	            if (j >= v[i]) f[i][j] = max(f[i][j], f[i - 1][j - v[i]] + w[i]);
	        }
	    }
	    int ans = 0, t = 0;
	    for (int j = 0; j <= m; j++) 
	        if (f[n][j] > ans) { 
	            ans = f[n][j]; 
	            t = j; 
	        }
	    vector<int> st(n + 1, 0);
	    int i = n, j = t;
	    while (i > 0) {
	        if (j >= v[i] && f[i][j] == f[i - 1][j - v[i]] + w[i]) {
	            st[i] = 1; 
	            j -= v[i];
	        } else st[i] = 0;
	        i--;
	    }
	    return {ans, st};
	}
    // ================= 完全背包 =================
    // 二维回溯版（可以恢复“是否至少选过某种物品”的一种方案）
    // 递推： f[i][j] = max(f[i - 1][j], f[i][j - v[i]] + w[i])
    static pair<int, vector<int>> complete_2D(int n, int m, const vector<int>& v, const vector<int>& w) {
        vector<vector<int>> f(n + 1, vector<int>(m + 1, -INF));
        for (int i = 0; i <= max(n, m); i++) f[min(n, i)][0] = f[0][min(m, i)] = 0;
        for (int i = 1;i <= n; i++) {
            for (int j = 0; j <= m; j++) {
                f[i][j] = max(f[i][j], f[i - 1][j]);
                if (j >= v[i]) f[i][j] = max(f[i][j], f[i][j - v[i]] + w[i]);
            }
        }
        int ans = 0, t = 0;
        for (int j = 0;j <= m; j++) if (f[n][j] > ans) { ans = f[n][j]; t = j; }

        vector<int> st(n + 1,0);
        int i = n,j = t;
        while (i > 0) {
            if (j >= v[i] && f[i][j] == f[i][j - v[i]] + w[i]) {
                st[i]++; j -= v[i];
            } else i--;
        }
        return {ans, st};
    }

    // 一维完全背包（竞赛常用写法，无法回溯）
    static vector<int> Complete_1D(int n, int m, const vector<int>& v, const vector<int>& w) {
        vector<int> f(m + 1, 0);
        for (int i = 1; i <= n; i++) {
            for (int j = v[i]; j <= m; j++) f[j] = max(f[j], f[j - v[i]] + w[i]);
        }
        return f;
    }

    // ================= 多重背包：二进制拆分（将 k 件拆成若干 0/1 项） ===========
    // 有 N 种物品和一个容量是 V 的背包。第 i 种物品最多有 cnti 件，每件体积是 vi，价值是 wi。
    // 求解将哪些物品装入背包，可使物品体积总和不超过背包容量，且价值总和最大。
    // 时间复杂度 O(m * sum log k_i)，常用于 cnt 较大时
    static pair<int, vector<int>> MultipleBinarySplit(int n, int m, const vector<int>& v, const vector<int>& w, const vector<int>& cnt) {
        struct Item { int v, w, org; };
        vector<Item> items(1);
        for (int i = 1; i <= n; i++) {
            int k = cnt[i], base = 1;
            while (k > 0) {
                int tmp = min(base, k);
                items.push_back({v[i] * tmp, w[i] * tmp, i});
                k -= tmp;
                base <<= 1;
            }
        }

        int N = items.size() - 1;
        vector<vector<int>> f(N + 1, vector<int>(m + 1, -INF));
        for (int i = 0; i <= max(N, m); i++) f[min(N, i)][0] = f[0][min(m, i)] = 0;

        for (int i = 1; i <= N; i++) {
            for (int j = 0; j <= m; j++) {
                f[i][j] = max(f[i][j], f[i - 1][j]);
                if (j >= items[i].v) f[i][j] = max(f[i][j], f[i - 1][j - items[i].v] + items[i].w);
            }
        }
        int ans = 0, t = 0;
        for (int j = 0; j <= m; j++) if (f[N][j] > ans) { ans = f[N][j]; t = j; }
        vector<int> stOrg(n + 1, 0LL);
        int i = N, j = t;
        while (i > 0) {
            if (j >= items[i].v && f[i][j] == f[i - 1][j - items[i].v] + items[i].w) {
                stOrg[items[i].org] = 1;
                j -= items[i].v;
            }
            i--;
        }
        return {ans, stOrg};
    }

    // ================= 多重背包：单调队列优化 =================
    // 参考转移：对于物品 i (V, W, C)，对每个 r in [0..V-1], 考虑 j = k*V + r，
    // f[j] = max_{t in [0..C]} ( prev[j - tV] + t*W )
    // 等价把序列转化为 k 空间，用单调队列维护凸性，时间 O(m)
    static vector<int> Multiple_MonotoneQueue(int n, int m, const vector<int>& v, const vector<int>& w, const vector<int>& cnt) {
        vector<int> f(m+1, INT_MIN/4);
        f[0]=0;
        for (int i=1;i<=n;++i) {
            int V=v[i], W=w[i], C=cnt[i];
            if (V==0) continue;
            for (int r=0;r<V;++r) {
                deque<pair<int,int>> dq; // (k, value = prev[k*V + r] - k*W)
                vector<int> prev;
                for (int j=r;j<=m;j+=V) prev.push_back(f[j]);
                int len = prev.size();
                for (int k=0;k<len;++k) {
                    int val = prev[k];
                    int key = val - k*W;
                    while (!dq.empty() && k - dq.front().first > C) dq.pop_front();
                    while (!dq.empty() && dq.back().second <= key) dq.pop_back();
                    dq.emplace_back(k,key);
                    int ans = dq.front().second + k*W;
                    f[r + k*V] = max(f[r + k*V], ans);
                }
            }
        }
        return f;
    }


    // ================= 分组背包（每组最多选 1 件） =================
    // groups: vector of groups, each group is vector<pair<v,w>>
    // 地推：对每组进行倒序容量枚举并尝试组内每个选项
    static pair<int, vector<int>> GroupKnapsack(const vector<vector<pair<int,int>>>& groups, int m) {
        int G = (int)groups.size();
        vector<int> f(m + 1, INT_MIN / 4), ndp;
        vector<vector<int>> dp_before(G);
        f[0]=0;
        for (int g=0; g < G; g++) {
            dp_before[g] = f;
            ndp = f;
            for (auto &it: groups[g]) {
                int V = it.first, W = it.second;
                for (int j=m;j>=V;--j) ndp[j] = max(ndp[j], f[j - V] + W);
            }
            f.swap(ndp);
        }
        int ans=0, t=0;
        for (int j=0;j<=m;++j) if (f[j] > ans) { ans = f[j]; t = j; }
        // 回溯：简单恢复每组选中项的索引（-1 表示不选）
        vector<int> st(G, -1);
        int cur_j = t;
        for (int g=G-1; g>=0; --g) {
            bool found = false;
            for (int idx=0; idx<(int)groups[g].size(); ++idx) {
                int V = groups[g][idx].first, W = groups[g][idx].second;
                if (cur_j>=V && f[cur_j] == dp_before[g][cur_j - V] + W) {
                    st[g] = idx; cur_j -= V; found = true; break;
                }
            }
            // 若未找到，则不选该组
        }
        return {ans, st};
    }


    // ================= 树形背包（普通：节点可独立选择） =================
    // 给定树，每个节点有 (v[i], w[i])，节点可独立选择（选子不强制选父）
    // 做法：DFS 合并子树 dp（卷积）
    static vector<int> tree_knapsack(int n, int m, const vector<int>& v, const vector<int>& w, const vector<vector<int>>& adj, int root=1) {
        function<vector<int>(int,int)> dfs = [&](int u, int parent) -> vector<int> {
            vector<int> f(m+1, INT_MIN/4);
            f[0] = 0;
            for (int to: adj[u]) if (to != parent) {
                vector<int> child = dfs(to, u);
                vector<int> ndp(m+1, INT_MIN/4);
                for (int i=0;i<=m;++i) if (f[i] > INT_MIN/8) {
                    for (int j=0;j+i<=m;++j) if (child[j] > INT_MIN/8) {
                        ndp[i+j] = max(ndp[i+j], f[i] + child[j]);
                    }
                }
                f.swap(ndp);
            }
            // 最后考虑是否选 u 本身（倒序枚举或基于 f 前状态）
            vector<int> dp2 = f;
            for (int j=m;j>=v[u];--j) if (f[j - v[u]] > INT_MIN/8) dp2[j] = max(dp2[j], f[j - v[u]] + w[u]);
            return dp2;
        };
        return dfs(root, -1);
    }

    // ================= 依赖背包（若选子则必须选父） =================
    // 正确实现思路：把依赖关系建成森林并与虚根 0 相连。
    // 对于每个节点 u，只有在选 u 时才可以选它的子树。于是初始化 f[u] 只在体积 >= v[u] 有值（代表至少选 u），
    // 合并子树时要保留“不选该子树”的可能（即合并时先保留父的 dp，再把子树的选项作为可选增量合并）。
    // 返回值：对虚根 0 的 f 向量（包含各种容量下的最优值）
    static vector<int> DependentKnapsackCorrect(int n, int m, const vector<int>& v, const vector<int>& w, const vector<int>& parent) {
        vector<vector<int>> children(n+1);
        int root = 0;
        for (int i=1;i<=n;++i) {
            if (parent[i] == 0) children[root].push_back(i);
            else children[parent[i]].push_back(i);
        }
        // extend arrays with index 0
        vector<int> v2(n+1), w2(n+1);
        for (int i=1;i<=n;++i) { v2[i] = v[i]; w2[i] = w[i]; }
        v2[0] = w2[0] = 0;
        function<vector<int>(int)> dfs = [&](int u)->vector<int> {
            vector<int> f(m+1, INT_MIN/4);
            if (u != 0) {
                if (v2[u] <= m) f[v2[u]] = w2[u]; // 选 u（至少要占 v2[u] 容量）
            } else {
                f[0] = 0; // 虚根可以不选
            }
            // 合并每个子树：记得保留“不选子树”的情形（即先把 f 拷贝进去）
            for (int ch: children[u]) {
                vector<int> child = dfs(ch);
                vector<int> ndp = f; // 先保留不选 child 的情况
                for (int i=0;i<=m;++i) if (f[i] > INT_MIN/8) {
                    for (int j=0;j+i<=m;++j) if (child[j] > INT_MIN/8) {
                        ndp[i+j] = max(ndp[i+j], f[i] + child[j]);
                    }
                }
                f.swap(ndp);
            }
            return f;
        };
        return dfs(0);
    }
};
```

## 方案回溯

### 完全背包

* 设定一个 `vector<PII> path`  记录下每次体积改变时选中的物品编号

```C++
vector<vector<int>> f(n + 1, vector<int>(k + 1, 0));  // 前i个数字里面选择之后数字和恰好为j能否做到
vector<PII> path(k + 1);  // 记录一下当前体积为 i 的上一步体积是多少
f[0][0] = 1;
for (int i = 1; i <= n; i++) {  
	for (int j = 0; j <= k; j++) {
		f[i][j] = f[i - 1][j];
		if (j - a[i] >= 0 && f[i][j - a[i]]) {
			f[i][j] = 1;
			path[j] = {j - a[i], i};
			// 体积为 j 的上一步是 j - a[i];
			// 把第i号物品拿过来之后进行的转移
		}
	}
}
if (!f[n][k]) {
	cout << -1 << endl;
	return;
}
vector<int> nums;
int curr = k;
while(curr > 0) {
	auto [pre, x] = path[curr];
	nums.emplace_back(x);
	curr = pre;
}
```

* 附一个一维写法
```C++
vector<int> f(k + 1, 0);  // 前i个数字里面选择之后数字和恰好为j能否做到
vector<PII> path(k + 1);  // 记录一下当前体积为 i 的上一步体积是多少
f[0] = 1;
for (int i = 1; i <= n; i++) {  // （以倒数第n行为开始的后缀）（倒数第n - 1行开始的）。。
	for (int j = a[i]; j <= k; j++) {
		if (f[j - a[i]] && !f[j]) {
			f[j] = 1;
			path[j] = {j - a[i], i};
			// 体积为 j 的上一步是 j - a[i];
			// 把第i号物品拿过来之后进行的转移
		}
	}
}
if (!f[k]) {
	cout << -1 << endl;
	return;
}
vector<int> nums;
int curr = k;
while(curr > 0) {
	auto [pre, x] = path[curr];
	nums.emplace_back(x);
	curr = pre;
}
```

***
