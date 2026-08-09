---
topic: "最大子数组和 plus 版本"
category: "10-dp"
source: "动态规划 DP.md"
---

# 最大子数组和 plus 版本

给你一个数组 $a_1,a_2,…,a_n$ 和两个整数 $m$ 和 $k$ 。
你可以选择某个子数组 $a_l,a_{l+1},…,a_{r−1},a_r$.
子数组 $a_l,a_{l+1},…,a_{r−1},a_r$ 的代价等于  $∑_{i=l}^{r}a_i − k*⌈\frac{r−l+1}{m}⌉$ ，其中 $⌈x⌉$ 表示上取整。

```C++
	int ans = 0;
	for (int x = 1; x <= m; x++) {
		int cur = 0;
		for (int i = x; i <= n; i += m) {
			int res = 0;
			for (int j = i; j <= min(n, i + m - 1); j++) {
				res += a[j];
				ans = max(ans, res + cur - k);
			}
			cur = max(0LL, cur + res - k);  // 表示贪心操作
		}
	}
```
