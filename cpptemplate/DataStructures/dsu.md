---
topic: "并查集 DSU"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 并查集 DSU

```C++
	auto get_id = [&](int i, int j) -> int {
		return (i - 1) * (m) + j;
	};
	for (int i = 1; i <= n * m; i++) { 
		int x = (i - 1) / m + 1, y = (i - 1) % m + 1; 
	}
```

### (1) 一般并查集
```C++
struct dsu {
  public:
    int _n;
    vector<int> f, siz;

	dsu() : _n(0) { }
	explicit dsu(int n) : _n(n) { init(n); }
	void init(int n) {
		_n = n;
		f.resize(n + 1);
		iota(f.begin(), f.end(), 0LL);
		siz.assign(n + 1, 1);
	}
	int find(int x) {
        assert(0 <= x && x <= _n);
		while(x != f[x]) {
			x = f[x] = f[f[x]];
		}
		return x;
	}
	bool same(int x, int y) {
        assert(0 <= x && x <= _n); assert(0 <= y && y <= _n);
		return find(x) == find(y);
	}
	bool merge(int x, int y) {
        assert(0 <= x && x <= _n);
        assert(0 <= y && y <= _n);
		x = find(x), y = find(y);
		if(x == y) {
			return 0;
		}
		siz[y] += siz[x];
		f[x] = y;
		return 1;
		
	}
	int size(int x) {
        assert(0 <= x && x <= _n);
		return siz[find(x)];
	}
};
```

* 并查集为区间中的每个点定义一个指针，指向下一个点

```C++
for (int i = dsu.find(l); i <= r; i = dsu.find(i + 1)) {
    // 1. 执行你的操作
    // ...

    // 2. 判断是否满足“失效/删除”条件
    if ( /* 比如 a[i] 变成 0 了 */ ) {
        dsu.fa[i] = i + 1; // 将当前位置指向右边
    }
}
```

### (2) 带权并查集

* 给定好多区间，询问某个区间的和是多少，距离是多少，维护倍数，维护异或值
* 查询区间是否和已知区间产生冲突
* 算距离时候是 dist[后] - dist[前] + w, 这里可能不是加减法

```C++
class dsu_2 {
  private:
    int _n;
    vector<int> f, siz;
    vector<i64> dis;
  public:
    dsu_2() : _n(0) { }
    dsu_2(int n): _n(n) { init(n); }
    void init(int n) {
        f.resize(n + 1);
        dis.resize(n + 1);
        iota(f.begin(), f.end(), 0);
        siz.assign(n + 1, 1);
    }

    function<int(int)> find = [&](int x) {
        assert(0 <= x && x <= _n);
        if (x == f[x]) return x;
        find(f[x]); dis[x] += dis[f[x]];
        return f[x] = f[f[x]];
    };

    bool same(int x, int y) {
        assert(1 <= x && x <= _n); assert(1 <= y && y <= _n);
        return find(x) == find(y);
    }
    bool merge(int x, int y, i64 w) {
        assert(1 <= x && x <= _n);
        assert(1 <= y && y <= _n);

        int xf = find(x), yf = find(y);
        if (xf == yf) return 0;
        siz[yf] += siz[xf];
        f[xf] = yf;
        dis[xf] = -dis[x] + w + dis[y];
        return 1;
    }
    int dist(int x, int y) {
        assert(1 <= x && x <= _n);
        assert(1 <= y && y <= _n);
        
        int xf = find(x), yf = find(y);
        if (xf != yf) return -1;
        return dis[x] - dis[y];
    }
    int size(int x) {
        return siz[find(x)];
    }
};
```

eg: XOR
```C++
class dsu_2 {
  private:
    int _n;
    vector<int> f, siz;
    vector<i64> dis;
  public:
    dsu_2() : _n(0) { }
    dsu_2(int n): _n(n) { init(n); }
    void init(int n) {
        f.resize(n + 1);
        dis.resize(n + 1);
        iota(f.begin(), f.end(), 0);
        siz.assign(n + 1, 1);
    }

    function<int(int)> find = [&](int x) {
        assert(1 <= x && x <= _n);
        if (x == f[x]) return x;
        find(f[x]); 
        dis[x] ^= dis[f[x]];
        return f[x] = f[f[x]];
    };

    bool same(int x, int y) {
        assert(1 <= x && x <= _n); assert(1 <= y && y <= _n);
        return find(x) == find(y);
    }
    bool merge(int x, int y, i64 w) {
        assert(1 <= x && x <= _n);
        assert(1 <= y && y <= _n);

        int xf = find(x), yf = find(y);
        if (xf == yf) return 0;
        if (xf == 0) swap(xf, yf), swap(x, y);
        f[xf] = yf;
        siz[yf] += siz[xf];
        dis[xf] = dis[y] ^ dis[x] ^ w;
        return 1;
    }
    int dist(int x, int y) {
        assert(1 <= x && x <= _n);
        assert(1 <= y && y <= _n);
        
        int xf = find(x), yf = find(y);
        if (xf != yf) return -1;
        return dis[x] ^ dis[y];
    }
    int size(int x) {
        return siz[find(x)];
    }
};
```
### (3) 启发式合并 std::list\<T>

```C++
struct dsu {
  public:
	vector<int> f, siz;
    vector<std::list<int>> mem;
	dsu() { }
	dsu(int n) {
		init(n);
	}
	void init(int n) {
		f.resize(n + 1);
        mem.resize(n + 1);
		for (int i = 1; i <= n; i++) {
            f[i] = i;
            mem[i].push_back(i);
        }
		siz.assign(n + 1, 1);
	}
	int find(int x) {
		while(x != f[x]) {
			x = f[x] = f[f[x]];
		}
		return x;
	}
	bool same(int x, int y) {
		return find(x) == find(y);
	}
	bool merge(int x, int y) {
		x = find(x); y = find(y);
		if(x == y) {
			return 0;
		}
        if (siz[x] > siz[y]) swap(x, y);
        mem[y].splice(mem[y].end(), mem[x]);
		siz[y] += siz[x];
		f[x] = y;
		return 1;
		
	}
	int size(int x) {
		return siz[find(x)];
	}
};
```

### (5) 可撤销并查集 rollback

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

```
