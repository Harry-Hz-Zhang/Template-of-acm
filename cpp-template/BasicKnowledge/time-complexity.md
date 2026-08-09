---
topic: "计算时间复杂度是很重要的"
category: "17-basic-knowledge"
source: "Z 基础知识.md"
---

# 计算时间复杂度是很重要的

**不要因为觉得很暴力就不去思考，这样你可能就会丧失一个正解**
**永远都是先思考暴力再思考正解**

***

```C++
#include <bits/stdc++.h>
using namespace std;

struct Item { int key; string name; };

struct MinCmp {
    bool operator()(const Item &a, const Item &b) const {
        return a.key > b.key; // 注意：返回 true 表示 a 的优先级比 b 低
    }
};

int main() {
    priority_queue<Item, vector<Item>, MinCmp> min_pq;
    min_pq.push({3,"c"});
    min_pq.push({1,"a"});
    min_pq.push({2,"b"});
    cout << min_pq.top().key << '\n'; // 输出 1（小根堆）
}
```
