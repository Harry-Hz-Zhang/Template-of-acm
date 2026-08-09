---
topic: "快读 Read"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 快读 Read

```C++
#include <bits/stdc++.h>
#pragma GCC optimize("O3")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")
using namespace std;
namespace FastIO {
    const int LEN = 1 << 20;
    char in[LEN], out[LEN], *p1 = in, *p2 = in, *pp = out;
    
    inline char gc() {
        return p1 == p2 && (p2 = (p1 = in) + fread(in, 1, LEN, stdin), p1 == p2) ? EOF : *p1++;
    }
    inline void pc(char c) {
        if (pp - out == LEN) fwrite(out, 1, LEN, stdout), pp = out;
        *pp++ = c;
    }
    struct Cin {
        // 兼容 cin.tie(nullptr) 和 sync_with_stdio(false)
        void tie(void*) { }
        void sync_with_stdio(bool) { }
        template <typename T>
        inline Cin& operator>>(T &x) {
            x = 0; char c = gc(); bool f = 0;
            while (c < '0' || c > '9') { if (c == '-') f = 1; c = gc(); }
            while (c >= '0' && c <= '9') x = (x << 3) + (x << 1) + (c ^ 48), c = gc();
            if (f) x = -x;
            return *this;
        }
        inline Cin& operator>>(char &c) {
            c = gc(); while (c <= 32) c = gc();
            return *this;
        }
        inline Cin& operator>>(char *s) {
            char c = gc(); while (c <= 32) c = gc();
            while (c > 32) *s++ = c, c = gc();
            *s = 0;
            return *this;
        }
        inline Cin& operator>>(string &s) {
            s.clear(); char c = gc(); while (c <= 32) c = gc();
            while (c > 32) s += c, c = gc();
            return *this;
        }
    } cin_fast;
    
    struct Cout {
        ~Cout() { fwrite(out, 1, pp - out, stdout); }
        
        template <typename T>
        inline Cout& operator<<(T x) {
            if (x < 0) pc('-'), x = -x;
            static int st[40]; int top = 0;
            do st[++top] = x % 10, x /= 10; while (x);
            while (top) pc(st[top--] + '0');
            return *this;
        }
        inline Cout& operator<<(char c) { pc(c); return *this; }
        inline Cout& operator<<(const char *s) { while (*s) pc(*s++); return *this; }
        inline Cout& operator<<(const string &s) { for (char c : s) pc(c); return *this; }
        // 支持 cout << endl;
        inline Cout& operator<<(ostream& (*)(ostream&)) { pc('\n'); return *this; }
    } cout_fast;
}
//#define cin FastIO::cin_fast
//#define cout FastIO::cout_fast
```
