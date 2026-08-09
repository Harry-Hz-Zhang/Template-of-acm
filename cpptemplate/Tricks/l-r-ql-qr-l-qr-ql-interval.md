---
topic: "存在区间 (l,r) 完全包含在 (ql,qr) 当且仅当 L\\[qr] >= ql"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 存在区间 (l,r) 完全包含在 (ql,qr) 当且仅当 L\[qr] >= ql

```C++
	vector<PII> ranges;
	vector<int> L(n + 2, 0);
	for (auto [l, r] : ranges) {
		L[r] = max(L[r], l);
	}
	for (int i = 1; i <= n; i++) {
		L[i] = max(L[i], L[i - 1]);
	}
  
	while (q--) {
		int l, r;
		cin >> l >> r;
		if (l <= L[r]) cout << "YES\n";  // 查询区间中有完整的合法区间存在
		else cout << "NO\n";
	}
```

***
