---
topic: "基础 知识，数论"
category: "01-math-number"
source: "基础数学 + 数论 Math Number.md"
---

# 基础 知识，数论

* 基本不等式 (也许可以通过三分来做？？)

## 二次函数

```C++
struct quad {
    int a, b, c;
    quad() { }
    quad(int a_, int b_, int c_) : a(a_), b(b_), c(c_) { }
    int delta(int a_, int b_, int c_) const {
        return b_ * b_ - 4 * a_ * c_;
    };
    bool operator< (const quad& t) const {
        if (this->a > t.a) return 0;
        if (this-> a == t.a) {
            return (this->b == t.b && this->c < t.c);
        } else {    
            int da = t.a - this->a;
            int db = t.b - this->b;
            int dc = t.c - this->c;
            return delta(da, db, dc) < 0;
        }
    }
    bool operator>(const quad& t) const {
        return t < *this;
    }
};
```

## 求和运算 $\sum$

**常数可以提出求和号外**

$$\sum_{i=1}^n (c \cdot f(i))= c \sum_{i=1}^nf(i)$$

 **对内层变量无关的量，可直接乘上项数**  
 
 $$\sum_{y=1}^n x = x \cdot n \quad $$
 
 $$\sum_{x = 1}^n​\sum_{y = 1}^n​ (x+y)=n\sum_x​x+n\sum_y​y=n⋅n(n+1)/ 2​⋅2=n^2(n+1)$$

**线性性（加法可分）**

$$\sum_{i=1}^n (f(i) + g(i)) = \sum_{i=1}^n f(i) + \sum_{i=1}^n g(i)$$
​
**平方和与交叉项**

$$\Big(\sum_{i=1}^n x_i\Big)^2 = \sum_{i=1}^n x_i^2 + 2\sum_{1\le i<j\le n} x_i x_j $$

用途：把 $\sum_{i<j} x_i x_j$ 用平方和代换；或把 $(\sum_{i<j}(x_i+x_j)^2)$ 展开成平方和+总和的平方

**双重求和交换（改变求和次序）**

$$\sum_{i=1}^n \sum_{j=1}^m f(i,j) = \sum_{j=1}^m \sum_{i=1}^n f(i,j)$$

**对称双和变体（计数出现次数）**

$$\sum_{i<j} a_i^2 + \sum_{i<j} a_j^2 = (n-1)\sum_{i} a_i^2$$

（每个 $(a_k^2)$ 出现 $(n-1)$ 次）

**差的平方与变形（常用于距离/方差类问题）** 

$$\sum_{i<j} (x_i-x_j)^2 = n\sum_i x_i^2 - \Big(\sum_i x_i\Big)^2$$

用途：最小化方差/均值相关问题，或把 pairwise 距离写成平方和形式。

**完全平方/配方（complete the square）**

对二次形式 $(ax^2+bx+c)$，配方找最小点：$(a(x + b/(2a))^2 - b^2/(4a) + c)$。

在涉及 $(x^2+(S-x)^2)$ 类型问题，直接把目标写成关于 $x$ 的二次函数，利用凸性找最优位置（若连续，则取导为 0，否则枚举离散可行点）。

**组合恒等式**

$$\sum_{i} \sum_{j\ne i} 1 = n(n-1) $$

以及 $\sum_{i<j} \binom{?}{?}$ 型等式常用双计数思想。

### 推公式

**二项式定理**

$$(a + b)^n = \sum_{k = 0}^{n}C_n^ka^{n - k}b^{k}$$

**数列求和**

$$\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$$
$$\sum_{k=1}^{n} k^2 = \frac{n(n+1)(2n+1)}{6}$$
$$\sum_{k=1}^{n} k^3  = \left[ \frac{n(n+1)}{2} \right]^2$$
$$\sum_{k=1}^{n} k(k+1) = \frac{n(n+1)(n+2)}{3}$$


## 位运算

