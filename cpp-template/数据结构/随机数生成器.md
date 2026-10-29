---
topic: "随机数 Rand"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 随机数 Rand

```C++
struct Rand {
  public:
    mt19937_64 eng;
    Rand() : eng(random_device{}()) {}
    explicit Rand(uint64_t seed) : eng(seed) {}
    template <typename T>
    T gen(T l, T r) {
        if constexpr (is_integral_v<T>) return uniform_int_distribution<T>(l, r)(eng);
        else return uniform_real_distribution<T>(l, r)(eng);
    }
    template <typename T>
    T operator()(T l, T r) { return gen(l, r); }
#if __cplusplus > 202002L
    template <typename T>
    T operator[](T l, T r) { return gen(l, r); }
#endif
    double operator()() { return uniform_real_distribution<double>()(eng); }
    // 随机 bool，p 为 true 的概率
    bool bernoulli(double p = 0.5) {
        return bernoulli_distribution(p)(eng);
    }
    // 打乱容器
    template <typename Container>
    void shuffle(Container& c) {
        std::shuffle(range_(c), eng);
    }
}R;
```
