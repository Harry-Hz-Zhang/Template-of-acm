---
topic: "分块经典模型 每 k 个球就拿走一个，最后剩下的球在最开始的哪个位置"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 分块经典模型 每 k 个球就拿走一个，最后剩下的球在最开始的哪个位置

```C++
void solve()
{
	int n, k;
	cin >> n >> k;   // 一共 n 个球，每 k 个球就拿走一个
/*
如 n = 6，k = 2

[1,2,3,4,5,6]
|
[2,4,6]
|
[4]

*/
	int m = 0, d = 1;
	if (k <= sqrt(n)) {
		while (n > 1) {
			n -= (n + k - 1) / k;
			m++;
		}
		while (m > 0) {
			d += (d + k - 2) / (k - 1);  // 这一轮和上一轮差的球数
										 // 等价于 ceil(d / (k - 1))
			m--;
		}
	} else {
		while (n > 1) {
			int le = (n + k - 1) / k;
			int r = (n % k == 0 ? k : n % k);  // 分块 看余数
			int num = (r + le - 1) / le;   // 判断还能进行多少轮
			m += min(num, (n - 1) / le);
			n -= le * num;
		}
		while (m > 0) {
			int mo = (d + k - 2) / (k - 1);
			int r = (d % (k - 1) == 0 ? 1 : k - 1 - d % (k - 1));
			// 看能增加的余数是多少来看还有多少轮
			// 如果没有了，则最多一轮，就要切换
			// 如果还能再空余，每一轮会增加 mo 个，看多少轮过后能增加到 下一个块
			int num = (r + mo - 1) / mo;
			d += min(num, m) * mo;
			m -= num;
		}
	}
	cout << d << endl;
}
```

***
