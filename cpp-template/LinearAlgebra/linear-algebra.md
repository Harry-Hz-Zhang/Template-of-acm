---
topic: "矩阵"
category: "04-linear-algebra"
source: "线性代数 Linear algebra.md"
---

# 矩阵

## 普通线性方程组 (Mod int)

```C++
int qpow(int a, int k) {
    a %= mod;
	i64 res = 1 % mod;
	while(k) {
		if (k & 1) res = (i64)res * a % mod;
		a = (i64)a * a % mod;
		k >>= 1;
	}
	return res;
}
int inv(int x) {
	return qpow(x, mod - 2);
}
template<typename T = int>
struct Matrix : public vector<vector<T>> {
    int n, m;
    Matrix(int _n = 0, int _m = 0, bool ident = false): vector<vector<T>>(_n + 1, vector<T>(_m + 1, 0)), n(_n), m(_m) {
        if (ident) { for (int i = 1; i <= min(n, m); i++) (*this)[i][i] = 1; }
    }
	Matrix(std::initializer_list<std::initializer_list<T>> init) {
        n = init.size(); m = init.begin()->size();
        this->assign(n + 1, vector<T>(m + 1));
        int i = 0;
        for (auto &row : init) {
            int j = 1;
            for (auto &val : row) {
                int x = val % mod;
                if (x < 0) x += mod;
                (*this)[i + 1][j++] = (T)x;
            }
            i++;
        }
	}
    friend istream &operator>>(istream &in, Matrix &B) {
        for (int i = 1; i <= B.n; i++) {
            for (int j = 1; j <= B.m; j++) {
                int x; in >> x;
                B[i][j] = x;
            }
        }
        return in;
    }
    friend ostream &operator<<(ostream &out, const Matrix &B) {
        for (int i = 1; i <= B.n; i++) {
            for (int j = 1; j <= B.m; j++) {
                out << B[i][j] << ' ';
            }
            out << '\n';
        }
        return out;
    }
    Matrix operator+ (const Matrix &B) const {
        assert(n == B.n && m == B.m);
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                int x = ( (*this)[i][j] + B[i][j] + mod) % mod; 
                (*this)[i][j] = x;
            }
        }
    }
    Matrix operator- (const Matrix &B) const {
        assert(n == B.n && m == B.m);
        for (int i = 1; i <= n; i++) for (int j = 1; j <= m; j++) {
            int x = ((*this)[i][j] - B[i][j] + mod) % mod;
            (*this)[i][j] = x;
        }
    }
    Matrix operator* (const Matrix &B) const {
        assert(m == B.n);
        Matrix C(n, B.m);
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= B.m; j++) {
                int sum = 0;
                for (int k = 1; k <= m; k++) {
                    (sum += ((*this)[i][k] * B[k][j] + mod) % mod) %= mod;
                }
                C[i][j] = sum;
            }
        }
        return C;
    }
    Matrix operator*(const T x) const {
        x %= mod;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                (*this)[i][j] = (T)((*this)[i][j] * x % mod);
            }
        }
    }
    friend Matrix operator*(const T x, const Matrix &A) { return A * x; }
    Matrix operator/(const T x) const {
        return (*this) * inv(x % mod);
    }
    Matrix pow(int e) const {
        assert(n == m);
        Matrix base = *this;
        Matrix res(n, n, true);
        while (e) {
            if (e & 1) res = res * base;
            base = base * base;
            e >>= 1;
        }
        return res;
    }

    int det() const {
        assert(n == m);
        Matrix &t = *this;

        int ans = 1;
        for (int i = 1; i <= n; i++) {
            int p = -1;
            for (int r = i; r <= n; r++) {
                if (t[r][i] % mod) { p = r; break; }
            }
            if (p == -1) return 0;
            if (p != i) {
                swap(t[p], t[i]);
                ans = (mod - ans) % mod;
            }

            int val = (t[i][i] + mod) % mod; 
            ans = (ans * val % mod);

            int ip = inv(val);
            for (int r = i + 1; r <= n; r++) {
                if (!t[r][i]) continue;
                int fac = (t[r][i] * ip + mod) % mod;
                for (int c = i; c <= n; c++) {
                    t[r][c] = (t[r][c] - fac * t[i][c] % mod + mod) % mod;
                }
            }
        }
        return (ans + mod) % mod;
    }

    pair<bool, Matrix> inverse() const {
        if (n != m) return {false, Matrix()};

        vector<vector<int>> aug(n + 1, vector<int>(2 * n + 1, 0));
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                aug[i][j] = (*this)[i][j] % mod;
            } 
            aug[i][n + i] = 1;
        }

        for (int col = 1, row = 1; col <= n && row <= n; col++, row++) {
            int sel = -1;
            for (int i = row; i <= n; i++) {
                if (aug[i][col] % mod) { sel = i; break; }
            }
            if (sel == -1) return {false, Matrix()};
            if (sel != row) {
                swap(aug[sel], aug[row]);
            }

            int ip = inv((aug[row][col] + mod) % mod);

            for (int j = col; j <= 2 * n; j++) {
                aug[row][j] = ( aug[row][j] * ip ) % mod;
            }
            for (int i = 1; i <= n; i++) {
                if (i == row || !aug[i][col]) continue;
                int fac = (aug[i][col] + mod) % mod;

                for (int j = col; j <= 2 * n; j++) {
                    aug[i][j] = (aug[i][j] - fac * aug[row][j] % mod + mod) % mod;
                }
            }
        }

        Matrix invm(n, n);
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                invm[i][j] = aug[i][n + j];
            }
        }
        return {true, invm};
    }

    // 返回 pair<status, solution>:
    //   status: 0 = 无解, 1 = 唯一解, 2 = 多解
    //   solution: 若有解，返回一个可能的解向量长度为 m（采用 1-based，索引 1..m；自由变量设为 0）
    pair<int, vector<T>> GuessSolve(const vector<T>& b) const {
        assert((int)b.size() == n + 1);
        Matrix<int> a(n + 1, m + 2);
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                a[i][j] = (int)(((*this)[i][j] % mod + mod) % mod);
            }
            a[i][m + 1] = (int)((b[i] % mod + mod) % mod);
        }

        int r = 1;
        vector<int> pos(m + 1, 0);
        for (int c = 1; c <= m && r <= n; c++) {
            int sel = 0;
            for (int i = r; i <= n; i++) {
                if (a[i][c]) { sel = i; break; }
            }

            if (!sel) continue;
            swap(a[sel], a[r]);
            pos[c] = r;
            int ip = inv(a[r][c]);

            for (int j = c; j <= m + 1; j++) a[r][j] = a[r][j] * ip % mod;
            for (int i = 1; i <= n; i++) {
                if (i != r && a[i][c]) {
                    int f = a[i][c];
                    for (int j = c; j <= m + 1; j++) {
                        a[i][j] = (a[i][j] - f * a[r][j] % mod + mod) % mod;
                    }
                }
            }
            r++;
        }
        for (int i = r; i <= n; i++) {
            if (a[i][m + 1]) return {0, {}};
        }
        vector<int> ans(m + 1, 0);
        for (int c = 1; c <= m; c++) {
            if (pos[c]) ans[c] = a[pos[c]][m + 1];
        }
        for (int c = 1; c <= m; c++) {
            if (!pos[c]) return {2, ans};
        }
        return {1, ans};
    }
};
```

