---
topic: "水位线（全局偏移）"
category: "10-dp"
source: "动态规划 DP.md"
---

# 水位线（全局偏移）

为避免每步对整张表做平移，用一个哈希表 `cnt` 存储“键 = s−s-s−tag → dp 值”，再用一个变量 `tag` 记录当前的整体偏移，使得真实前缀和总是 `key+tag`。

```C++
ll wel = 0;    // 全局偏移
int tol = 1;   // ∑_s dp[i][s]
for (int i = 1; i <= n; i++) {
	// 分支 A：整体前缀和 + b[i]
	wel -= b[i];
	// 分支 B：聚合到前缀和 == b[i]
	ll key = b[i] + wel;
	int old = 0;
	
	auto it = f.find(key);
	if (it != f.end()) old = it->second;
	
	int add = tol - old;
	// 把所有旧方案（共 tol 条）聚到 s = b[i]
	f[key] = tol;
	// 更新总方案数
	tol = tol + add;
}
```