*  取某一位的时候（熟练使用 |= ）
```C++
num |= x & (1 << i);
```

* 枚举一个数字的二进制表示下的子集 $O(2^{k})$
```C++
for (int w = v; w; w = (w - 1) & v) //枚举v的子集贡献
```

* 当位移过大时记住`(1LL << n)`

* `__lg(x)` 和 `log2(x)` 返回的以0开始 x 的最高位数.

* 想要从高位1到低位1依次减去时：

```C++
x = x - (1LL << (__lg(x)))
```

* 想要从低位1到高位1依次减去时：
```C++
x -= (x & -x);
```

* 一个数二进制表示下1的个数
```C++
int cnt1 = __popcount(n);
```

* 计算 二进制下 0 的个数
```C++
int32_t countr_zero(uint32_t n) {
    return __builtin_ctz(n);
}
```

* __ builtin_clzll 返回前导零数，64 - 1 - clz 得到最高位索引
```C++
__builtin_clzll(n)
```

* 找到最大的整数 k，使得 (b >> k) >= a
```C++
k = min(k, __lg(b[i] / a[i]));
```
### 镜像配对

在一个以某个位 `h` 为分界（把区间分为左段 L（位 h 为 0）和右段 R（位 h 为 1））的问题里，把左段的数与右段中“按和为常数 $C = 2·t − 1$”反向配对：  对每个被配的 `x`，令  `y = C - x`。这种“把一段反转并与另一段对应位置配”的方式就是镜像配对。

```text
    000
    001
    010
    011
  -------
    100
    101
    110
    111
```
* 性质  — **低 h 位互补**

	对于这对 `(x,y)`，在 **低位上它们的 OR 恰好是全 1**，而它们的 AND 在低位上恰好是 0。
```C++
	int xr = l_ ^ r_;
	int it = 63 - __builtin_clzll(xr);
	int h = r_ >> it << it;   // 分界数
	// [l_, t - 1] AND [t, r_]
```
### 格雷码 Gray

两位之间之变化一个 1
```C++
int gray(int n) { return n ^ (n >> 1); }
```

## 异或 ^

* 拆位！

* 快速计算出一个区间的异或和 (Trie树)

*  **异或操作是加法操作 mod 2 的体现**:
	两数异或 $=$ **相加 %2** $=$ **两数相加之后的和是奇数 / 偶数。**

*  树上异或分割
	分割成几个子树，使得每个子树异或和都相等
	联想到 异或的性质：x ^ x ^ x == x

## 模运算 mod

* 基础运算性质

	* $a^b$ % $p$ $=$ $(a$ % $p)$$^b$ % $p$

	* 满足分配律，结合律，交换律...

	* $a \ mod \ b > b \ mod \ a$     =>   $a < b$

	* $a \ mod \ b + b \ mod \ a = max(a, b)$

* 同余：
	$a$ 和 $b$ 对 $p$ 模同余的条件：$(a-b)$ % $p$ $=$ $0$.   //可结合鸽巢原理（组合数学）

* 本质可以看作是 **a mod b = a - floor(a / b) * b;**

## Max 和 Min 运算

$$max(a, b) = \frac{a + b + |a - b|}{2}$$ $$min(a, b) = \frac{a + b - |a - b|}{2}$$

所以又有

$$\max(a, b) = a + b - \min(a, b)$$

可以在切比雪夫距离的时候进行转化 (?)

## 关于整除

* [1 ~ n] 这个区间内有多少个数字是 x  的倍数：答： `floor(n / x)`

## 向下取整 / 向上取整

* 想到奇数与偶数凑一起后会变小。

* 向下取整本质

* $\lceil x + y \rceil = x + \lceil y \rceil$

## 关于平方

* 不止平方，一些构造题目要保证数字平方之后单位数字不能进位，那这种情况一般就只有 $1 * 3$， $3 * 3$... 这样的操作。

