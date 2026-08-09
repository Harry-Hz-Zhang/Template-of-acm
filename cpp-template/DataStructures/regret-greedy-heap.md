---
topic: "反悔贪心 heap"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 反悔贪心 heap

```C++
int n, mid, ans;
int a[N];
priority_queue<int> heap;
int main() {
	cin >> n;
	for (int i = 1; i <= n; i++) {
		cin >> a[i];
		heap.push(a[i]);
		if (!heap.empty() && a[i] < heap.top()) {
			ans += heap.top() - a[i];
			heap.pop();
			heap.push(a[i]);
		}
	}
	cout << ans << endl;
	return 0;
}
```
