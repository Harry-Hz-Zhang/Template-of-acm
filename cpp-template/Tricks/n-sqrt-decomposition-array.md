---
topic: "n 不断取根号 将数组分块"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# n 不断取根号 将数组分块
```C
while (n > 2) {
    int s = ceil(sqrt(n));
    for (int i = s + 1; i < n; i++) {
	    // 操作
    }
    n = s;
}
```


***
