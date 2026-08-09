---
topic: "字符串匹配 KMP"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 字符串匹配 KMP


```C++
for (int i = 1; i <= n; i++) {  // 倒着匹配 nxt 数组
	vector<int> nxt(n + 1, 0);
	nxt[i] = i + 1; int it = i + 1;
	for (int j = i - 1; j >= 1; j--) {
		while (it != i + 1 && a[j] != a[it - 1]) it = nxt[it];
		if (a[j] == a[it - 1]) it--;
		nxt[j] = it;
	}
	for (int j = i; j >= 1; j--) {
		if (nxt[j] == i + 1) f[i] += f[j - 1];  // 无 borad
	}
}
auto build_next = [&](const vector<int> &p, int m) -> vector<int> {
	vector<int> nxt(m + 1);
	nxt[1] = 0; 
	for (int i = 2, j = 0; i <= m; i++) {
		while (j > 0 && p[i] != p[j + 1]) j = nxt[j];
		j += p[i] == p[j + 1];
		nxt[i] = j;
	}
	return nxt;
};
auto kmp = [&](const vector<int>& s, const vector<int>& p) {
	int n = s.size() - 1, m = p.size() - 1;
	auto nxt = build_next(p, m);
	for (int i = 1, j = 0; i <= n; i++) {
		while (j > 0 && s[i] != p[j + 1]) j = nxt[j];
		j += s[i] == p[j + 1];
		if (j == m) {
			cout << "在下标 " << i - m + 1 << " 处找到匹配" << endl;
			j = nxt[j]; 
		}
	}
};
```
