---
topic: "SOS DP"
category: "10-dp"
source: "动态规划 DP.md"
---

# SOS DP

1. 求 **超集** 111001 最后也会算到 100001 这个贡献里面

```C++
vector<int> pre = f[u];
auto SOS = [&](int k, vector<int>& f) -> void {
	int N = 1 << k;
	for (int bit = 0; bit < k; bit++) {
		for (int mask = 0; mask < N; mask++) {
			if (!(mask & (1 << bit))) {
				f[mask] += f[mask | (1 << bit)];
				// 子集  <-  超集
			}
		}
	}
};
```

```C++
for(int d = 0; d < n; d++) {
	for(int s = 0; s < M; s++) {
		if(s & 1 << d) {
			st[s] &= st[s ^ 1 << d];
		}
	}
}
```


```C++
// -------------------------
// 求超集（superset）SOS 变换
// 对于每个 mask，最终 f[mask] = sum_{superset S of mask} orig[S]
// 原始示例（等价写法）：
// for (int bit = 0; bit < k; bit++) {
//   for (int mask = 0; mask < N; mask++) {
//     if (!(mask & (1 << bit))) {
//       f[mask] += f[mask | (1 << bit)]; // 子集 <- 超集
//     }
//   }
// }
// 注意：这里用的是 if (!(mask & (1 << bit))) 判断，等价于 if ((mask & (1<<bit)) == 0)
// -------------------------
void SOS_superset(int k, vector<int>& f) {
    int N = 1 << k;
    for (int bit = 0; bit < k; bit++) {
        for (int mask = 0; mask < N; mask++) {
            // 如果 mask 在 bit 位为 0，则把该位为 1 的超集的值加入到当前 mask
            if (!(mask & (1LL << bit))) {
                f[mask] += f[mask | (1LL << bit)]; // 子集 <- 超集
            }
        }
    }
}

// -------------------------
// 求子集（subset）SOS 变换（需要补全的部分）
// 对于每个 mask，最终 f[mask] = sum_{submask S of mask} orig[S]
// 常见实现：
// for (int bit = 0; bit < k; ++bit) {
//   for (int mask = 0; mask < N; ++mask) {
//     if (mask & (1 << bit)) f[mask] += f[mask ^ (1 << bit)];
//   }
// }
// 说明：只在 mask 的 bit 位为 1 时，把去掉该位的子掩码累加到 f[mask]
// -------------------------
void SOS_subset(int k, vector<int>& f) {
    int N = 1 << k;
    for (int bit = 0; bit < k; bit++) {
        for (int mask = 0; mask < N; mask++) {
            // 注意加上括号以避免移位与按位与优先级带来的歧义（虽大多数编译器会按期望解析）
            if (mask & (1LL << bit)) {
                f[mask] += f[mask ^ (1LL << bit)]; // 子集 <- 更小的子集（去掉 bit 位）
            }
        }
    }
}
```

