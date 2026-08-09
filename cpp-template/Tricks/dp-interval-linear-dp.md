---
topic: "线段树维护“线性 DP”区间状态"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 线段树维护“线性 DP”区间状态

**区间查询**：真正要“从 L 到 R”跑一次 DP 时，只需把 \[L,R] 切分成若干子区间节点，取出它们各自的状态，再按“左 + 右”顺序合并 $O(\log n)$ 次，就等价于一趟线性扫描。

``` text
// 合并 A 段和 B 段（严格 A 在左，B 在右）
Info operator+(Info a, Info b) {
  i64 add = min(a.left, b.need);
  return {
    a.left + b.left - add,    
    a.need + b.need - add,    
    a.ans  + b.ans  + add
  };
}
```

***
