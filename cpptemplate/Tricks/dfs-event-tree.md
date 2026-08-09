---
topic: "事件树 + DFS 回溯（模拟“时间旅行”）"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 事件树 + DFS 回溯（模拟“时间旅行”）

题目允许“回溯到第 x 天”，相当于在时间轴上做分支，之后的操作又从那条分支继续

**优点**：不用持久化数据结构，也无需重置全局数组——只靠「压栈」「备份—修改—还原」就能探索所有时间分支，时间复杂度 $O((n+m+\sum k)\log n)$

```C++
for (int i = 1; i <= m; i++) {   // 建时序树
	int op, x = 0, y = 0, k;
	cin >> op;
	if (op == 1 || op == 2) {
		cin >> x >> y;
		e[i - 1].push_back({op, x, y, i});
	} else if (op == 3) {
		cin >> x;
		e[x].push_back({op, x, y, i});
	} else {
		st[i] = 1;
		cin >> k;
		while (k--) {
			cin >> x;
			angry[i].push_back(x);
		}
		e[i - 1].push_back({op, x, y, i});
	}
}

vector<int> res(m + 1, -1);
function<void(int)> dfs = [&](int u) -> void {
	if (st[u] == 1) {
		Info merge;
		int l = 1, r;
		for (auto pos : angry[u]) {
			r = pos - 1;
			merge = merge + seg.rangeQuery(l, r);
			merge.left += a[pos].left;
			merge.ans += (merge.left + 1) / 2;
			merge.left /= 2;
			l = pos + 1;
		}
		merge = merge + seg.rangeQuery(l, n);
		res[u] = merge.ans;
	} 
	for (auto &[op, x, y, v] : e[u]) {
		Info pre;
		if (op <= 2) {
			pre = a[x];
			if (op == 1) a[x].left = y;
			else a[x].need = y;
			seg.modify(x, a[x].init());
		}
		dfs(v);
		if (op <= 2) {
			a[x] = pre;
			seg.modify(x, a[x].init());
		}
	}
};

dfs(0);
```

***
