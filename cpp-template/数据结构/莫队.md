---
topic: "莫队"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 莫队
* O( $n\sqrt n$)
* 奇偶排序：
	* $l$ 所在的块号
	* 如果块号为奇数，$r$ 从小到大
	* 如果块号为偶数，$r$ 从大到小

```cpp
    struct query {
        int id, l, r;
    };
    vector<query> q(m);  // 
    for (int i = 0; i < m; ++i) {
        cin >> q[i].l >> q[i].r;
        q[i].id = i;
    }
    int siz = max(1LL, (int)(n / sqrt(max(1LL, m))));
    sort(q.begin(), q.end(), [&](const query& x, const query& y) {
        int bx = x.l / siz, by = y.l / siz;
        if (bx != by) return bx < by;
        return (bx & 1) ? x.r < y.r : x.r > y.r;
    });
    int res = 0; 
    vector<int> cnt(n + 1, 0);
    vector<int> ans(m);
    auto add = [&](int idx) -> void {

    };
    auto sub = [&](int idx) -> void {

    };

    int L = 1, R = 0;
    for (const auto& [id, l, r] : q) {
        while (L > l) add(--L);
        while (R < r) add(++R);
        while (L < l) sub(L++);
        while (R > r) sub(R--);
        
        ans[id] = res;
    }
    for (int i = 0; i < m; i++) {
        
    }
    
```

### (1) 查询某个区间内不同元素个数是否even

```C++
vector<int> cnt(1e6 + 1);
struct MOA {
  public:
	struct query {
		int id, l, r;
	};
	
	int siz, n, m;
	vector<query> q;
	MOA () { }
	MOA (int n_, int m_): n(n_), m(m_), siz(sqrt(n_)) {
		q.resize(m + 1);
	}
	int bel(int x) {
		return (x - 1) / siz + 1;
	}
	void insert(int i, int l, int r) {
		q[i] = {i, l, r};
	}
	void sort() {
		std::sort(q.begin() + 1, q.end(), [&](query x, query y) {
			return bel(x.l) == bel(y.l) ? x.r < y.r : bel(x.l) < bel(y.l);
		});
	}
	void add(int x, int &res) {
		if (cnt[x] & 1) res--;
		else res++;
		cnt[x]++;
	}
	void sub(int x, int &res) {
		if (cnt[x] & 1) res--;
		else res++;
		cnt[x]--;
	}
};
  
void solve()
{  
	int n, q;
	cin >> n >> q;
	vector<int> a(n + 1);
	for (int i = 1; i <= n; i++){
		cin >> a[i];
		cnt[a[i]] = 0;
	}
	MOA moa(n, q);  
	for (int i = 1; i <= q; i++) {
		int l, r;
		cin >> l >> r;
		moa.insert(i, l, r);
	}
  
	moa.sort();
	vector<int> ans(q + 1);
	int i = 1, j = 0, res = 0;
	for (int k = 1; k <= q; k++) {
		auto [id, l, r] = moa.q[k];
		while(i > l) moa.add(a[--i], res);
		while(j < r) moa.add(a[++j], res);
		while(j > r) moa.sub(a[j--], res);
		while(i < l) moa.sub(a[i++], res);
		ans[id] = res;
	}
  
	for (int i = 1; i <= q; i++) {
		cout << ((ans[i] == 0) ? "YES" : "NO") << endl;
	}
	cnt.clear();
}
```

### (2) 二分查询某个区间中出现频次大于阈值的元素

