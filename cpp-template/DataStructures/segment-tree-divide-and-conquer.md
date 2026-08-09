---
topic: "(5) 线段树分治"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

### 线段树分治

```C++
struct op {
    int t, a, b;
};
class dsu {
  public:
	vector<int> f, siz;
    stack<op> save;

	dsu() { }
	dsu(int n) { init(n); }
	void init(int n) {
		f.resize(n + 1);
		iota(range(f), 0);
		siz.assign(n + 1, 1);
	}
	int find(int x) {
        return f[x] == x ? x : find(f[x]);
	}
	bool same(int x, int y) {
		return find(x) == find(y);
	}
	bool merge(int x, int y) {
		x = find(x); y = find(y);
		if(x == y) { return 0; }
        if (siz[x] > siz[y]) { 
            swap(x, y); 
        }
        save.push({1, x, y});
		siz[y] += siz[x];
		f[x] = y;
		return true;
	}
    void roll_back() {
        auto [t, x, y] = save.top();
        save.pop();

        if (t == 1) {
            siz[y] -= siz[x];
            f[x] = x;
        } else { }
    }
    size_t get_snapshot() const { return save.size(); }
    void roll(int tar) {
        while(save.size() > tar) { roll_back(); }
    }

	int size(int x) {
		return siz[find(x)];
	}
};

vector<char> ans;
vector<op> opt; 

template<typename T>
struct segment_tree_DC {
  public:
    int tot;          // 时间点数（叶子数量）
    vector<vector<T>> tr;        // 每个节点的操作列表

    segment_tree_DC(): tot(0LL) {}
    segment_tree_DC(int _T) { init(_T); }
    void init(int _T) {
        tot = max(1LL, _T);
        tr.clear();
        tr.resize(4LL * (tot + 5));
    }

    // 插入一个操作 op 到闭区间 [l, r]
    void insert_op(int p, int L, int R, int l, int r, const T& op) {
        if (l > r || l > R || r < L) return;
        if (l <= L && R <= r) {
            tr[p].push_back(op);
            return;
        }
        int mid = L + R >> 1;
        insert_op(p << 1, L, mid, l, r, op);
        insert_op(p << 1 | 1, mid + 1, R, l, r, op);
    }
    void insert_op(int l, int r, const T& op) {
        if (l > r) return;
        insert_op(1, 1, tot, l, r, op);
    }
    void dfs(DSU &dsu) {
        function<void(int,int,int)> dfs = [&](int p, int l, int r) {
            size_t snap = dsu.get_snapshot();
            for (auto &e : tr[p]) {
                dsu.merge(e.first, e.second);
            }
            if (l == r) {
                if (opt[l].t == 2) {  // 查询某两个点是否连通
                    int x = opt[l].a, y = opt[l].b;
                    if (dsu.same(x, y)) ans.push_back('Y');
                    else ans.push_back('N');
                }
            } else {
                int mid = (l + r) >> 1;
                dfs(p << 1, l, mid);
                dfs(p << 1 | 1, mid + 1, r);
            }
            dsu.roll(snap);
        };
        dfs(1, 1, tot);
    }
};
void solve()
{
    int n, m;
    cin >> n >> m;
    opt.resize(m + 1);
    for (int i = 1; i <= m; i++) {
        auto &[ty, u, v] = opt[i];
        cin >> ty >> u >> v;
        if (u > v) swap(u, v);  // 保证哈希的顺序 小大
    }
    map<PII, int> la;
    segment_tree_DC<PII> seg(m + 1);
    for (int i = 1; i <= m; i++) {
        auto &[ty, u, v] = opt[i];
        if (ty == 0) {
            la[{u, v}] = i;
        } else if (ty == 1) {
            seg.insert_op(la[{u, v}], i - 1, make_pair(u, v));
            la.erase({u, v});  // 删除，避免歧义
        }
    }
    for (auto &kv : la) {
        seg.insert_op(kv.second, m, kv.first);  // 最后的部分也要加上
    }
    DSU dsu(n + 1);
    seg.dfs(dsu);
    for (auto ch : ans) {
        cout << ch << endl;
    }
}
```