## 关于中位数

* 涉及到中位数的题目，基本都是二分的思路，直接二分中位数，然后再想方法验证。
* 也有可能是贪心分块，前缀和等于 0 的点就是中位数
```C++
auto check = [&](int mid) -> bool {
    int cnt = 0;
    int m;  // 删去对应元素后的新数组的长度 n - ?k;
    for (int i = 1; i <= m; i++) {
        if (a[i] >= mid) {
            cnt++;
        }
    }
    return (cnt >= m - (m + 1) / 2 + 1);  // 满足这个条件可为中位数
};

i64 l = -INF, r = INF;
while(l < r) {
    int mid = l + r + 1 >> 1;
    if (check(mid)) l = mid;
    else r = mid - 1;
}
cout << l << endl;
```

## 裴蜀定理

对于任意整数 $u,v$ 方程
$$u\,s + v\,t = x$$
有整数解 $(s,t)$ 的充要条件是
$$\gcd(u,v)\;\bigm|x$$
即 $x$ 是 $gcd(u, v)$ 的倍数


## $GCD$ & $LCM$

1. 求最大公约数与最小公倍数：
```C++
int gcd(int a, int b) { return b ? gcd(b, a % b) : a; }
int lcm(int a, int b) { return a / gcd(a, b) * b; }
```

```C++
struct GMath {
    static const int MAXG = 5010;
    static uint16_t Tbl[MAXG + 1][MAXG + 1];
    // 自动构造器在程序启动时运行一次，填充表
    struct Init {
        Init() {
            for (int i = 0; i <= MAXG; i++) {
                for (int j = i; j <= MAXG; j++) {
                    if (i == 0) Tbl[i][j] = (uint16_t)j;
                    else Tbl[i][j] = Tbl[j % i][i];
                    Tbl[j][i] = Tbl[i][j];
                }
            }
        }
    };
    static Init _init_instance; // 定义在类外
    static inline int gcd_impl(int a, int b) {
        a = llabs(a), b = llabs(b);
        if (!a) return b;
        if (!b) return a;
        if (a <= MAXG) return Tbl[a][b % a];
        if (b <= MAXG) return Tbl[b][a % b];
        return std::gcd(a, b);
    }
    static inline int lcm_impl(int a, int b) {
        if (!a || !b) return 0;
        int g = gcd_impl(a,b);
        int t = a / g * b;
        if (t > LLONG_MAX) return -1;
        return t;
    }
};
uint16_t GMath::Tbl[GMath::MAXG + 1][GMath::MAXG + 1];
GMath::Init GMath::_init_instance;
inline int gcd(int a, int b) { return GMath::gcd_impl(a, b); }
inline int lcm(int a, int b) { return GMath::lcm_impl(a, b); }
```

* **一个序列的任何 子序列的 LCM 都是 整个序列LCM 的因数**

* **一种重要的理解(结合裴蜀定理)：
*
	a和b的最大公约数 = ax 和 by，随意给定整数x，y，所能得到的最小的正整数的差值
	  (+ ?a + ?b == + ?gcd(a, b) )

2. 辗转相除法的过程暨裴蜀定理的证明：
	* 裴蜀定理：**如果a和b是不全为0的整数，则有整数x, y，使得 $ax + by = gcd(a, b)$
	* 辗转相除法：
		<!-- image removed -->

