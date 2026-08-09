---
topic: "关于图上的回文串的拓展"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 关于图上的回文串的拓展

即确定一段之后分别向两端进行bfs，加入到队列当中，不断向两端拓展，因为bfs的单调性，所以一定会保证是最短的距离；

```C++
vector<vector<int>> dis(n + 1, vector<int>(n + 1, INF));
auto bfs = [&](auto bfs) -> void {
	queue<PII> q;
	for (int i = 1; i <= n; i++) {
		if (dis[i][i] > 0) {
			dis[i][i] = 0;
			q.push({i, i});
		}
	}
	for (int i = 1; i <= n; i++) {
		for (auto [v, ch] : e[i]) {
			if (dis[i][v] > 1) {
				dis[i][v] = 1;
				q.push({i, v});
			}
		}
	}
	while(!q.empty()) {
		auto [u, v] = q.front();
		q.pop();
		int d = dis[u][v];
		for (auto [x, ch1] : p[u]) {
			for (auto [y, ch2] : e[v]) {
				if (ch1 == ch2 && d + 2 < dis[x][y]) {
					dis[x][y] = d + 2;
					q.push({x, y});
				}
			}  
		}
	}
};
bfs(bfs);
```

***
