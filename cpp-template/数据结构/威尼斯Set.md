---
topic: "威尼斯 Set"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 威尼斯 Set
https://codeforces.com/blog/entry/58316

```C++
struct venice_set {
  public:
	multiset<int> S;
	int water_level = 0;
	void add(int v) {
		S.insert(v + water_level);
	}
	void remove(int v) {
		S.erase(S.find(v + water_level));
	}
	void update_all(int v) {
		water_level += v;
	}
	int get_min() {
		return *S.begin() - water_level;
	}
	int size() {
		return S.size();
	}
};
```
