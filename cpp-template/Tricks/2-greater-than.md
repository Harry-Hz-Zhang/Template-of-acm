---
topic: "对于只有根节点的度数大于 2 的树剖分成若干链条"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 对于只有根节点的度数大于 2 的树剖分成若干链条

```C++
vector<int> dep(n + 1), bel(n + 1);
vector<vector<int>> path(n + 1);
vector<int> stk;

auto dfs = Ycombinator([&](auto self, int u, int fa) -> void {
	stk.push_back(u);
	int K = 0;
	for (auto v : e[u]) {
		if (v == fa) continue;
		K++;
		self(v, u);
	}
	
	if (u != 1 && K == 0 && stk.size() > 1) {
		int id = stk[1];
		for (int i = 0; i < (int)stk.size(); ++i) {
			path[id].push_back(stk[i]);
			bel[stk[i]] = id;
			dep[stk[i]] = i + 1;
		}
	}
	stk.pop_back();  // 使用栈来存储一整条链
});
dfs(1, 0);
```
