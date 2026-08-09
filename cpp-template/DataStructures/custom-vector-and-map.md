---
topic: "自定义 vector + map"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 自定义 vector + map

```cpp
namespace my {
    static int vector_pool[24000000];
    unsigned int pool_ptr = 1;
    struct vector {
        unsigned int idx = 0;
        unsigned int sz = 0;
        unsigned int cap = 0;
        inline unsigned int size() const { return sz; }
        inline void push_back(int v) {
            if (sz == cap) {
                unsigned int ncap = cap == 0 ? 2 : cap * 2;
                unsigned int nidx = pool_ptr;
                pool_ptr += ncap;
                if (sz > 0) {
                    memcpy(vector_pool + nidx, vector_pool + idx, sz * sizeof(int));
                }
                idx = nidx;
                cap = ncap;
            }
            vector_pool[idx + sz] = v;
            sz++;
        }
        inline void assign(size_t n, int v) {
            if (n > cap) {
                cap = n;
                idx = pool_ptr;
                pool_ptr += cap;
            }
            sz = n;
            for (size_t i = 0; i < n; ++i) vector_pool[idx + i] = v;
        }
        inline int& operator[](size_t i) { return vector_pool[idx + i]; }
        inline vector& operator=(const vector& o) {
            if (o.sz > cap) {
                cap = o.sz;
                idx = pool_ptr;
                pool_ptr += cap;
            }
            sz = o.sz;
            if (sz > 0) memcpy(vector_pool + idx, vector_pool + o.idx, sz * sizeof(int));
            return *this;
        }
    };
}

template<int MAX_KEYS, int MAX_VALUES>
struct context_map {
    inline static int dense_id[MAX_KEYS];
    inline static int id_cnt = 0;
    static inline int get_id(int k) {
        if (!dense_id[k]) dense_id[k] = ++id_cnt;
        return dense_id[k];
    }
    template<typename V>
    struct shared {
        V pool[MAX_VALUES];
        inline V& operator[](int key) {
            return pool[get_id(key)];
        }
    };
    template<typename V>
    struct Direct {
        V pool[MAX_KEYS];
        inline V& operator[](int key) {
            return pool[key];
        }
    };
};
using ctx = context_map<4000005, 2000005>;
ctx::shared<my::vector> pos;
ctx::shared<my::vector> f;
ctx::shared<my::vector> pre;
ctx::Direct<int> cnt;
ctx::Direct<int> idx;
ctx::Direct<char> vis;
```