eg: https://codeforces.com/contest/2158/problem/E

```C++
int dx[4] = {0, 1, 0, -1}, dy[4] = {1, 0, -1, 0};
struct op {
    int t, a, b;
};
class dsu{
  public:
	vector<int> f, siz, sum;
    stack<op> save;
    
    int cnt0 = 0;  // 出度 = 0 的个数

	dsu() { }
	dsu(int n) { init(n); }
	void init(int n) {
		f.resize(n + 1);
		iota(range(f), 0);
		siz.assign(n + 1, 1);
        sum.resize(n + 1, 0);
        cnt0 = n;
	}

	int find(int x) {
        return f[x] == x ? x : find(f[x]);
	}
	bool same(int x, int y) {
		return find(x) == find(y);
	}
	bool merge(int x, int y) {
		x = find(x); y = find(y);
		if(x == y) { return 0; }
        if (siz[x] > siz[y]) { 
            swap(x, y); 
        }
        save.push({1, x, y});
        if (!sum[x]) cnt0 --;
        if (!sum[y]) cnt0 --;

		siz[y] += siz[x];
		f[x] = y;
        sum[y] += sum[x];

        if (!sum[y]) cnt0++;
		return true;
	}

    void add(int v, int x) {
        v = find(v);
        save.push({2, v, x});

        if (sum[v] == 0) cnt0--;
        sum[v] += x;
        if (sum[v] == 0) cnt0++;
    }

    void rollback() {
        auto [t, x, y] = save.top();
        save.pop();

        if (t == 1) {
            if (!sum[y]) cnt0--;

            sum[y] -= sum[x];
            siz[y] -= siz[x];
            f[x] = x;

            if (!sum[x]) cnt0++;
            if (!sum[y]) cnt0++;
        } else {    
            if (!sum[x]) cnt0--;

            sum[x] -= y;

            if (!sum[x]) cnt0++;
        }
    }
    size_t getSnapshot() const { return save.size(); }
    void roll(int tar) {
        while(save.size() > tar) { rollback(); }
    }

	int size(int x) {
		return siz[find(x)];
	}
};

template<typename T>
struct segment_tree_DC {
  public:
    int tot;          // 时间点数（叶子数量）
    vector<vector<T>> tr;        // 每个节点的操作列表
    vector<vector<T>> upd;

    segment_tree_DC(): tot(0LL) { }
    segment_tree_DC(int _T) { init(_T); }
    void init(int _T) {
        tot = max(1, _T);
        tr.clear(); 
        upd.clear();
        tr.resize(4LL * (tot + 5));
        upd.resize(4LL * (tot + 5));
    }

    // 插入一个操作 op 到闭区间 [l, r]
    void insert_op(int p, int L, int R, int l, int r, const T& op) {
        if (l > r || l > R || r < L) return;
        if (l <= L && R <= r) {
            tr[p].push_back(op);
            return;
        }
        int mid = L + R >> 1;
        insert_op(p << 1, L, mid, l, r, op);
        insert_op(p << 1 | 1, mid + 1, R, l, r, op);
    }
    void insert_op(int l, int r, const T& op) {
        if (l > r) return;
        insert_op(1, 0, tot - 1, l, r, op);
    }

    void insert_add(int p, int L, int R, int l, int r, const T& op) {
        if (l > r || l > R || r < L) return;
        if (l <= L && R <= r) {
            upd[p].push_back(op);
            return;
        }
        int mid = L + R >> 1;
        insert_add(p << 1, L, mid, l, r, op);
        insert_add(p << 1 | 1, mid + 1, R, l, r, op);
    }
    void insert_add(int l, int r, const T& op) {  // 更新出度！！！
        if (l > r) return;
        insert_add(1, 0, tot - 1, l, r, op);
    }

    void dfs(DSU &dsu) {
        function<void(int,int,int)> dfs = [&](int p, int l, int r) {
            size_t snap = dsu.getSnapshot();
            for (auto &e : tr[p]) {
                dsu.merge(e.first, e.second);
            }

            for (auto &e : upd[p]) {
                dsu.add(e.first, e.second);
            }
            if (l == r) {   
                cout << dsu.cnt0 << endl;
            } else {
                int mid = (l + r) >> 1;
                dfs(p << 1, l, mid);
                dfs(p << 1 | 1, mid + 1, r);
            }

            dsu.roll(snap);
        };
        dfs(1, 0, tot - 1);
    }
};

void solve()
{
    int n, m;
    cin >> n >> m;
    vector<vector<int>> a(n + 1, vector<int>(m + 1));

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            cin >> a[i][j];
        }
    }
    auto getId = [&](int i, int j) -> int {
        return (i - 1) * m + j;
    };

    map<PII, int> la;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            for (auto k = 0; k < 4; k++) {
                int cx = i + dx[k], cy = j + dy[k];
                if (cx < 1 || cx > n || cy < 1 || cy > m) continue;
                int u = getId(i, j);
                int v = getId(cx, cy);
                if (u > v) swap(u, v);

                if (a[i][j] == a[cx][cy]) la[{u, v}] = 0;
            }
        }
    }
    
    int q; 
    cin >> q;
    segment_tree_DC<PII> seg(q + 1);
    vector<tuple<int, int, int>> que(q + 1);
    
    for (int i = 1; i <= q; i++) {
        int r, c, x;
        cin >> r >> c >> x;
        
        que[i] = {r, c, x};
        int org = a[r][c];
        a[r][c] -= x;
        
        for (int k = 0; k < 4; k++) {
            int cx = r + dx[k], cy = c + dy[k];
            if (cx < 1 || cx > n || cy < 1 || cy > m) continue;
            int u = getId(r, c);
            int v = getId(cx, cy);
            if (u > v) swap(u, v);
            auto it = la.find({u, v});
            if (it != la.end() && org == a[cx][cy]) {
                seg.insert_op(it->second, i - 1, {u, v});
                la.erase(it);
            }
            if (a[r][c] == a[cx][cy]) {
                la[{u, v}] = i;
            }
        }
    }

    for (auto [edge, ti] : la) {
        seg.insert_op(ti, q, edge);
    }
    for (int i = 1; i <= q; i++) {
        auto [x, y, _x] = que[i];
        a[x][y] += _x;
    }
    vector<vector<int>> deg(n + 1, vector<int>(m + 1));  // 出度
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            int org = a[i][j];  // 原始的
            int u = getId(i, j);  // 
            for (auto k = 0; k < 4; k++) {
                int cx = i + dx[k], cy = j + dy[k];
                if (cx < 1 || cx > n || cy < 1 || cy > m) continue;
                int v = getId(cx, cy);
                if (org > a[cx][cy]) deg[i][j]++;
            }
            seg.insert_add(0LL, q, {u, deg[i][j]});
        }
    }

    for (int i = 1; i <= q; i++) {
        auto [r, c, x] = que[i];

        int org = a[r][c]; // 原始的
        int u = getId(r, c);  // 
        a[r][c] -= x;

        int nval = 0;
        for (int k = 0; k < 4; k++) {
            int cx = r + dx[k], cy = c + dy[k];
            if (cx < 1 || cx > n || cy < 1 || cy > m) continue;
            int v = getId(cx, cy);

            if (a[r][c] > a[cx][cy]) nval++;

            if (org >= a[cx][cy] && a[cx][cy] > a[r][c]) {
                seg.insert_add(i, q, {getId(cx, cy), 1});
                deg[cx][cy] ++;
            }
        }
        seg.insert_add(i, q, { u, nval - deg[r][c] });
        deg[r][c] = nval;
    }

    DSU dsu(n * m);
    seg.dfs(dsu);
}

signed main()
{
    cin.tie(nullptr) -> ios::sync_with_stdio(false);
    int T = 1;
    cin >> T;
    for (; T_ <= T; T_++) solve();
    return 0;
}
```
