---
topic: "二分"
category: "02-basic"
source: "基础算法 Basic.md"
---

# 二分

* 当题目要我们枚举端点，或者看到第k大，第k小之类的字眼，可以去往二分想

```C++
while (l < r) {
	int mid = l + r >> 1;
	if (check(mid)) r = mid;
	else l = mid + 1;
}

while (l < r) {
	int mid = l + r + 1 >> 1;
	if (check(mid)) l = mid;
	else r = mid - 1;
}
```

[Problem - B - Codeforces](https://codeforces.com/contest/1902/problem/B)
```C++
void solve()
{
	int n, P, l, t;
	cin >> n >> P >> l >> t;
	int weeks = n / 7 + (n % 7 != 0);
	int L = 1, R = n;
	while(L < R) {
		int mid = L + R >> 1;
		if (mid * l + min(weeks, mid * 2) * t >= P) R = mid;
		else L = mid + 1;
	}
	cout << n - L << endl;
	return;
}
```
* 坑：可能会爆LL，所以有些题目 check 函数需要注意；


```C++
int pos1 = (partition_point(range_(preMax), [&](int v) { return v <= hi; }) - preMax.begin()) - 1;
```

`partition_point(range_(preMax), [&](int v){ return v <= hi; })`
- 在 `preMax[1..n]` 上找第一个使 `v <= hi` 为 **false** 的位置。
- `!(v <= hi)` 等价 `v > hi`，所以该 `it` 指向**第一个 `preMax[i] > hi`** 的迭代器；若没有 `> hi`，则返回 `preMax.end()`（对应位置 `n + 1`）

```C++
int pos2 = (partition_point(range_(preMin), [&](int v) { return v >= lo; }) - preMin.begin()) - 1;
```

- `partition_point(..., [&](int v){ return v >= lo; })` 返回第一个使 `v >= lo` 为 **false** 的位置，也就是第一个 `v < lo` 的迭代器；
- 若没有 `< lo`，返回 `end()`（`n+1`）
- `idx_it = it - preMin.begin()` 是第一个 `preMin[i] < lo` 的 1-based 下标，或 `n+1` 表示不存在。
- `pos2 = idx_it - 1`，范围 `0..n`

```C++
pos1 = (partition_point(range_(sufMax), [&](int v) { return v > hi; }) - sufMax.begin());

```
- `partition_point(..., [&](int v){ return v > hi; })` 返回第一个使 `v > hi` 为 **false** 的位置，也就是第一个 `v <= hi` 的迭代器；若没有 `<= hi`，返回 `end()`（`n+1`）

- `pos1 = idx_it`，范围 `1..n+1`


```C++
pos2 = (partition_point(range_(sufMin), [&](int v) { return v < lo; }) - sufMin.begin());
```

- `partition_point(..., [&](int v){ return v < lo; })` 返回第一个使 `v < lo` 为 **false** 的位置，即第一个 `v >= lo` 的迭代器；若没有 `>= lo`，返回 `end()`（`n+1`）
- `pos2 = idx_it`，范围 `1..n+1`


## 实数域

```C++
double lo = 0, hi = 1E12; 
while (hi - lo > std::max(1.0, lo) * eps) { 
	double mid = (lo + hi) / 2; 
	if (check(mid)) hi = x; 
	else lo = x; 
}
```