3. 常见性质积累
	* $gcd(a, b) = gcd(a, b - a)$
	* $gcd(a, 0) = |a|$
	* $gcd(a, b) = 1  ⇐⇒  a b$ $互质$
	* 任何正整数都可以分解为素数（质因子）的幂积
		：$$y=p_1^{e_1}​​×p_2^{e_2}​​×⋯×p_k^{e_k}​​.$$
		如果有两个数：$$u=∏p_i^{α_i}​​,v=∏p_i^{β_i}​​,$$
		那么：$$lcm(u,v)=∏p_i^{max(α_i​,β_i​)​}$$


	* 一道例题及结论的推导：
		对于  $gcd( lcm(a_1,a_2),lcm(a_1,a_3)…lcm(a_1,a_n) )$  这个式子，由于每一项内都含有公因子 $a_1$ ，则可以把公因子提出得到：

	     $lcm(a_1, gcd(a_2,a_3...a_n))$ ;

		也就是求解一个后缀最大公因数，与首元素的最小公倍数。

	* *一道例题及结论的推导：
		定义 f(i) 为最小的不能被 i 整除的正整数：
		对于 f(i) = x，我们分析一下会发现，因为 x 是最小的不能被 i 整除的最小正数，就说明其实 i 能整除 1 到 x - 1中的任何一个，也就是能整除lcm(1, 2, ……, x-1), 但是绝对不能整除 x，也就是说不能整除lcm(1, 2, ……, x)。*

	* $x = lcm(a, b)$ <==> 保证 $a$ 和 $b$ 是 $x$ 的次大以及最大的因数。


## 扩展欧几里得

```C++
class exgcd {
public:
    // 求方程 ax + by = c 的一组特解
    // 返回 {x的特解, y的特解, gcd(a, b), 成功标记 f(1有解/0无解)}
    static array<i128, 4> get(int a, int b, int c) {
        array<i128, 4> ans = {1, 0, 0, 1};
        auto &[x, y, g, f] = ans;
        auto dfs = [&](auto self, int a, int b) -> void {
            if (b == 0) { 
                g = a; 
                return; 
            }
            self(self, b, a % b);
            ans = {ans[1], ans[0] - (a / b) * ans[1], g, ans[3]};
        };
        dfs(dfs, a, b);
        if (g < 0) {
            g = -g;
            x = -x;
            y = -y;
        }
        if (c % g) {
            f = 0; // 无解
        } else {
            x *= c / g;
            y *= c / g;
        }
        return ans;
    }
    // 求方程 ax + by = c 中，x 的最小非负整数解
    // 返回值：{x的最小非负解, x的递增步长(即 b / gcd)}，若无解返回 {-1, -1}
    static array<i128, 2> minx(int a, int b, int c) {
        auto [x, y, g, f] = get(a, b, c);
        if (!f) return {-1, -1};  // 无解
        if (!c) return {0, b / g};  // c 为 0 的特判
        auto bg = b / g;
        if (bg < 0) bg = -bg;
        auto k = -x / bg;
        while (x + k * bg < 0) k++;
        while (x + (k - 1) * bg >= 0) k--; 
        return {x + k * bg, bg};
    }
};
```

## 类欧几里得 (FLoor_sum)

```C++
// 计算区间 [0, n - 1] 内所有 i 的 floor((a*i + b) / m) 之和
u64 floor_sum_unsigned(u64 n, u64 m, u64 a, u64 b) {
    u64 ans = 0;
    while (1) {
        if (a >= m) {
            ans += n * (n - 1) / 2LL * (a / m);
            a %= m;
        }
        if (b >= m) {
            ans += n * (b / m);
            b %= m;
        }
        u64 y_max = a * n + b;
        if (y_max < m) break;
        n = (u64)(y_max / m); b = (u64)(y_max % m);
        std::swap(m, a);
    }
    return ans;
}
i64 floor_sum(i64 n, i64 m, i64 a, i64 b) {
    assert(0 <= n && n < (1LL << 32));
    assert(1 <= m && m < (1LL << 32));
    u64 ans = 0;
    if (a < 0) {
        u64 a2 = (a + m) % m;
        ans -= 1ULL * n * (n - 1) / 2 * ((a2 - a) / m);
        a = a2;
    } if (b < 0) {
        u64 b2 = (b + m) % m;
        ans -= 1ULL * n * ((b2 - b) / m);
        b = b2;
    }
    return ans + floor_sum_unsigned(n, m, a, b);
}
```


