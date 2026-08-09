---
topic: "二分技巧"
category: "17-basic-knowledge"
source: "Z 基础知识.md"
---

# 二分技巧

`partition_point(first, last, pred)`：返回区间 `[first,last)` 中第一个使 `pred(elem)` 为 `false` 的迭代器。也就是说区间被分成 `true | false` 两段，返回“左段结束”的位置（第一个 false）。