### 矩阵快速幂优化 DP

**只要你能把“下一个时刻的每个需要的量”写成当前状态的线性组合，就能造矩阵。形式上，如果存在状态向量：**$$v_i = \begin{bmatrix} s^{(1)}_i \\ s^{(2)}_i \\ \vdots \\ s^{(k)}_i \end{bmatrix}$$
使得：$$v_{i+1} = F\; v_i$$
这是唯一的要求——并不要求方程一开始就只包含 `f[i-1]`、`f[i-2]` 之类。如果出现了$g_i$​ 这样的序列，**只要 $g$ 自己也有线性关系**，就把它一起放进状态向量。

eg:

原式：$$\text{dp}(n)=2^m(2^m-1)^{n-2}-(2^m-1)\text{dp}(n-2)$$把索引统一为 $i$：$$\text{dp}_{i+1} = A\cdot g_i - t\cdot \text{dp}_{i-1}$$其中 $A=2^m,\ t=2^m-1,\ g_i=t^{\,i-1}$. 右边使用到的量是：$\text{dp}_{i-1}$​ 和 $g_i$.​
$$g_{i+1}=t\cdot g_i$$
是线性的，满足条件。

我们可以选
$$v_i = \begin{bmatrix}\text{dp}_i\\ \text{dp}_{i-1}\\ g_i\end{bmatrix}.$$
这是闭合的：下一步 $\text{dp}_{i+1}$​ 用到 $\text{dp}_{i-1}$​ 和 $g_i$​，$\text{dp}_i$​ 下移成第二项，$g_{i+1}=t g_i$​。不能再删任何一项而保持闭合（试删 $g_i$​ 就无法表达右侧的 $g_i$​）。

