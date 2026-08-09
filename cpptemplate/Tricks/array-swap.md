---
topic: "对一个数组，通过两两交换来使得数组有序"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 对一个数组，通过两两交换来使得数组有序

```C++
vector<int> p(n + 1);
iota(p.begin(), p.end(), 0);
sort(p.begin() + 2, p.end() - 1, [&](int i, int j) {
	return a[i] < a[j];
});
auto swap = [&](int i, int j) {
	if (i < j) std::swap(i, j);
	work(x, y, a[x] - a[i]);
	work(i, y, a[i] - a[j]);
	work(j, y, a[j] - a[x]);
};
// *************************************
for (int i = 2; i <= n; i++) {
	while(p[i] != i) {
		swap(p[i], p[p[i]]);
		// std::swap(p[i], p[p[i]]);
	}
}
// *************************************
```
***
