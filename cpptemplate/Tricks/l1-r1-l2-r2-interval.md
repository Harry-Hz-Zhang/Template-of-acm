---
topic: "保证区间 \\[l1, r1] \\[l2, r2] 区间端点是重叠的"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 保证区间 \[l1, r1] \[l2, r2] 区间端点是重叠的

```C++
// 首先总长度 -1
m--;
vector<range> ranges(n + 1);
for (int i = 1; i <= n; i++) {
	ranges[i].read();
	ranges[i].r--;  // 所有的右端点都 -1
}
sort(ranges.begin() + 1, ranges.end());
LazySegmentTree<Info, Tag> seg(m);

seg.rangeApply(ranges[1].l, ranges[1].r, {1});
int ans = INF;
for (int i = 1, j = 2; i <= n; i++) {
	while (j <= n && seg.rangeQuery(1, m).Min == 0) {
		seg.rangeApply(ranges[j].l, ranges[j].r, {1});
		++j;
	}
	if (seg.rangeQuery(1, m).Min >= 1) ans = min(ans, ranges[j-1].w - ranges[i].w);
	auto [l, r, w] = ranges[i];
	seg.rangeApply(l, r, {-1});
}
```

**将原来的闭区间 `[l, r]` 转化成半开区间 `[l, r)`（即把所有右端点 `r` 都做 `r–1`），可以让“端点重叠”时也被当作真正的重叠来处理，从而统一加减操作，避免对 `r1==l2` 的特例判断。**

***
