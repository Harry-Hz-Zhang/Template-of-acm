---
topic: "每一位都有限制 凑出 i 个数字的下标得到几"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 每一位都有限制 凑出 i 个数字的下标得到几

* 贪心的填写较为大的数字，因为小的数字总是好填的
```C++
vector<int> a(n + 1), pre(n + 1), suf(n + 1);
// 前缀凑出来 i 个数字需要下标到几，后缀同理
for (int i = 1; i <= n; i++) {
	cin >> a[i];
}
// a[i] 表示每一位数字的限制（最大不超过 a[i]）

set<int> S;
for (int i = 1; i <= n; i++) S.insert(i);

int now = 0;
for (int i = 1; i <= n; i++) {
	auto it = S.upper_bound(a[i]);  // 找到更大的数字 --it 以确定出来最大的不超过limit的数字是几
	if (!S.size() || it == S.begin()) continue;  // 没有的话就直接跳过
	S.erase(--it);
	pre[++now] = i;   // 证明可以多插入一个数字了
}   

now = 0;
for (int i = 1; i <= n; i++) S.insert(i);
for (int i = n; i >= 1; i--) {
	auto it = S.upper_bound(a[i]);
	if (!S.size() || it == S.begin()) continue;
	S.erase(--it);
	suf[++now] = i;
}
```
***