## 质数 素数（Prime number）

* 2 是质数，而且是唯一的为偶数的质数

* **一个大于等于 4 的偶数，总能拆成两个质数和。**

* 性质：
	* 质数大于1.
	* 两个互质的数最大凑不出来的数是   $a*b-a-b$ .
	* 如果 $a c$ 互质，$b c$ 互质， 则 $a * b$ 与 $c$ 也互质.
	* 整数唯一分解定理 ：

		* *任何大于等于1的正整数n都可以**唯一**分解为有限个**质数**的乘积*

	* 质数乘质数不一定是质数
	* 如果一个乘积是质数，那么它一定是由一个单一的质数和若干个1相乘得来的。
	* 想要使得若干个数字 [1 ~ n] 与某个数字不互质，则该数字应该为这n个数字中质数的乘积。

### 分解质因数

```C++
vector<pii> divide(int x) {
	vector<pii> res;
	for (int i = 2; i * i <= x; i++) {
		if (x % i == 0) {
			int s = 0;
			while(x % i == 0) x /= i, s++;
			res.emplace_back(pii(i, s));
		}
	}
	if (x > 1) res.emplace_back(pii(x, 1));
	return res;
}
// ==================================
   /* 通过欧拉筛高效率求解质因数的个数 */
// ==================================
int calc(int x) {
	if (x == 1) return 0;
	int res = 0;
	for (int i = 0; i < primes.size(); i++) {
		if (primes[i] > sqrt(x)) break;
		while (x % primes[i] == 0) {
			res ++;
			x /= primes[i];
		}
	}
	if (x > 1) res++;
	return res;
}

int calc(int x) {
    int res = 0;
    while (x > 1) {
        int p = minp[x];
        while (x % p == 0) {
            x /= p;
            res++;
        }
    }
    return res;
}

```

#### 不同质因子个数 $\omega(n)$

**最大值**：要想让 $\omega(n)$ 最大，就从最小质数开始连乘：

 $2\cdot3\cdot5\cdot7\cdot11\cdot13\cdot17\cdot19=223\,092$。

$\max_{n\le10^9}\omega(n)=8$

## int 范围内判质数

时间复杂度：log(n)

```C++
constexpr int64_t safe_mod(int64_t x, int64_t m = mod) {
    x %= m;
    if (x < 0) x += m;
    return x;
}
constexpr int64_t pow_mod(int64_t x, int64_t n, const int m = mod) {
    if (m == 1) return 0;
    const uint32_t _m = uint32_t(m);
    uint64_t r = 1;
    uint64_t y = safe_mod(x, m);
    while (n) {
        if (n & 1) r = (r * y) % _m;
        y = (y * y) % _m;
        n >>= 1LL;
    }
    return r;
}
// Miller–Rabin 判质数
constexpr bool is_prime_constexpr(int n) {
    if (n <= 1) return 0;
    if (n == 2 || n == 7 || n == 61) return 1;
    if (n % 2 == 0) return 0;
    int64_t d = n - 1;
    while (d % 2 == 0) d /= 2LL;
    constexpr int64_t bases[3] = {2, 7, 61};
    for (int64_t a : bases) {
        int64_t t = d;
        int64_t y = pow_mod(a, t, n);
        while (t != n - 1 && y != 1 && y != n - 1) {
            y = y * y % n;
            t <<= 1;
        }
        if (y != n - 1 && t % 2 == 0) {
            return 0;
        }
    }
    return 1;
}
```
## 欧拉筛

```C++
static constexpr int MAX_N = 1e7;
std::vector<int> minp, primes;
void sieve(int n) {
    minp.assign(n + 1, 0);
    primes.clear();
    for (int i = 2; i <= n; i++) {
        if (minp[i] == 0) {
            minp[i] = i;
            primes.push_back(i);
        }
        for (auto p : primes) {
            if (i * p > n) {
                break;
            }
            minp[i * p] = p;
            if (p == minp[i]) {
                break;
            }
        }
    }
}
bool is_prime(int n) {
    return minp[n] == n;
}
```

