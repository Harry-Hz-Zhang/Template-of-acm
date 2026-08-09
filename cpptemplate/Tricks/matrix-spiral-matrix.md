---
topic: "螺旋矩阵"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 螺旋矩阵

```C++
const int dx[4] = {0, 1, 0, -1}, dy[4] = {1, 0, -1, 0};

int n;
vector<vector<int>> a(n + 2, vector<int>(n + 2));
int mid;

if (n & 1) mid = (n + 1) / 2;
else mid = n / 2;

int l = 1, num = 0, d = 0, x = mid, y = mid;
a[x][y] = num++;

while(num < n * n) {
	for (int i = 0; i < 2; i++) {
		for (int j = 0; j < l; j++) {
			if (num >= n * n) break;
			x += dx[d], y += dy[d];
			a[x][y] = num++;
		}
		d = (d + 1) % 4;
	}
	l++;
}
```
***
