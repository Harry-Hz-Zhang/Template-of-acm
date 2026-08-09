---
topic: "组合数 $C_a^b$"
category: "03-combinatorics"
source: "组合数学  Combinatorics.md"
---

# 组合数 $C_a^b$

### 递推法

* 首先组合数可以通过递归的方式来求解

<!-- image removed -->
以后见到这种类似的转移方式可以往组合数上想

mod 可能不是质数，则不能用费马小定理求解。
```C++
int C[5010][5010];
void init() {
	C[0][0] = 1;
	for (int i = 1; i <= 5000; i++) {
		for (int j = 0; j <= i; j++) {
			if (!j)  C[i][j] = 1;
			else C[i][j] = (C[i - 1][j] + C[i - 1][j - 1]) % mod;
		}
	}
}
```

*  组合数奇偶：
```C++
if(n & k == k) : C(n, k) is odd;
else C(n, k) is even
```

### 逆元 ( 计算 $C_a^b$ $A_a ^b$  )：

$$C_a ^b = \frac {a!}{b!(a - b)!} = a! * b!^{-1} * (a - b)!^{-1}$$
* 当 $p$ 为质数且 $a$ 与 $p$ 互质时，根据费马小定理有 $$a^{p - 1} ≡ 1$$
将其变形可得 $$a * a^{p-2} ≡ 1$$
这里的 $a^{p-2}$ 就可以看作 $a$ 在模 $p$ 下的逆元。

**模板**
```C++
int qpow(int a, int k) {
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
struct Comb {
    int n;
    vector<int> fac, invfac, pow2;
    Comb(): n(0) {}
    Comb(int _n): n(0) { init(_n); }

    void init(int m) {
        if (m <= n) return;
        fac.resize(m + 1);
        invfac.resize(m + 1);
        pow2.resize(m + 1);

        pow2[0] = 1;
        for (int i = 1; i <= m; i++) {
            pow2[i] = (int)(pow2[i - 1] * 2LL) % mod;
        }
        int start = n > 0 ? n + 1 : 1;
        if (n == 0) {
            fac[0] = invfac[0] = 1;
        }
        for (int i = start; i <= m; i++) {
            fac[i] = (int)((i64)fac[i - 1] * i % mod);
        }
        invfac[m] = qpow(fac[m], mod-2);
        for (int i = m; i > (n == 0 ? 1 : n); i--) {
            invfac[i - 1] = (int)((i64)invfac[i] * i % mod);
        }
        n = m;
    }

    // fac[m]
    int F(int m) {
        if (m > n) init(2 * m);
        return fac[m];
    }
    // invfac[m]
    int iF(int m) {
        if (m > n) init(2 * m);
        return invfac[m];
    }
    // inv[m] = m^{-1}
    int inv(int m) {
        return qpow(m, mod - 2);
    }
    // pow(2, n)
    int P2(int m) {
        if (m <= n) return pow2[m];
        return qpow(2, m);
    }
    // A(n, m) = n! / (n - m)!
    int A(int n_, int m_) {
        if (m_ < 0 || m_ > n_) return 0;
        if (n_ > n) init(2 * n_);
        return (int)( (i64)fac[n_] * invfac[n_ - m_] % mod );
    }
    // C(n, m) = n! / (m! * (n - m)!)
    int C(int n_, int m_) {
        if (m_ < 0 || m_ > n_) return 0;
        if (n_ > n) init(2 * n_);
        return (int)((i64)fac[n_] * invfac[m_] % mod * invfac[n_ - m_] % mod );
    }
};
Comb comb(1e6);
```

### Lucas定理

* 适用于mod范围小的时候可能出现类似于整除的现象，就得用Lucas定理递归求解
* 当 $mod = 2$ 时:  $C_a^b$ $mod$ $2$ = $(a$ & $b == a)$

```C++
int qpow(int a, int k) {
    i64 res = 1 % mod;
    while(k) {
        if (k & 1) res = (i64)res * a % mod;
        a = (i64)a * a % mod;
        k >>= 1;
    }
    return res;
}

int C(int a, int b) {
    if (b > a) return 0;
    if (b > a - b) b = a - b;
    int x = 1, y = 1;
    for (int i = 0; i < b; i++) {
        x = x * (a - i) % mod;
        y = y * (i + 1) % mod;
    }
    return x * qpow(y, mod - 2) % mod;
}

int lucas(int a, int b) {
    if (b == 0) return 1;
    return lucas(a / mod, b / mod) * C(a % mod, b % mod) % mod;
}
```

## 容斥原理

* 容斥原理（Inclusion-Exclusion Principle）是一种用于**计算集合中元素个数**的数学方法。它的核心思想是：
- 直接相加各部分的贡献时，会有重复计算的部分。
- 通过减去重复部分，再加回多减的部分，保证计算的准确性。

一个基本例子：
- 设有两个集合 $A$ 和 $B$，我们希望计算它们的并集的大小，即 $∣A∪B∣$。
- 直接相加会导致交集部分 $|A ∩ B|$ 被重复计算：
$$∣A∪B∣=∣A∣+∣B∣−∣A∩B∣$$
* 如果有三个集合 $A,B,C$：
$$∣A∪B∪C∣=∣A∣+∣B∣+∣C∣−∣A∩B∣−∣A∩C∣−∣B∩C∣+∣A∩B∩C∣$$
可以应用在区间DP的加减之中。
## 抽屉原理

* 10本书放入要9个抽屉里，无论怎么样放，至少有一个抽屉里面放不少于两本书。

* **一种应用：**
	当每种元素的出现的次数 $f(x)$ 小于 分成的组数时，则可以保证，分成的若干个数组中每个元素不会重复出现。
	eg：$[1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5 ]$ 中 $f(1) = 4 < ((n / 3) = 6)$，且 $f(2)$ , $f(3)$ , $f(4)$,  $f(5)$ 均满足，则由于抽屉原理，则存在某种划分 $1，2，3，4，5$ 一定不会在一个划分的数组中出现两次。

* **同余，余数相同**

	$|a_u−a_v|$ 可以被 $x$ 整除