**写出每一个“下一步量”作为当前状态的线性组合 → 得到矩阵的每一行**

**例子**（按顺序 $[dp_i,\ dp_{i-1},\ g_i]$）：

- $\text{dp}_{i+1}=0\cdot\text{dp}_i + (-t)\cdot\text{dp}_{i-1} + A\cdot g_i$ → 第一行系数 $[0,\ -t,\ A]$。

- $\text{dp}_i = 1\cdot\text{dp}_i + 0\cdot\text{dp}_{i-1} + 0\cdot g_i$​ → 第二行系数 $[1,0,0]$（相当于移位）。

- $g_{i+1} = 0\cdot\text{dp}_i + 0\cdot\text{dp}_{i-1} + t\cdot g_i$ → 第三行系数 $[0,0,t]$。

所以矩阵是：$$F=\begin{bmatrix}0 & -t & A\\[3pt] 1 & 0 & 0\\[3pt] 0 & 0 & t\end{bmatrix}$$

线性递推 `f[i] = a * f[i - 1] + b * f[i - 2] + ...` 也可以这样看：

- 把若干个 `f[i - 1], f[i - 2], ...` 放成一个向量 `V_i`，存在一个固定矩阵 `A`，使得 `V_i = A * V_{i-1}`（这里“×”是普通的数乘加法）。

- 于是 `V_R = A^R * V_0`。
    这就是矩阵快速幂的标准用法。


#### 例题：

```text
有 n 个人, 每个人可以选择是否操作花费 c_i 的费用造成 a_i 的伤害,每回合费用上限为 m, 如果一个人本回合操作了, 下回合对应操作的费用会临时增加 k, 问 T 回合能造成的最大伤害之和. n ≤ 6, T ≤ 10^9
```

可以得到对应的转移方程为

`f[i][j]` 表示进行到第 i 轮时候，使用技能的状态是 j 的最大伤害之和，此处 j 表示一个 6 位的二进制编码，0 表示不用，1 表示用。
$$f[i][j] \ = \ f[i - 1][k] + gain( j \ -> k) $$

考虑二进制优化，把 gain 理解为一个矩阵 $M$.

设状态数 S = 4（n = 2 的情况），我们用下面的矩阵 M 表示 “一步收益”：
（`-INF` 表示不可行的转移）

```
M =
        to:  0    1    2     3
from 0    [ -INF, 5,   2,  -INF ]
     1    [  3,   1,   8,   4   ]
     2    [ -INF, 6,   0,   2   ]
     3    [  7,  -INF, -INF, 3  ]
```

$$(M^2)[0][2] = max \ over \ k ( M[0][k] + M[k][2] )$$

则
```

f[1] = f[0] * M  => f[1] 等于 M 的第 0 行（因为 f[0] 只有第 0 项是 0）

f[2] = f[1] * M  => f[2] = f[0] * (M * M) = f[0] * M^2

```

#### 参考代码：

```C++
template<typename T = int>
struct Matrix : public vector<vector<T>> {
	int n, m;
	Matrix(int _n = 0, int _m = 0): 
     vector<vector<T>>(_n, vector<T>(_m, 0)), n(_n), m(_m) { }

    static Matrix unit(int n) {
        Matrix res(n, n);
        for (int i = 0; i < n; i++) res[i][i] = 1;
        return res;
    }

	Matrix operator+ (const Matrix &B) const {
		assert(n == B.n && m == B.m);
        Matrix res(n, m);
		for (int i = 0; i < n; i++) {
			for (int j = 0; j < m; j++) {
				res[i][j] = (*this)[i][j] + B[i][j];
			}
		}
        return res;
	}

    Matrix operator* (const Matrix &B) const {
        assert(m == B.n);
        Matrix C(n, B.m);
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < m; k++) {
                if ((*this)[i][k].val() == 0) continue;
                for (int j = 0; j < B.m; j++) {
                    C[i][j] += (*this)[i][k] * B[k][j];
                }
            }
        }
        return C;
    }

	Matrix pow(int e) const {
		assert(n == m);
		Matrix base = *this;
		Matrix res = Matrix::unit(n);
		while (e > 0) {
			if (e & 1) res = res * base;
			base = base * base;
			e >>= 1;
		}
		return res;
	}
};

void solve()
{
    int n, m;
    cin >> n >> m;

    Dmint::set_mod(m * 10007);
    Dmint N = 0;
    for (int i = 1; i <= n; i++) {
        int c, l;
        cin >> c >> l;
        Matrix<Dmint> M(2, 2);
        M[0][0] = 10, M[0][1] = c;
        M[1][0] = 0, M[1][1] = 1;
        M = M.pow(l);

        N = M[0][0] * N + M[0][1];
    }

    cout << N.val() / m << endl;
}

```

