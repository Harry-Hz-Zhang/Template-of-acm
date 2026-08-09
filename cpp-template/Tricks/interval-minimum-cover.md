---
topic: "带有权值的与长度限制的区间最小覆盖问题"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 带有权值的与长度限制的区间最小覆盖问题

序列 a\[1..n] 是一列「需求」（每个位置有一个强度/权值）；你有若干种「资源/代理」(p,s)，表示该代理能在一天内覆盖任意连续长度 ≤ s 的段落，但前提是段内最大需求 ≤ p。目标用最少天数把整个序列从左到右覆盖（每天只能选一个代理）。

- **归一化/预处理代理能力**：对于每个长度 s，只需关心该长度能达到的**最大 p**。令 `mp[s] = max p`（若无则 0），再做从右向左的前缀最大：`mp[i]=max(mp[i], mp[i+1])`，表示 “至少长度为 i 的英雄中，能达到的最大力量”。

- **按天贪心 + 二分扩展**：从当前未覆盖位置 i 出发，想找到最大长度 L $(1 \le L \le n-i+1$）使得 `mp[L] >= max(a[i..i + L - 1])`。可以用二分在长度上搜索（因为长度越大，mp\[L] 单调不增或不增不定，但我们仍可二分求最大满足条件的 L，检查函数用 RMQ）。每次取最大的 L，`i += L`，天数 ++。若 `mp[1] < a[i]` 则不可能。

```C++
int n, m;
cin >> n;
vector<int> a(n + 1);
for (int i = 1; i <= n; i++) cin >> a[i];

cin >> m;
vector<int> p(m + 1), s(m + 1), mp(n + 1);
for (int i = 1; i <= m; i++) {
	cin >> p[i] >> s[i];
	mp[s[i]] = max(mp[s[i]], p[i]);
}
for (int i = n - 1; i >= 1; i--) mp[i] = max(mp[i], mp[i + 1]);
int ans = 0;
for (int i = 1; i <= n; ) {
	if (mp[1] < a[i]) {
		cout << -1 << endl;
		return;
	}
	int Max = 0;
	int j = 0;
	for (; j + i <= n; j++) {
		Max = max(Max, a[i + j]);
		if (mp[j + 1] < Max) break;
	}
	i += j;
	ans++;
}
cout << ans << endl;
```

***
