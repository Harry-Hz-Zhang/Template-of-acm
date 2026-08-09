---
topic: "生成函数 求某个子集和的出现次数(Mod = m)"
category: "05-polynomial"
source: "多项式 Polynomial.md"
---

# 生成函数 求某个子集和的出现次数(Mod = m)

```C++
i64 mod = 998244353;
vector<int> mul(vector<int> a, vector<int> b, int len) {
    vector<int> res(len);
    for (int i = 0; i < a.size(); i++) {
        for (int j = 0; j < b.size(); j++) {
            (res[i + j >= len ? i + j - len : i + j] += a[i] * b[j]) %= mod;
        }
    }
    return res;
}
// 多项式的快速幂
vector<int> qpow(vector<int> x, int y, int len) {
    vector<int> res(len);
    res[0] = 1;
    while (y) {
        if (y & 1) res = mul(res, x, len);
        y >>= 1;
        x = mul(x, x, len);
    }
    return res;
}
//严格来讲 应该是 (1 + x^m) 但由于 mod m 就等于 0，所以替换一下
void solve()
{
    int n, m;
    cin >> n >> m;
    vector<int> f(m), g(m);
    g[0] = f[0] = 1;
    for (int i = 0; i < m; i++) {
        vector<int> h(m);
        h[0] = 1;
        h[i]++;
        f = mul(f, h, m);
    }
    f = qpow(f, n / m, m);
    for (int i = 1; i <= n % m; i++) {  // 从1开始是因为不可能存在等于m的余数了
    // 所以从生成函数的角度考虑就是不存在为 0 的所谓的项
        vector<int> h(m);
        h[0] = h[i] = 1;
        g = mul(g, h, m); 
    }
    f = mul(f, g, m);
    cout << (f[0] + mod - 1) % mod << endl;  // 去掉空集的 1
}
```
