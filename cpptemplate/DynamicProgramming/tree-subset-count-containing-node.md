---
topic: "关于树上包含 以 u 节点 的子树中的子集个数"
category: "10-dp"
source: "动态规划 DP.md"
---

# 关于树上包含 以 u 节点 的子树中的子集个数

对于 u 的每个孩子可以选择（选 / 不选）

```C++
Y_combinator dfs = [&](auto &&self, int u) -> void {
	if (fa[u]) e[u].erase(ranges::find(e[u], fa[u]));
	for (auto v : e[u]) {
		fa[v] = u;
		self(v);
		f[u] *= (f[v].val() + 1);
	}
};
dfs(in[0]);
```