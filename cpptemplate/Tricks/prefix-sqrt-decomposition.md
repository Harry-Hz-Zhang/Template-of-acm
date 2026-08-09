---
topic: "前缀和的分块"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 前缀和的分块
[Problem - D - Codeforces](https://codeforces.com/contest/2026/problem/D)

```C++
#include<bits/stdc++.h>

using namespace std;
using i64 = long long;
using u64 = unsigned long long;

#define int long long
#define debug(x) cerr << #x" = " << x << '\n';

typedef pair<int, int> PII;

const i64 N = 2e5 + 10, INF = 1e18 + 10;

int mod;

void solve()
{
    int n;
    cin >> n;
    vector<int> a(n + 1), sa(n + 1, 0), sblock(n + 1, 0), block(n + 1, 0);
    // block[i] 表示从 i ~ n 的区间和
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        sa[i] = sa[i - 1] + a[i];
    }
    for (int i = 1; i <= n; i++) {
        block[1] += sa[i];
    }
    for (int i = 2; i <= n; i++) {
        block[i] = block[i - 1] - (n - i + 2) * a[i - 1];
    }
    for (int i = 1; i <= n; i++) {
        sblock[i] = sblock[i - 1] + block[i];
    }

    vector<int> A(n + 1);
    for (int i = 1; i <= n; i++) {
        A[i] = A[i - 1] + sa[i];
    }
    auto find = [&](int x) {   // 给定了方格数，求出该方格的块的编号是多少
        int l = 1, r = n;
        while(l < r) {
            int mid = l + r >> 1;
            if ((2 * n - mid + 1) * mid / 2 >= x) r = mid;
            else l = mid + 1;
        }
        return l;
    };
    auto sol = [&](int x, int l, int r) {  // 用来计算块内的从 l ~ r 的和
        return A[r] - A[l - 1] - (r - l + 1) * sa[x - 1];
    };   // 即 sol(2, 2, n) =  s(2, 2) + s(2, 3) + ... + s(2, n);
    int q;
    cin >> q;
    while(q--) {
        int l, r;
        cin >> l >> r;
        int L = find(l), R = find(r);
        if (L == R) {
            L--;
            l = l - (2 * n - L + 1) * L / 2;
            r = r - (2 * n - L + 1) * L / 2;      // 前面的所有块的数量总和
            cout << sol(L + 1, l + L, r + L) << endl;  
        } else {
            int ans = 0;
            ans += sblock[R - 1] - sblock[L];
            R--;
            r = r - (2 * n - R + 1) * R / 2;   
            ans += sol(R + 1, R + 1 ,r + (R + 1) - 1);   // 计算当前块内的前缀和
            L--;
            l = l - (2 * n - L + 1) * L / 2;
            ans += sol(L + 1, l + (L + 1) - 1, n);
            cout << ans << endl;
        }
    }
}

signed main()
{
    cin.tie(0) -> ios::sync_with_stdio(false);
    int T = 1;
    //cin >> T;
    while (T --) solve();
    return 0;
}
```
***