### 拉普拉斯矩阵（矩阵树）

```C++
Matrix M(n, n);
vector<vector<int>> a(n + 1, vector<int>(n + 1));
for (int i = 1; i <= n; i++) {
	string s;
	cin >> s;
	s = ' ' + s;
	for (int j = 1; j <= n; j++) {
		if (s[j] == '1') a[i][j] = 1;
		else if (s[j] == '0') a[i][j] = 0;
		else a[i][j] = -1;   // 证明有权值 这里是概率
	}
}
vector<int> f(110, 0), d = f;   // 这里是拉格朗日插值法，带入n个点，求出n个坐标
// (x, f[x]),...,
for (int v = 1; v <= n; v++) {
	for (int i = 1; i <= n; i++) d[i] = 0;
	for (int i = 1; i <= n; i++) {
		for (int j = 1; j <= n; j++) {
			int w = a[i][j] >= 0 ? a[i][j] : v;
			d[i] += w;
			M[i][j] = (mod - w) % mod;
		}
	}
	for (int i = 1; i <= n; i++) M[i][i] = d[i];
	M.n = M.m = n-1;
	f[v] = M.det();
	M.n = M.m = n;
}
```

## XOR线性方程组  (Bitset\<int>)

```C++
vector<bitset<N>> M(n * n + 1);
for (int i = 1; i <= n; i++) {
	for (int j = i + 1; j <= n; j++) {
		auto p = getPath(i, j);
		if (p.size() == k + 1) {
			path.push_back({i, j});
			for (auto x : p) {
				M[path.size() - 1].set(x - 1);  // 根节点 0 已知，所以从 1 开始算
			}
		}
	}
}
vector<PII> que;
bool res = 1;
auto getPivot = [&](int n, int m) -> void { // 获取主元，看主元个数是不是 n
	for (int i = 1; i <= n; i++) {  // 题目中的 0 已知，所以直接从 1 开始建立线性方程组
		int p = 0;
		for (int j = i; j <= m; j++) {
			if (M[j][i]) { p = j; break; }
		}
		if (!p) { cout << "NO\n"; res = 0; return; }  // 多解
		if (p != i) swap(M[p], M[i]), swap(path[p], path[i]);
		que.push_back(path[i]);
		for (int j = i + 1; j <= m; j++) {
			if (M[j][i]) M[j] ^= M[i];
		}
	}
};
getPivot(n - 1, path.size() - 1);  // 只有 n - 1 个未知数
if (!res) return;

vector<int> b(n * n + 1);
for (int i = 1; i <= que.size(); i++) cin >> b[i];

int idx = 1;
for (auto [u, v] : que) {
	M[idx].reset();
	auto p = getPath(u, v);
	for (auto x : p) M[idx].set(x - 1);
	idx++;
}
// n - 1 个未知数，m 个方程，RHS 向量是 b
auto Guess = [&](int n, int m, vector<int>& b) -> vector<int> {
	for (int i = 1; i <= n; i++) {
		int p = 0;
		for (int j = i; j <= m; j++) {
			if (M[j][i]) {
				p = j; break;
			}
		}
		if (p > i) swap(M[p], M[i]), swap(b[p], b[i]);
		for (int j = 1; j <= m; j++) {
			if (j == i) continue;
			if (M[j][i]) {
				M[j] ^= M[i], b[j] ^= b[i];
			}
		}
	}
	return b;
};
auto ans = Guess(n - 1, que.size(), b);
for (int i = 1; i < n; i++) cout << ans[i] << " \n"[i == n - 1];

```
