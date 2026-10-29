---
topic: "二维前缀和 / 二维差分  Prefix / Diff"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 二维前缀和 / 二维差分  Prefix / Diff

```C++
struct prefix_2D {
  public:
	int n, m;
	vector<vector<int>> s;
	prefix_2D(const vector<vector<int>>& a) {
		n = a.size() - 1;
		m = a[0].size() - 1;
		s.assign(n + 1, vector<int>(m + 1, 0));
		for (int i = 1; i <= n; i++) {
			for (int j = 1; j <= m; j++) {
				s[i][j] = a[i][j] + s[i - 1][j] + s[i][j - 1] - s[i - 1][j - 1];
			}
		}
	}
	int sum(int x1, int y1, int x2, int y2) const {
		return s[x2][y2] - s[x1 - 1][y2] - s[x2][y1 - 1] + s[x1-1][y1-1];
	}
};

struct diff_2D {
  public:
	int n, m;
	vector<vector<int>> d;
	diff_2D(int _n = 0, int _m = 0) {
		n = _n; m = _m;
		d.assign(n + 2, vector<int>(m + 2, 0));
	}
    // 闭区间 [x1..x2] [y1..y2] 加 val
	void insert(int x1, int x2, int y1, int y2, int val = 1) {
		if (x1 > x2 || y1 > y2 || x1 > n || x2 < 1 || y1 > m || y1 < 1) return;
        x1 = std::max( (int)1, min(x1, (int)n) ); x2 = max( (int)1, min(x2, (int)n) );
        y1 = std::max( (int)1, min(y1, (int)m) ); y2 = max( (int)1, min(y2, (int)m) );
        if (x1 > x2 || y1 > y2) return;
		d[x1][y1] += val;
		d[x1][y2 + 1] -= val;
		d[x2 + 1][y1] -= val;
		d[x2 + 1][y2 + 1] += val;
	}

	vector<vector<int>> to_array() const {
		vector<vector<int>> a(n + 1, vector<int>(m + 1, 0));
		vector<vector<int>> tmp = d;
		for (int i = 1; i <= n; ++i) {
			for (int j = 1; j <= m; ++j) {
				tmp[i][j] += tmp[i - 1][j] + tmp[i][j - 1] - tmp[i - 1][j - 1];
				a[i][j] = tmp[i][j];
			}
		}
		return a;
	}
	prefix_2D to_prefix_sum_2D() const {
		auto a = to_array();
		return prefix_2D(a);
	}
};
```

* 四个角开始的二维前缀和

```C++
auto calc_2 = [&](int si, int sj, int ei, int ej, int di, int dj) -> void {
	vector<vector<int>> pre(n + 2, vector<int>(m + 2)), pre_ = pre;
	for (int i = si; i != ei + di; i += di) {
		for (int j = sj; j != ej + dj; j += dj) {
			pre[i][j] = pre[i - di][j] + pre[i][j - dj] - pre[i - di][j - dj] + a[i][j];
		}
	}
	for (int i = si; i != ei + di; i += di) {
		for (int j = sj; j != ej + dj; j += dj) {
			pre_[i][j] = pre[i][j] + pre_[i - di][j - dj];
		}
	}
};
calc_2(1, 1, n, m, 1, 1);
calc_2(1, m, n, 1, 1, -1);
calc_2(n, 1, 1, m, -1, 1);
calc_2(n, m, 1, 1, -1, -1);
```
