---
topic: "LCS"
category: "10-dp"
source: "动态规划 DP.md"
---

# LCS

```C++
void LCS() {
	string a, b;
	cin >> a >> b;
	int n = a.size(), m = b.size();
	a = ' ' + a, b = ' ' + b;
	vector<vector<int>> f(n + 1, vector<int>(m + 1, 0));
	for (int i = 1; i <= n; i++) {
		for (int j = 1; j <= m; j++) {
			f[i][j] = max(f[i - 1][j], f[i][j - 1]);
			if (a[i] == b[j]) {
				f[i][j] = max(f[i][j], f[i - 1][j - 1] + 1);
			}
		}
	}
	
	int i = n, j = m, org = f[n][m] + 1;
	vector<char> ans(org);
	while(i && j) {
		if (a[i] == b[j]) {
			ans[f[i][j]] = a[i];
			i--, j--;
		} else {
			if (f[i][j] == f[i - 1][j]) i--;
			else if (f[i][j] == f[i][j - 1]) j--;
		}
	}
	
	for (int i = 1; i <= f[n][m]; i++) {
		cout << ans[i];
	}
}
```
***
