---
topic: "二进制拆位法"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 二进制拆位法

* 题目当中一般都会含有异或的字样，而且最后要计算一个总贡献
当**不同的二进制位之间对答案的贡献是互不影响**的时候我们考虑拆位，对每一位求解贡献。

 [D. Sum of XOR Functions].(https://codeforces.com/contest/1879/problem/D)
```C++
void solve()
{
	int n;
	cin >> n;
	vector<int> a(n + 1);
	for (int i = 1; i <= n; i++) {
		cin >> a[i];
	}
  
	int ans = 0;
	for (int i = 0; i <= 30; i++) {
		vector<int> num(2, 0), sum(2, 0);
		num[0] = 1;
		int cur = 0, len = 0;
		for (int j = 1; j <= n; j++) {
			cur = (cur + (a[j] >> i & 1)) % 2;
			len = (len + num[1 - cur] * j - sum[1 - cur]) % mod;
			num[cur]++;
			sum[cur] += j;
		}
		ans = (ans + len * (1 << i) % mod) % mod;
	}
	cout << ans % mod << endl;
}
```

***
