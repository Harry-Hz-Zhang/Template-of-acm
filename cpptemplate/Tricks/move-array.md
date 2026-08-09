---
topic: "移动数组元素至目标状态"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 移动数组元素至目标状态

https://codeforces.com/contest/2096/problem/E

- **拆解逆序对和“下标奇偶”两条维度**，分别用 $\mathrm{inv}$ 和 $\Delta$ 表示。
- **两类操作** 恰好对应“逆序对 −1/−2” 与“Δ ±1/0”，可以线性拆分。
- **最优配比**：先 x=$\Delta$ 次“−1/±1”操作，再 $(\mathrm{inv}-\Delta)/2$ 次“−2/0”操作。
- 当且仅当 $\mathrm{inv}=0$ 且 $\Delta=0$ 时，原串已经「达成目标」，不需任何操作。

***
