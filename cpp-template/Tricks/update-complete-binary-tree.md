---
topic: "关于完全二叉树建树和update的递归操作"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 关于完全二叉树建树和update的递归操作

注释：本例题的左右子树是反着的。

```C++
vector<int> f(n + 1);
function<int(int)> build = [&](int u) -> int {
	if ((u << 1) > n) {  // 如果是叶子节点 就是 u << 1 > n
		return f[u] = (s[u] == '?' ? 2 : 1);
	}
	if (s[u] == '0') {
		return f[u] = build(u << 1 | 1);
	} else if (s[u] == '1') {
		return f[u] = build(u << 1);
	} else {
		return f[u] = build(u << 1 | 1) + build(u << 1);
	}
};
for (int i = 1; i <= n; i++) {
	build(i);
}
```

```C++
vector<int> path;   // 0 left son    1 right son
int u = pos;  
while(u > 1) {   // 根节点不在里面，可以直接调用
    path.push_back(u & 1);
    u >>= 1;
}
reverse(path.begin(), path.end());
// 向下递归到目标节点之后返回值
// 向上递归过程中如果出现特殊情况 影响不再需要递归就返回 0 
function<int(int,int)> update = [&](int u, int idx) -> int {
    if (idx == (int)path.size()) {
        int oldv = f[u], now;
        if (s[u] == '0') now = ((u << 1) > n ? 1 : f[u << 1 | 1]);
        else if (s[u] == '1') now = ((u << 1) > n ? 1 : f[u << 1]);
        else now = ((u << 1) > n ? 2 : f[u << 1] + f[u << 1 | 1]);
        f[u] = now;
        return now - oldv;
    }
    int delta;
    if (path[idx] == 0) {
        delta = update(u << 1, idx + 1);
        if (s[u] != '0') {
            f[u] += delta;
            return delta;
        }
        return 0;
    } else {
        delta = update(u << 1 | 1, idx + 1);
        if (s[u] != '1') {
            f[u] += delta;
            return delta;
        }
        return 0;
    }
};
```

***
