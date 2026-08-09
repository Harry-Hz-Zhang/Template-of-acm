---
topic: "Z函数"
category: "11-string"
source: "字符串 String.md"
---

# Z函数

- $z[i]$ = 从位置 $i$ 开始的子串，与整个字符串 $s$ 的前缀（从位置 $0$ 开始）相等的最长长度。
- 例如，若 $s=$"$aaabaaa$"，那么：
    - 从 $i=1$ 开始的子串是 "$aabaaa$"，它与前缀 "$aaabaaa$" 相同的最大前缀长度是 $2$（"$aa$"），所以 $z[1]=2$.

```C++
std::vector<int> z_function(const std::string& s){
    int n = s.size() - 1;  // 1-base
	std::vector<int> z(n + 1, 0);
	z[1] = n;
	int l = 0, r = 0;
	for (int i = 2; i <= n; i++) {
		if(i <= r)	z[i] = std::min(z[i - l + 1], r - i + 1);
		while(i + z[i] <= n && s[1 + z[i]] == s[i + z[i]]) z[i]++;
		if(i + z[i] - 1 > r){
			l = i;
			r = i + z[i] - 1;
		}
	}
	return z;
}
```
