---
topic: "通过两两交换来使得数组有序"
category: "15-group"
source: "群论 Group.md"
---

# 通过两两交换来使得数组有序

```C++
vector<int> p(n + 1);
iota(p.begin(), p.end(), 0);
sort(p.begin() + 2, p.end() - 1, [&](int i, int j) {
	return a[i] < a[j];
});
for (int i = 2; i <= n; i++) {
	while(p[i] != i) {
		swap(p[i], p[p[i]]);  // 也交换对应元素 a[i] a[j]
		std::swap(p[i], p[p[i]]);
	}
}
```