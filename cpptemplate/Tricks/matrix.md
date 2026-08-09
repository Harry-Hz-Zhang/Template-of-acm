---
topic: "矩阵行跟列从左上到右下的遍历"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 矩阵行跟列从左上到右下的遍历

用两个指针 i，j 分别指向 行， 列
```C++
int i = 1, j = 1;
while(i + j <= n + m) {
	if(i + j == m + n || path[i + j - 2] == 'D')
	{ // 最右下角的位置只能是向下
		int res = 0;
		for (int x = 1; x <= m; x++){
			res -= a[i][x];
		}
		a[i][j] = res;
		i++;
	} else {
		int res = 0;
		for (int x = 1; x <= n; x++){
			res -= a[x][j];
		}
		a[i][j] = res;
		j++;
	}
}
```

***
