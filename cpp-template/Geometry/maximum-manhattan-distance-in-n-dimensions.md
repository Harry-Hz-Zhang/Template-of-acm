---
topic: "N维空间下的多点曼哈顿距离的最大值"
category: "06-geometry"
source: "几何 Geometry.md"
---

# N维空间下的多点曼哈顿距离的最大值

```C++
template<class T>
T GetManhattan(const vector<vector<T>>& p) {   // 每个点 每个维度坐标
	int d = p.front().size() - 1, n = p.size() - 1;
	T ans = 0, Min, Max;
	for (int sta = 0; sta < (1 << d); sta++) {    //用二进制形式遍历所有可能的运算情况
		Min = INF, Max = -INF;
		for (int j = 0; j < n; j++) {
			T sum = 0;
			for (int bit = 0; bit < d; bit++) {
				sum += p[j][bit] * (sta >> bit & 1 ? 1 : -1);
			}
			Max = max(Max, sum), Min = min(Min, sum);
		}
		if (Max - Min > ans) ans = Max - Min;
	}
	return ans;
}
```
