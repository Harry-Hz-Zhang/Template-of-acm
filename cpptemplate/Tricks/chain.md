---
topic: "将一棵大树划分为若干的小的直链，使得划分数量最少"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 将一棵大树划分为若干的小的直链，使得划分数量最少

可以使得其(操作次数)不超过 $k \le \left\lfloor \frac{n}{4} \right\rfloor$

•	问题对象是树（无环、连通），可以以某种方式“在节点做操作把附近一块儿处理掉”或“以节点为中心做破坏/封锁”，从而使得该部分不再参与以后计算。

•	目标是把全树的某些量（检查次数、扫描次数、消耗等）压缩到线性级别，或者要构造保证性质的操作序列（如追捕、覆盖、消除、隔离等游戏/构造题）。

•	要求的操作允许“把一整块隔离/删除/覆盖”，而覆盖后被覆盖的节点不再影响上层决策（关键点）。

```C++
vector<bool> del(n + 1), vis(n + 1);
vector<string> ans;
function<int(int, int)> dfs = [&](int u, int fa) -> int {
	int s = 1;
	for (auto v : e[u]) {
		if (v == fa) continue;
		s += dfs(v, u);
	}
	if (s >= 4) {   // 最后每一块的长度小于等于 3 是直链
		del[u] = 1;
		// debug(u);
		s = 0;
	}
	return s;
};
dfs(1, 0);
```
***
