---
topic: "字符自动机"
category: "10-dp"
source: "动态规划 DP.md"
---

# 字符自动机

* 找到在某个下标时候下一个某个字母的最小位置
```C++
vector<vector<int>> next(n + 2, vector<int>(150, n + 1));
auto init = [&]() -> void {
	for (int i = n + 1; i >= 1; i--) {
		for (int j = 'a'; j <= 'z'; j++) {
			next[i - 1][j] = next[i][j];
			// debug(next[i][j])
		}
		if (i <= n) next[i - 1][s[i]] = i;
	}
};
init();
```
***
