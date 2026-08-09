---
topic: "LIS"
category: "10-dp"
source: "动态规划 DP.md"
---

# LIS

```C++
	vector<int> lis(n + 1);
	auto LIS = [&](const vector<int> &seq) -> void {
		int sz = seq.size() - 1;
		vector<int> tail;
		for (int i = 1; i <= sz; i++) {
			auto it = lower_bound(range(tail), seq[i]);
			if (it == tail.end()) {
				tail.push_back(seq[i]);
				lis[i] = tail.size();
			} else {
				*it = seq[i];
				lis[i] = (int)(it - tail.begin()) + 1;
			}
		}
	};
	LIS(a);
	int res = *max_element(range_(lis));
```

***
