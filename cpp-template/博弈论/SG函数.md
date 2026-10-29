---
topic: "关于$SG$函数"
category: "12-game-theory"
source: "博弈论 Game.md"
---

# 关于$SG$函数

$SG(x) = mex(S) = min {x}$

$SG(x)=mex( {SG(y1),SG(y2),…,SG(yk)} )$   如图

<!-- image removed -->

~~结论二则：~~
* **$SG(x) = 0$ 则必败**，**否则必胜**（若非零说明这个点直接指向了 $0$，也就意味着可以到达必败状态，是必胜状态）

* 对于由 n 个有向图游戏组成的组合游戏 设它们的起点分别为 $s_1$, $s_2$ ,..., $s_n$​（好多个起点，有好多个博弈图，也就是有好多个上图) 则当且仅当 $SG$ ($s_1$) ⊕ $SG$ ($s_2$) ⊕ . . . ⊕ $SG$ ($s_n$) $≠0$.这个游戏为 **先手必胜** (也就是Nim游戏的结论，每个子游戏的SG值均为石子数量)

**是独立游戏而且是ICG才能拆成若干个小的游戏，并取最后的异或和。**

### $SG$函数模板

```C++
vector<int> fab(30, 0), f(1010, -1);
void init() {   
    fab[1] = 1, fab[2] = 2;
    for (int i = 3; i <= 27; i++) {
        fab[i] = fab[i - 1] + fab[i - 2];
    }
}
int sg(int u) {
    if (f[u] != -1) return f[u];
    set<int> S;
    for (int i = 1; ; i++) {
        if (u - fab[i] >= 0) S.insert(sg(u - fab[i]));
        else break;
    }
    for (int i = 0;; i++) {
        if (S.count(i) == 0) {
            return f[u] = i;
        }
    }
}
void solve()
{
    int a, b, c;
    while(cin >> a >> b >> c, a | b | c) {
        cout << (sg(a) ^ sg(b) ^ sg(c) == 0 ? "Nacci" : "Fibo") << endl;
    }
}
```

## 树上博弈

* 找根节点和叶子节点的关系 eg：100010010101

