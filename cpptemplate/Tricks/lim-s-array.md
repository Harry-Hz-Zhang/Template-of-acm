---
topic: "统计所有“仅包含元素 ≤ lim”的子数组中，子数组和恰好等于 `s` 的个数"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 统计所有“仅包含元素 ≤ lim”的子数组中，子数组和恰好等于 `s` 的个数

```C++
for (int i = 1; i <= n; i++) cin >> a[i], pre[i] = pre[i - 1] + a[i];

auto get = [&](int lim) -> int {
	map<int, int> cnt;
	cnt[0] = 1;
	int res = 0;
	for (int i = 1; i <= n; i++) {
		if (a[i] > lim) {
			cnt.clear();
			cnt[pre[i]] = 1;
			continue;
		}
		int tar = pre[i] - s;
		if (cnt.count(tar)) {
			res += cnt[tar];
		}
		cnt[pre[i]]++;
	}
	return res;
};

```

***
