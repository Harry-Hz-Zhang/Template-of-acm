---
topic: "数位DP模板"
category: "10-dp"
source: "动态规划 DP.md"
---

# 数位DP模板

```C++
int dfs(int pos, int pre, int lead, int limit) {
    if (!pos) {
    	边界条件
    }
    if (!limit && !lead && dp[pos][pre] != -1) return dp[pos][pre];
    int res = 0, up = limit ? a[pos] : 无限制位;
    for (int i = 0; i <= up; i ++) {
        if (不合法条件) continue;
        res += dfs(pos - 1, 未定参数, lead && !i, limit && i == up);
    }
    return limit ? res : (lead ? res : dp[pos][sum] = res);
}
int cal(int x) {
    memset(dp, -1, sizeof dp);
    len = 0;
    while (x) a[++ len] = x % 进制, x /= 进制;
    return dfs(len, 未定参数, 1, 1);
}
signed main() {
    cin >> l >> r;
    cout << cal(r) - cal(l - 1) << endl;
}
```

### 关于求解 \[0,  n - 1] 所有数字的数位之和

```C++
// 模板：计算 0..n-1 每个整数各位数字之和的累加（sum_{x=0}^{n-1} sumdigits(x))
// 采用按位从高到低的分解：对 n 的每一位 d_i，统计当该位取 0..d_i-1 时
// 高位贡献 + 低位贡献，累加得到总和。
long long sum_digits_prefix_count(long long n) {
    if (n <= 0) return 0;
    string s = to_string(n);
    int l = (int)s.size();
    int ps = 0; // 前缀各位和 S_{i-1}
    long long cur_count = 9;
    for (int i = 1; i < l; ++i) cur_count *= 10; // cur_count = 9 * 10^{l-1}
    long long pow10 = cur_count / 9; // pow10 = 10^{l-1}
    long long ans = 0;
    for (int i = 0; i < l; ++i) {
        int d = s[i] - '0';
        if (d) {
            long long L = pow10; // 10^{l-i-1}
            // 高位 + 当前位贡献
            ans += L * ( (long long)d * ps + (long long)d * (d - 1) / 2 );
            // 低位（后缀）贡献： d * t * 45 * 10^{t-1}, t = l-i-1
            int t = l - i - 1;
            if (t > 0) {
                ans += (long long)d * t * 45LL * (L / 10);
            }
        }
        ps += d;
        pow10 /= 10;
    }
    return ans;
}
// wrapper
long long compute_sum_0_to_nminus1(long long n) {
    return sum_digits_prefix_count(n);
}

int main() {
    vector<long long> inputs;
    long long x;
    while ( (cin >> x) ) inputs.push_back(x);
    for (long long v : inputs) {
        cout << compute_sum_0_to_nminus1(v) << "\n";
    }
    return 0;
}
```
***
