---
topic: "ST表 RMQ"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## ST表 RMQ

```C++
template<typename T, class Op>
struct ST {
  public:
    int n, LOG;
    vector<vector<T>> st;
    Op op;
    ST(int n_ = 0, const vector<T>& a = vector<T>()) { init(n_, a); }
    void init(int n_, const vector<T>& a){
        n = n_;
        if(n <= 0) { LOG = 0; st.clear(); return; }
        LOG = 1;
        while((1 << LOG) <= n) LOG++;
        st.assign(n + 1, vector<T>(LOG + 1, Op::identity()));

        for(int i = 1; i <= n; i++) st[i][0] = (i < a.size() ? a[i] : Op::identity());
        for(int j = 1, len = 2; len <= n; j++, len <<= 1) {
            for(int i = 1; i + len - 1 <= n; i++) {
                st[i][j] = op(st[i][j - 1], st[i + (len >> 1)][j - 1]);
            }
        }
    }
    inline T find(int l, int r){
        if(n <= 0) return Op::identity();
        if(l < 1) l = 1; 
        if(r > n) r = n; 
        if(l > r) return Op::identity();
        int len = r - l + 1, t = 31 - __builtin_clz((unsigned)len);
        return op(st[l][t], st[r - (1<<t) + 1][t]);
    }
};

template<typename T>
struct op_max {
    T operator()(T a, T b) const { return a > b ? a : b; }
    static T identity(){ return numeric_limits<T>::min(); }
};
template<typename T>
struct op_min {
    T operator()(T a, T b) const { return a < b ? a : b; }
    static T identity(){ return numeric_limits<T>::max(); }
};
struct op_gcd {
    int operator()(int a, int b) const {
        int aa = llabs(a), bb = llabs(b);
        if(aa == 0) return bb; 
        if(bb == 0) return aa;
        return gcd(aa, bb);
    }
    static int identity(){ return 0; }
};
struct op_lcm {  // 基本都会超
    int operator()(int a, int b) const {
        int aa = llabs(a), bb = llabs(b);
        if(aa == 0 || bb == 0) return 0;
        int g = gcd(aa, bb);
        return llabs((aa / g) * bb);
    }
    static int identity(){ return 1; }
};
// ST<int, op_min<int>> st(n, a);

```
