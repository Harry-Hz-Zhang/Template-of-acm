---
topic: "KMP"
category: "11-string"
source: "字符串 String.md"
---

# KMP
* $next[i]$ 表示在模板串 $p[]$ 中，以 $p[i]$ 结尾的后缀，能够匹配最长的前缀的最大长度(最大下标)

```C++
vector<int> prefix(const string &p) {
	int m = p.size();
	vector<int> next(m, 0);
	for (int i = 1, j = 0; i < m; i++) {
		while(j > 0 && p[i] != p[j]) j = next[j - 1];
		if (p[i] == p[j]) j++;
		next[i] = j;
	}
	return next;
}

vector<int> KMP(const string &t, const string &p) {
	int n = t.size(), m = p.size();
	if (m == 0) return { };

	auto next = prefix(p);
	vector<int> matches;
	matches.reserve(n / (m > 0 ? m : 1) + 5);
	for (int i = 0, j = 0; i < n; i++) {
		while(j > 0 && t[i] != p[j]) j = next[j - 1];
		if (t[i] == p[j]) j++;
		if (j == m) {
			matches.push_back(i - m + 1);
			j = next[j - 1];
		}
	}
	return matches;
}
void solve()
{
	string s;
	cin >> s;
	int n = s.size();
	auto next = prefix(s);
	unordered_map<int, int> Ha;
	for (int i = 1; i < s.size() - 1; i++) Ha[next[i]] = 1;
	int x = next[n - 1];
	while(Ha.count(x) == 0 && x) x = next[x - 1];

	if (!x) cout << "Just a legend" << endl;
	else cout << s.substr(0, x) << endl;
}
```

* **1-base

```C++
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
