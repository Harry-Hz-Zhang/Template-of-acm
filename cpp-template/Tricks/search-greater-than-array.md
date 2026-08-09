---
topic: "寻找数组中最靠左 / 靠右大于某个数的数字"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 寻找数组中最靠左 / 靠右大于某个数的数字

如果我们要找寻一个数组中，最靠左/最靠右的大于某个数字的数，考虑按照值的大小排序，这样就转化成了排序后每个值右边序号的最大值和最小值，所以逆序扫描一遍。

```C++
struct node {
	int id, x;
};
vector<node> a(n + 1);
for (int i = 1; i <= n; i++) {
	cin >> a[i].x;
	a[i].id = i;
}
sort(a.begin() + 1, a.end(), [&](node a, node b) {
	return a.x < b.x;
});
int Max = -INF, Min = INF;

for (int i = n; i >= 1; i--) {
	int now = a[i].x;
	int id = a[i].id;
	Max = max(Max, id);
	Min = min(Min, id);
}
```

***
