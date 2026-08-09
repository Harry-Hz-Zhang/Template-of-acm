---
topic: "区间 \\[0,X] 中二进制中第 k 位为 1 的数的个数"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 区间 \[0,X] 中二进制中第 k 位为 1 的数的个数

那么区间 $[l,r]$ 中第 $k$ 位为 $1$ 的数目为：$$\text{count}_1 = \text{count}(k, r) - \text{count}(k, l - 1)$$
```C++
int count(int k,int X){
    return (X + 1) / (1 << k + 1) * (1 << k)
        + max(0LL, (X + 1) % (1 << k + 1) - (1 << k));
}
```

***