```C++
template<class Info>
class ZKW_segment_tree {
  public:
    int N = 1;
    int n = 0;
    vector<Info> info;

    ZKW_segment_tree() { }
    template<class T>
    ZKW_segment_tree(vector<T> init_) {
        n = (int)init_.size() - 1;
        while (N < n) N <<= 1;
        info.assign((N << 1) + 2, Info());

        for (int i = 1; i <= n; i++) info[i + N - 1] = init_[i];
        for (int i = N - 1; i >= 1; --i) info[i] = info[i << 1] + info[i << 1 | 1];
    }

    void modify(int x, const Info& v) {
        int idx = x + N - 1;
        info[idx] = v;
        for (idx >>= 1; idx; idx >>= 1) info[idx] = info[idx << 1] + info[idx << 1 | 1];
    }
    Info range_query(int l, int r) {
        Info ans = Info();
        if (l > r) return ans;
        int L = N + l - 1, R = N + r - 1;
        while (L <= R) {
            if (L & 1) ans = ans + info[L++];
            if (!(R & 1)) ans = ans + info[R--];
            L >>= 1; R >>= 1;
        }
        return ans;
    }

    int find_first(int idx, int l, int r, int ql, int qr, int f) {
        if (l > qr || r < ql) return -1;
        if (info[idx].Max < f) return -1;
        if (l == r) {
            if (l <= n) return l;
            return -1;
        }
        int mid = l + r >> 1;
        int t = find_first(idx << 1, l, mid, ql, qr, f);
        if (t != -1) return t;
        return find_first(idx << 1 | 1, mid + 1, r, ql, qr, f);
    }

    int find_first(int ql, int qr, int f) {
        if (ql > qr) return -1;
        if (range_query(ql, qr).Max < f) return -1;
        return find_first(1, 1, N, ql, qr, f);
    }
};

struct Info {
    int Max = 0;
    Info() { }
    Info(int _) : Max(_) { };
};
Info operator+(const Info &l, const Info &r) {
    if (l.Max >= r.Max) return l;
    if (r.Max > l.Max) return r;
    return l;
};

struct MOA {
    struct query {
        int id, l, r;
    };
    // array_size query_num
    int siz, n, m;
    vector<query> q;
    MOA () { }
    MOA (int n_, int m_): n(n_), m(m_), siz(sqrt(n_)) {
        q.resize(m);
    }
    int bel(int x) {
        return (x - 1) / siz + 1;
    }
    void insert(int i, int l, int r) {
        q[i - 1] = {i, l, r};
    }
    void sort() {
        std::sort(q.begin(), q.end(), [&](query x, query y) {
            return bel(x.l) == bel(y.l) ? ((bel(x.l) & 1) ? x.r < y.r : x.r > y.r) : bel(x.l) < bel(y.l);
        });
    }
};

void solve()
{
    int n, m;
    cin >> n >> m;
    vector<int> a(n + 1), alls;
    for (int i = 1; i <= n; i ++ ) cin >> a[i], alls.push_back(a[i]);

    sort(alls.begin(), alls.end());
    alls.erase(unique(alls.begin(), alls.end()), alls.end());
    auto find = [&](int x) -> int {
        return lower_bound(alls.begin(), alls.end(), x) - alls.begin() + 1;
    };

    for (int i = 1; i <= n; i ++ ) a[i] = find(a[i]);
    MOA mo(n, m);
    for (int i = 1; i <= m; i ++ ) {
        int l, r;
        cin >> l >> r;
        mo.insert(i, l, r);
    }

    mo.sort();
    vector<Info> info(alls.size() + 1, {0});
    ZKW_segment_tree<Info> seg(info);
    int i = 1, j = 0;

    vector<vector<int>> ans(m + 1);
    vector<int> cnt(alls.size() + 1, 0);
    for (auto& [id, l, r] : mo.q) {
        while(i > l) {
            cnt[a[--i]] ++;
            seg.modify(a[i], {cnt[a[i]]});
        }
        while(j < r) {
            cnt[a[++j]] ++;
            seg.modify(a[j], {cnt[a[j]]});
        }
        while(i < l) {
            cnt[a[i]] --;
            seg.modify(a[i], {cnt[a[i]]});
            i++;
        }
        while(j > r) {
            cnt[a[j]] --;
            seg.modify(a[j], {cnt[a[j]]});
            j--;
        }

        int res = (r - l + 1) / 3 + 1;
        auto it = seg.find_first(1, (int)alls.size(), res);

        if (it == -1) {
            ans[id].push_back(-1);
            continue;
        } else {
            int p = it;
            ans[id].push_back(alls[p - 1]);
            it = seg.find_first(p + 1, (int)alls.size(), res);
            if (it == -1) {
                continue;
            } else {
                ans[id].push_back(alls[it - 1]);
            }
        }
    }
    for (int i = 1; i <= m; i ++ ) {
        for (auto x : ans[i]) cout << x << ' ';
        cout << '\n';
    }
}
```
