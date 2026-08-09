---
topic: "拉格朗日插值"
category: "05-polynomial"
source: "多项式 Polynomial.md"
---

# 拉格朗日插值

* 根据一个多项式带入多个值可以求出一个查询点的函数值
* 说白了还是函数带入未知数求值的过程，只是这个函数是个多项式，套以下模板就行
$$f(x) = \sum_{i = 1} ^ {n}y_i L_i(x)​$$ $$L_i(x) = \prod_{j\neq i}\frac{x - j}{ i - j}$$
```C++
vector<int> f(n + 1);
f[0] = (1 == n) ? 1 : 0;
for (int i = 1; i <= n - 1; i++) {
	cin >> f[i];
}

// (i, f[i]) 表示点
// n + 1 个点确定一个 n 次多项式
auto Lagrange = [&]() -> Poly {
	if (n == 0) return Poly();
	// 构造 P(x) = prod_{j = 0.. n - 1} (x - j) ，degree = n
	Poly P(1, 1);
	for (int j = 0; j < n; j++) {
		int negj = (mod - j) % mod;
		Poly nxt(P.size() + 1);
		for (int a = 0; a < P.size(); a++) {
			// nxt[a] += P[a] * (-j)
			nxt[a] = (nxt[a] + P[a] * negj) % mod;
			// nxt[a + 1] += P[a] * 1
			nxt[a + 1] = (nxt[a + 1] + P[a]) % mod;
		}
		P.swap(nxt);
	}
	// P 的大小为 n + 1，P[k] 对应 x^k 的系数，P[n] 应为 1
	vector<int> fact(n);
	fact[0] = 1;
	for (int i = 1; i < n; ++i) fact[i] = fact[i - 1] * i % mod;
	Poly L(n);
	for (int i = 0; i < n; ++i) {
		vector<int> Q(n);
		Q[n - 1] = P[n];
		for (int k = n - 1; k >= 1; k--) {
			Q[k - 1] = (P[k] + i * Q[k]) % mod;
		}
		int denom = fact[i] * fact[n - 1 - i] % mod;
		if (((n - 1 - i) & 1) != 0) denom = (mod - denom) % mod;
		int invden = inv(denom);
		int coef = f[i] * invden % mod;
		for (int t = 0; t < n; t++) {
			L[t] = (L[t] + coef * Q[t]) % mod;
		}
	}
	return L;
};

Poly L = Lagrange();

int k;
cin >> k; // 读入 k 求解答案，带入多项式，n 求解
auto Horner = [&](Poly &f, int x) -> int {
	int res = 0;
	for (int i = f.size() - 1; i >= 0; i--) {
		res = (res * x % mod + f[i] % mod) % mod;
	}
	return res % mod;
};
cout << Horner(L, k) << '\n';
```
