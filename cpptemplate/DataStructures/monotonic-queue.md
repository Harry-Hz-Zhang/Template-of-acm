---
topic: "单调队列 deque"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 单调队列 deque

* **单调队列就是一种队列内的元素有单调性的队列。
* **最优解就存在队首，而队尾则是最后进队的元素。因为其单调性所以经常会被用来维护区间最值 或者 降低DP的维数已达到降维来减少空间及时间的目的**

```C++
int n, k;  //序列的长度和窗口的长度
vectors<int> a(n + 1);
deque<int> dq;
for (int i = 1; i <= n; i++) {
	while(!dq.empty() && dq.front() <= i - k) dq.pop_front();
	int val = a[i];
	while(!dq.empty() && a[dq.back()] <= val) dq.pop_back();
	dq.push_back(i);
	ansMax[i] = a[dq.front()];
}
dq.clear();
for (int i = 1; i <= n; i++) {
	while(!dq.empty() && dq.front() <= i - k) dq.pop_front();
	int val = a[i];
	while(!dq.empty() && a[dq.back()] >= val) dq.pop_back();
	dq.push_back(i);
	ansMin[i] = a[dq.front()];
}
```
