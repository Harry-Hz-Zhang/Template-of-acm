---
topic: "Trick"
category: "11-string"
source: "字符串 String.md"
---

# Trick

## 括号串问题

* 在任何正规括号串中：任何一个 `(` 与它匹配的 `)` 的下标奇偶性是不同的。

* 每个偶数位的 `(` 必然与某个奇数位的 `)` 配对，所以 **偶数位的 `(` 的数量 = 奇数位的 `)` 的数量**，同理，每个奇数位的 `(` 必然与某个偶数位的 `)` 配对。

* 长度 `2n` 的合法括号串数是 Catalan 数 `C_n = (1/(n+1)) * C(2n,n)`

## 某种自动机

* 找到在某个下标时候下一个某个字母的位置
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
