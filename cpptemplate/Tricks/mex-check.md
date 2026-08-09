---
topic: "求 MEX 的 check 函数"
category: "16-tricks"
source: "Tricks 经验积累.md"
---

# 求 MEX 的 check 函数

```C++
auto check = [&](int mid) -> bool {
    int cnt = 0, cur = 0;
    vector<int> S(mid, 0);
    //cout << mid << endl;
    for (int i = 1; i <= n; i++) {
        if (a[i] < mid && !S[a[i]]) {
            S[a[i]] = 1;
            cur++;
            if (cur == mid) {
                cnt++;
                fill(S.begin(), S.end(), 0);
                cur = 0;
            }
        }
    }
    return cnt >= k;
};
```
***
