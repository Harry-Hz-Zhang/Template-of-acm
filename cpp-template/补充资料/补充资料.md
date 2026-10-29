---
topic: "补充"
category: "supplements"
source: "补充.md"
---

**模板 1：经典旋转卡壳，求凸包直径**

前提：

- `ch` 是**严格凸**、**逆时针**
- 你现在这个 `get_hull()` 用了 `<= / >=`，正好就是我想要的这种“去掉共线内点”的 hull

```cpp
template<typename T = double>
i128 convex_diameter2(const Polygon<T> &ch) {
    int n = (int)ch.size();
    if (n <= 1) return 0;
    if (n == 2) return dist2_i128(ch[0], ch[1]);

    int j = 1;
    i128 ans = 0;

    for (int i = 0; i < n; i++) {
        int ni = (i + 1) % n;

        while (cross_i128(ch[ni] - ch[i], ch[(j + 1) % n] - ch[j]) > 0) {
            j = (j + 1) % n;
        }

        ans = max(ans, dist2_i128(ch[i], ch[j]));
        ans = max(ans, dist2_i128(ch[ni], ch[j]));
    }

    return ans;
}
```

这个板子就是最经典那种：

- 枚举一条边 `i -> i+1`
- `j` 去找和这条边“最对着”的点
- `j` 只会单调前进一圈

---

**模板 2：线性函数最值版旋转卡壳**

这个就是你这道题真正该用的板子。

含义：

- 固定一个点 `A`
- `B` 在凸包上按顺序扫
- 对每个 `ab = B - A`
- 在线性时间里维护让 `dot(ab, C - A)` 最小的 `C`

```cpp
template<typename T = double>
i128 min_dot_rotating_calipers(const Polygon<T> &ch, const Point<T> &A) {
    int m = (int)ch.size();
    if (m <= 1) return 0;

    vector<Point<T>> H(m * 2);
    for (int i = 0; i < m; i++) {
        H[i] = H[i + m] = ch[i];
    }

    i128 res = 0;
    int j = 0;

    for (int i = 0; i < m; i++) {
        if (j < i) j = i;

        Point<T> ab = H[i] - A;

        // 如果沿着边 j -> j+1 继续走，dot 还在下降，就继续推 j
        while (j + 1 < i + m && dot_i128(ab, H[j + 1] - H[j]) < 0) {
            j++;
        }

        res = min(res, dot_i128(ab, H[j] - A));
        if (j + 1 < i + m) {
            res = min(res, dot_i128(ab, H[j + 1] - A));
        }
    }

    return res;
}
```

这个板子背后的判断条件你一定要记住：

```cpp
dot_i128(ab, H[j + 1] - H[j]) < 0
```

含义是：

- 从 `H[j]` 走到 `H[j+1]`
- 目标函数 `dot(ab, C - A)` 还在继续减小
- 那就继续推指针

一旦不小了，最优点就在 `j / j+1` 附近。

---

**基于这个板子，Astral Decay 的 `solve()` 可以直接写成这样**

```cpp
void solve() {
    int n;
    cin >> n;
    vector<Point<int>> p(n);
    for (int i = 0; i < n; i++) {
        p[i].read();
    }

    auto ch = get_hull(p);

    i128 ans = 0;
    for (auto &A : p) {
        ans = min(ans, min_dot_rotating_calipers(ch, A));
    }

    cout << ans << '\n';
}
```

---

**如果你想做一个“更通用”的旋转卡壳记忆法**

你可以把旋转卡壳大致分成两类：

1. `边 -> 点`
   典型：凸包直径、最小宽度、最小面积矩形
   判的是 `cross`
2. `方向 -> 支撑点`
   典型：这道题、线性函数在凸包上的最值
   判的是 `dot`

你这次容易绕晕，就是因为把第二类题硬往“点在线哪一侧”上套了。