## 埃式筛求 omega

```C++
vector<int> sieveOmega(int n) {
    vector<int> w(n + 1, 0);       // 存放 ω(i)
    vector<bool> isp(n + 1, 1);
    isp[0] = isp[1] = false;
    for (int p = 2; p <= n; ++p) {
        if (isp[p]) {
            // p 是质数，给所有 p 的倍数加 1
            for (int mul = p; mul <= n; mul += p) {
                w[mul]++;
                isp[mul] = (mul == p);
            }
        }
    }
    return w;
}
vector<int> w;
```

### 互质构造：

1. 所有的质数一定都在 $6 * n + 1$ 和 $6 * n - 1$ 这两列
2. 相邻的两个数字互质
3. 相邻的两个奇数互质

## 约数 因数（Divisor）

1. 性质：
	* **重要性质：一个数 x 的约数都是成对存在的 (以sqrt(x)为分界线)**

	* **对于两个数 $x，y$，如果 $x$ mod $m≡ y$ mod $m$，则有 $(y − x)$ ≡ $0$ (mod $m$)，则 $m$ 是 $(y - x)$ 的因数。**
		然后可联系gcd相关知识

	* 由质因数分解定理：任何一个大于2的正整数都可以被分解为质数的乘积。
	* 每个正约数 $i$ 在 $1$ ~ $n$  中出现的次数为 $\lfloor \frac{x}{i} \rfloor$ .

### 约数个数 τ(n)

在 $n\le10^6$  范围内，已知 $\max_{n\le10^6} \tau(n) = 240$，也就是说最多最多不会超过 240 个约数，平均下来实际上可能只有 $\ln10^6\approx14$ 个约数。

在 \[1, $2 \dot \ 10^5$] 范围内，最大的约数数目 $\tau_{\max}=160$（发生在 166320）.

注意类似于 997920 或者 831600 等高度合数。

$\max_{n\le10^9}\tau(n)=1344$，而这个数字就是 n = 735134400。

**枚举约数不是严格的 nlogn ，一些高约数数字可能有很多很多约数，枚举约数是一件很危险的事**

但是 $10^6$ 以内还是可以做到的。

### 求约数个数
```C++
int get_factor(int n) {
	int res = 0;
	for (int i = 1; i <= sqrt(n); i++)
		if (n % i == 0) res++;
	if (sqrt(n) == ceil(sqrt(n))) return res * 2 - 1;
	return res * 2;
}
```
### 因数筛 $O(n * logn)$

```C++
void init() { //预先处理因子
    for(int i=1;i<=MAXN*10;i++) {
        for(int j=i;j<=MAXN*10;j+=i) {
            p[j].push_back(i);
        }
    } 
}
```
## 数论分块

```C++
int division_block(int n) {
	int res = 0;
	for (int l = 1, r; l <= n; l = r + 1) {
		r = n / (n / l);
		res += n / l * (r - l + 1);
	}
	return res;
}
```

## 关于一种位运算所构成的数列规律

```C++
for (int i = 1; i <= n; i++) {
	cout << __lg(i & -i) + 1 << " ";
}
```

* 解释一下这里的位运算
	* `__lg(x)` 是取x二进制表示下最高位的1在哪一位，
	* `lowbit(x) = x & -x` 表示x的最低位的1在哪一位
* 这个数列的奇数位（1，3，5...） 都是 1，因为奇数最低位1都在最后一位。
* 所有 $2^k$ 形式的数，输出都是 k + 1（eg：1 2 4 8 16）。
* 模式是周期性的按照 $2^k$ 递增。
*
```
1  2  1  3  1  2  1  4  1  2  1  3  1  2  1  5  1  2  1  3  1  2  1  4 ...
```
