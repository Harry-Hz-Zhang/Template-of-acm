---
topic: "字符串 Hash"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 字符串 Hash

### 滚动哈希（Rolling Hash）

* 把长度为 $n$ 的位串（从上到下）写成 $b_0,b_1,\dots,b_{n-1}$​，定义多项式滚动哈希为
$$H = b_0\cdot P^{\,n-1} + b_1\cdot P^{\,n-2} + \cdots + b_{n-1}\cdot P^{0}.$$
把每一位按**位置权重**乘上不同的幂再相加。

所以对于前缀 $[1, \ i]$
$$H_i = H_{i - 1} \cdot P + b_i, \ \ H_0 = 0$$对于某区间 $[l, \ r]$
$$H_{l, r} = H_r - H_{l - 1} \cdot P^{r - l + 1}$$

若**只改变第 i 位**，把它从 $old$ 变为 $new$。其它所有位 $b_k$​（$k\neq i$）都不变，于是新的哈希

$$H' = b_0\cdot P^{n-1}+\cdots + b_{i-1}\cdot P^{n-i} + \underbrace{new\cdot P^{n-1-i}}_{\text{只有这一项变了}} + b_{i+1}\cdot P^{n-2-i}+\cdots + b_{n-1}\cdot P^0. $$

把 $H$ 与 $H'$ 比较，只有第 $i$ 项不同，所以

$$H' = H - old\cdot P^{n-1-i} + new\cdot P^{n-1-i} = H + (new - old)\cdot P^{n-1-i}.$$

如果在模 $M$ 下计算，就写成

$$H' \equiv \big(H + (new-old)\cdot P^{\,n-1-i}\big)\bmod M$$

```C++
using u64 = uint64_t;
using u32 = uint32_t;
using uch = unsigned char;
using puu = pair<u64, u32>;
struct double_hash {
  public:
    vector<u64> H1, P1;
    vector<u32> H2, P2;
    static constexpr u64 B1 = 911382497ULL;
    static constexpr u32 B2 = 3571428577UL;
    u64 base1; u32 base2;
    vector<u64> elems;
    int n;
    double_hash() : base1(B1), base2(B2), n(0) { }
    double_hash(const vector<u64> &a) {
        elems = a;
        n = static_cast<int>(elems.size());
        base1 = B1; 
        base2 = B2; 
        H1.assign(n + 1, 0); 
        H2.assign(n + 1, 0);
        P1.assign(n + 1, 1); 
        P2.assign(n + 1, 1);
        for (int i = 0; i < n; i++) {
            H1[i + 1] = H1[i] * base1 + elems[i];
            H2[i + 1] = (u32)((u64)H2[i] * base2 + (u32)elems[i]);
            P1[i + 1] = P1[i] * base1;
            P2[i + 1] = (u32)((u64)P2[i] * base2);
        }
    }
    double_hash(const string &s) {
        vector<u64> a(s.size());
        for (size_t i = 0; i < s.size(); i++) a[i] = (u64)(unsigned char)s[i];
        *this = double_hash(a);
    }
    double_hash(const vector<int> &v) {
        vector<u64> a(v.size());
        for (size_t i = 0; i < v.size(); i++) a[i] = (u64)v[i];
        *this = double_hash(a);
    }
    // 取得区间哈希 [l..r]（0-based 包含端点）
    puu get(int l, int r) const {
        int len = r - l + 1;
        u64 x1 = H1[r + 1] - H1[l] * P1[len];
        u64 tmp2 = (u64)H2[r + 1] - (u64)H2[l] * P2[len];
        return { x1, (u32)tmp2 };
    }
    // 拼接两个哈希（左 + 右），lenRight 为右边子串长度
    puu combine_hashes(const puu &L, const puu &R, int lenRight) const {
        u64 c1 = L.first * P1[lenRight] + R.first;
        u32 c2 = (u32)((u64)L.second * P2[lenRight] + R.second);
        return { c1, c2 };
    }

    // O(1) 计算：把 p 位置改为 nv 后的整个串哈希（不修改对象）
    // 公式：H' = H + (new - old) * P^{n - 1 - p}
    puu hash_after_change(int p, u64 nv) const {
        if (p < 0 || p >= n) return get(0, n - 1);
        puu os = get(p, p);
        puu full = get(0, n - 1);
        auto [o1, o2] = os;
        u64 d1 = nv - o1;
        u64 newH1 = full.first + d1 * P1[n - 1 - p];
        u32 d2 = (u32)((u32)nv - o2);
        u32 newH2 = (u32)((u64)full.second + (u64)d2 * P2[n - 1 - p]);
        return { newH1, newH2 };
    }
    puu hash_after_change(int p, int nv) const { return hash_after_change(p, (u64)nv); }
    puu hash_after_change(int p, unsigned char ch) const { return hash_after_change(p, (u64)ch); }
    void apply_change(int p, u64 nv) {
        if (p < 0 || p >= n) return;
        if (elems[p] == nv) return;
        elems[p] = nv;
        for (int i = p; i < n; i++) {
            H1[i + 1] = H1[i] * base1 + elems[i];
            H2[i + 1] = (u32)((u64)H2[i] * base2 + (u32)elems[i]);
        }
    }
    void apply_change(int p, int nv) { apply_change(p, (u64)nv); }
    void apply_change(int p, unsigned char ch) { apply_change(p, (u64)ch); }

    // 返回整串哈希（方便调用）
    puu Hash() const {
        if (n == 0) return { 0, 0 };
        return get(0, n - 1);
    }
};
```


### 状态哈希 （zobrist_hash）


```cpp
using u64 = uint64_t;  
using u32 = uint32_t;  
using uch = unsigned char;  
using puu = pair<u64, u32>;  
struct zobrist_hash {  
    int sz;  // 字符集大小  
    int k;   // 模数  
    vector<u64> val;  
    vector<int> cnt;   
    u64 cur;   
  
    zobrist_hash(int _sz, int _k) : sz(_sz), k(_k), cur(0) {  
        cnt.assign(sz, 0);  
        val.resize(sz);  
        mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());  
        for (int i = 0; i < sz; i++) {  
            val[i] = rng();  
        }  
    }  
    u64 add(int c) {  
        cnt[c] = (cnt[c] + 1) % k;  
        if (cnt[c] == 0) {  
            cur -= (u64)(k - 1) * val[c];  
        } else {  
            cur += val[c];  
        }  
        return cur;  
    }  
    u64 get() const {  
        return cur;  
    }  
};
```
