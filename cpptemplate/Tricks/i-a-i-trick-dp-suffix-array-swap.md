---
topic: "类似于 i + a\\[i]，这样的数组的 trick，交换元素的贡献可以通过前后缀dp处理"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 类似于 i + a\[i]，这样的数组的 trick，交换元素的贡献可以通过前后缀dp处理

```C++
vector<int> pre(n + 1), suf(n + 2);
for (int i = 1; i <= n; i++) {
	if (i & 1) {
		pre[i] = pre[i - 1];
	} else {
		pre[i] = max(pre[i - 1], (a[i] << 1) - i);
	}
}
for (int i = n; i >= 1; i--) {
	if (i & 1) {
		suf[i] = suf[i + 1];
	} else {
		suf[i] = max(suf[i + 1], (a[i] << 1) + i);
	}
}
int Max = 0;
int res = (n % 2 == 0 ? ((n - 1) - 1) : (n - 1));
if (n == 1) {
	cout << a[1] << endl;
	return;
}
for (int i = 1; i <= n; i++) {
	if (i & 1) {
		Max = max({Max, pre[i] - (a[i] * 2 - i), suf[i] - (a[i] * 2 + i)});
	}
}
```

***
