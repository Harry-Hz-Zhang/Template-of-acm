---
topic: "求解区间和恰好为k的区间的个数"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 求解区间和恰好为k的区间的个数

```C++
map<int, int> cnt;
int sum = 0, n;
// 枚举到 i 的前缀和是 sum
for (int i = 1; i <= n; i++) {
	if (cnt.count(sum - k)) {
		//"YES";
	}
}
```

变形后也要会写：（只统计多少个前缀是奇数，多少个是偶数）

* 记录某一个区间内 0 和 1 的个数时候相等，也就是过去是否有 0 1 个数相等的情况，则记录下 0，1 的奇偶性，然后查询同样奇偶性的状态时候存在，如果存在，则就是对的。

* 记录多少个区间乘积是正数，多少个是负数：

```C++
void solve() {
	int n;
	cin >> n;
	vector<int> a(n + 1);
	for (int i = 1; i <= n; i++) cin >> a[i];
	vector<int> cnt(2, 0);
	cnt = {1, 0};

	int ansPos = 0, ansNeg = 0;
	int c = 0;
	for (int i = 1; i <= n; i++) {
		c ^= (a[i] < 0);
		ansPos += cnt[c];
		ansNeg += cnt[c ^ 1];
		cnt[c] ++;
	}
	cout << ansNeg << ' ' << ansPos << endl;
}
```
***
