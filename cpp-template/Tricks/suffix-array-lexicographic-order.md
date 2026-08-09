---
topic: "处理从某个下标开始的所有数组的最小后缀字典序"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 处理从某个下标开始的所有数组的最小后缀字典序

```C++
	vector<vector<int>> a(n + 1, vector<int>(1));
	int l = 0;
	for (int i = 1; i <= n; i++) {
		int k;
		cin >> k;
		l = max(l, k);
		while (k--) {
			int x;
			cin >> x;
			a[i].push_back(x);
		}
	}
  
	vector<vector<int>> len(l + 1);
	for (int i = 1; i <= n; i++) {
		int m = a[i].size() - 1;
		len[m].push_back(i);
	}
	vector<int> rank(n + 1); // 排名，
	vector<int> f(l + 1);
	vector<int> S; // 
	for (int i = l; i >= 1; i--) {
		for (auto x : len[i]) {
			S.push_back(x);
		}
  
		sort(S.begin(), S.end(), [&](int x, int y) {
			if (a[x][i] != a[y][i]) return a[x][i] < a[y][i]; // DP想法
			return rank[x] < rank[y];
		});
		
		// 若本位相等，则比较之前的
		f[i] = S.front();
		for (int j = 0; j < S.size(); j++) {
			rank[S[j]] = j + 1;
		}
		// 每一次rank都要更新一下

	}
```


***
