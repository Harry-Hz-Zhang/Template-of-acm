---
topic: "关于区间的合并 和 包含区间（冗余）的删除"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 关于区间的合并 和 包含区间（冗余）的删除

```C++
int n;
cin >> n;
vector<PII> ran(n);
sort(range(ran), [&](PII &A, PII &B) {
	return A.first != B.first ? A.first < B.first : A.second > B.second;
});
vector<PII> kee;
for (auto &[l, r] : ran) {
	if (kee.size() && r <= kee.back().second) continue;
	kee.push_back({l, r});
}
ran = kee;
n = ran.size();
// 剩余的区间单调递增，l，r 都递增

vector<PII> mer;
sort(range(ran));
for (auto &[l, r] : ran) {
	if (mer.empty() || l > mer.back().second) mer.push_back({l, r});
	else mer.back().second = max(mer.back().second, r);
}
```


***
