---
topic: "Manacher (马拉车)"
category: "11-string"
source: "字符串 String.md"
---

# Manacher (马拉车)

* 这里的 $r[i]$ 表示的是带有中心点的半径长度，所以答案就是 $r[i] - 1$

```C++
std::vector<int> manacher(std::string s) {
	while(s.front() == ' ') s = s.substr(1);
	string t = "$#";
	for (auto c : s) {
		t += c;
		t += "#";
	}
	int n = t.size() - 1;
	vector<int> r(n + 1, 0);
	for (int i = 1, j = 0; i <= n; i++) {  //j 表示已知回文串中向右延伸最远的那个回文串的中心下标
		if (i <= j + r[j]) r[i] = min(r[2 * j - i], j + r[j] - i);
		while(i + r[i] <= n && t[i - r[i]] == t[i + r[i]]) r[i]++;
		if (i + r[i] > j + r[j]) j = i;
	}
	return r;
}
```

## 寻找一个最大的回文后缀 (马拉车模板)

```C++
std::vector<int> manacher(std::string s) {
	while(s.front() == ' ') s = s.substr(1);
	string t = "$#";
	for (auto c : s) {
		t += c;
		t += "#";
	}
	int n = t.size() - 1; 
	vector<int> r(n + 1, 0);
	for (int i = 1, j = 0; i <= n; i++) {  //j 表示已知回文串中向右延伸最远的那个回文串的中心下标
		if (i <= j + r[j]) r[i] = min(r[2 * j - i], j + r[j] - i);
		while(i + r[i] <= n && t[i - r[i]] == t[i + r[i]]) r[i]++;
		if (i + r[i] > j + r[j]) j = i;
	}
	return r;
}

void solve()
{
	string s;
	cin >> s;
	s = ' ' + s;
	vector<int> r = manacher(s);
	int n = s.size();
	int l = 0;
	while(r[l + n] < n - l){
		l++;
	}

	int num = r[n + l];
	auto t = s.substr(1, l);	
	reverse(t.begin(), t.end());
	auto ans = s.substr(1) + t;
	cout << ans << endl;
}
```
