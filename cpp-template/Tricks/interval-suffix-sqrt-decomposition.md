---
topic: "后缀分块区间 给点求块编号"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 后缀分块区间 给点求块编号

<!-- image removed -->
如图：每个块的长度为 len =  n - i + 1， i = {1, 2, 3, 4, ... , n}.

* 可利用二分求解
*
```C++
auto find = [&](ll x) {
	int l = 1, r = n;
	while(l < r) {
		int mid = l + r >> 1;
		if((2 * n - mid + 1) * mid / 2 >= x) r = mid;
		else l = mid + 1;
	}
	return l;
};
```

***
