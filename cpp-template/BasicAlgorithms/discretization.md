---
topic: "离散化"
category: "02-basic"
source: "基础算法 Basic.md"
---

# 离散化

[0,maxVal]

```C++
sort(alls.begin(), alls.end());
alls.erase(unique(alls.begin(), alls.end()), alls.end());
auto find = [&](int x) -> int {
	return lower_bound(alls.begin(), alls.end(), x) - alls.begin();
};
```
