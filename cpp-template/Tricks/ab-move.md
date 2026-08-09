---
topic: "移动相邻的 AB"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 移动相邻的 AB

一个长度为 2N 的字符串 S 。其中 S 恰好包含 N 次的 `A` 和 N 次的 `B`。
求使 S 中没有相邻的相同字符所需的最少操作次数(可能为零)，其中一个操作包括交换 S 中相邻的两个字符。

就是第 i 个 A 也就是目标串中 第 i 个 A 的位置，所以就只需要考虑把串移动过去的带价值和

```C++
int idx = 1, res1 = 0, res2 = 0;
for (int i = 1; i <= n; i++) {
	if (s[i] == 'A') {
		res1 += abs(i - 2 * idx);
		res2 += abs(i - (2 * idx - 1));
		idx++;
	}
}
```
***
