---
topic: "单调栈 stk"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 单调栈 stk

* **求解序列中的每一个数左/右边，离它最近的 大/小 的数字在什么地方（下标/具体值）**
* 单调栈也可以用于维护一个单调递增序列的最大贡献
```C++
// eg: 维护一个元素左右第一个 **小于** 该元素的位置 // 维护单减栈
// 灵活运用+1之后就是最后一个（最靠左/右）的大于该元素的位置
stack<int> stk;
vector<int> l_res(n + 1), r_res(n + 1);
for (int i = 1; i <= n; i++) {
	while(!stk.empty() && a[stk.top()] >= a[i]) stk.pop();
	l_res[i] = stk.empty() ? 0 : stk.top();
	stk.push(i);
}
while(stk.size()) stk.pop();
for (int i = n; i >= 1; i--) {
	while(!stk.empty() && a[stk.top()] >= a[i]) stk.pop();
	r_res[i] = stk.empty() ? n + 1 : stk.top();
	stk.push(i);
}
```
