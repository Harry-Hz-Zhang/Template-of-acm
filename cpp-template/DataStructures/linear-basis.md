---
topic: "线性基"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 线性基

### (1) 类高斯消元线性基

```cpp
struct Guess_basis {  // 1-based
  public:
    int n;
    int len = 0;
    int bit = 62;
    bool zero = 0;

    vector<i64> ba;
    Guess_basis() : n(0), len(0) { }
    Guess_basis(vector<i64> &a_) : len(0) {
        n = (int)a_.size() - 1;
        ba = a_;
        int cur = 1;
        for (int i = bit; i >= 0; --i) {
            int p = -1;
            for (int j = cur; j <= n; ++j) {
                if (((ba[j] >> i) & 1ULL) != 0) {
                    p = j;
                    break;
                }
            }
            if (p == -1) continue;
            swap(ba[p], ba[cur]);
            for (int j = 1; j <= n; ++j) {
                if (j != cur && (((ba[j] >> i) & 1ULL) != 0)) {
                    ba[j] ^= ba[cur];
                }
            }
            ++cur; 
        }
        len = cur - 1;
        zero = (len < n);
    }
    int query_max() {
        int Max = 0;
        for (int i = 1; i <= len; i++) {
            Max ^= ba[i];
        }
        return Max;
    }
    int query_k(int k) {
        if (zero && k == 1) {
            return 0;
        }
        if (zero) {
            k--;
        }
        if (k >= (1LL << len)) {
            return -1;
        }
        int ans = 0;
        for (int i = len, j = 0; i >= 1; i--, j++) {
            if (k >> j & 1) {
                ans ^= ba[i];
            }
        }
        return ans;
    }
};
```

### (2) 在线 / 时间戳 线性基

**0-base**

```C++
struct basis {
  public:
    int BIT = 63;
    vector<int> a;
    vector<int> t;

    basis() {
        a.assign(BIT, 0LL); // indices 0 .. BIT-1
        t.assign(BIT, -1);
    }
    // 高位优先插入（BIT - 1 .. 0）
    void insert(int x, int y = INF) {
        for (int i = BIT - 1; i >= 0; i--) {
            if ((x >> i & 1LL) == 0) continue;
            if (a[i] == 0) {
                a[i] = x;
                t[i] = y;
                return;
            }
            if (y > t[i]) {
                swap(a[i], x); swap(t[i], y);
            }
            x ^= a[i];
        }
    }
    bool query(int x, int y = 0) const {
        for (int i = BIT - 1; i >= 0; i--) {
            if (((x >> i) & 1LL) != 0 && t[i] >= y) x ^= a[i];
            if (x == 0) return true;
        }
        return x == 0;
    }
    int query_max(int x = 0) const {
        for (int i = BIT - 1; i >= 0; i--) {
            if ((x ^ a[i]) > x) x ^= a[i];
        }
        return x;
    }
};
```

```cpp
#include <bits/stdc++.h>
#define int long long
using namespace std;
const int M = 60;
int p[M + 5];

void init() {
	for (int i = 0; i <= M; i++) p[i] = 0;
}
void ins(int x) {
	for (int i = M; i >= 0; i--) {
		if (((x >> i) & 1) == 0) continue;
		if (!p[i]) {
			p[i] = x;
			return;
		}
		x ^= p[i];
	}
}

bool query(int x) {
	for (int i = M; i >= 0; i--) {
		if (((x >> i) & 1) == 0) continue;
		if (!p[i]) return false;
		x ^= p[i];
	}
	return true;
}

int getMax(int x = 0) {
	for (int i = M; i >= 0; i--) {
		if ((x ^ p[i]) > x) x ^= p[i];
	}
	return x;
}

signed main() {
	init();
	int n;
	cin >> n;
	for (int i = 1; i <= n; i++) {
		int x;
		cin >> x;
		ins(x);
	}
	int q;
	cin >> q;
	while (q--) {
		int x;
		cin >> x;
		if (query(x)) cout << "Yes\n";
		else cout << "No\n";
	}
	return 0;
}

```

### (3) 还原方案 basis

```C++
struct basis {
  public:
    const int BIT = 63;
    int sz;
    vector<int> a;
    vector<int> from, mask;

    basis() : sz(0), a(BIT), from(BIT, -1), mask(BIT) {}
    bool insert(int x, int id) {
        int now = 0;
        for (int i = BIT - 1; i >= 0; i--) {
            if (x >> i & 1) {
                if (a[i] == 0) {
                    a[i] = x;
                    from[i] = id;
                    mask[i] = now | (1 << i);
                    sz ++;
                    return 1;
                } else {
                    x ^= a[i];
                    now ^= mask[i];
                }
            }
        }
        return 0;
    }
 
    pair<bool, vector<int>> cal(int init) {
        int now = 0;
        for (int i = BIT - 1; i >= 0; i--) {
            if (init >> i & 1) {
                if (a[i] == 0) return {false, {}};
                init ^= a[i];
                now ^= mask[i];
            }
        }
        vector<int> res;
        for (int i = 0; i < BIT; i++) {
            if ((now >> i) & 1) {
                if (from[i] != -1) res.push_back(from[i]);
            }
        }
        return {true, res};
    }
};
```
