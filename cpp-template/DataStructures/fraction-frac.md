---
topic: "分数 Frac"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 分数 Frac

```C++
template<class T>
struct Frac {
  public:
    T num, den;  // 分子 分母
    Frac(T num_, T den_) : num(num_), den(den_) {
        if (den < 0) {
            den = -den;
            num = -num;
        }
    }
    Frac() : Frac(0, 1) { }
    Frac(T num_) : Frac(num_, 1) { }
    explicit operator double() const {
        return 1.0L * (num) / (den);
    }
    Frac &operator+= (const Frac &b) {
        num = num * b.den + b.num * den;
        den *= b.den;
        return *this;
    }
    Frac &operator-= (const Frac &b) {
        num = num * b.den - b.num * den;
        den *= b.den;
        return *this;
    }
    Frac &operator*= (const Frac &b) {
        num *= b.num;
        den *= b.den;
        return *this;
    }
    Frac &operator/= (const Frac &b) {
        num *= b.den;
        den *= b.num;
        if (den < 0) {
            num = -num;
            den = -den;
        }
        return *this;
    }
    friend Frac operator+ (Frac a, const Frac &b) {
        return a += b;
    }
    friend Frac operator- (Frac a, const Frac &b) {
        return a -= b;
    }
    friend Frac operator* (Frac a, const Frac &b) {
        return a *= b;
    }
    friend Frac operator/ (Frac a, const Frac &b) {
        return a /= b;
    }
    friend Frac operator- (const Frac &a) {
        return Frac(-a.num, a.den);
    }
    friend Frac operator* (Frac a, i64 k) { 
        return a *= Frac((T)k); 
    }
    friend Frac operator* (i64 k, Frac a) { 
        return a *= Frac((T)k); 
    }
    friend bool operator== (const Frac &a, const Frac &b) {
        return a.num * b.den == b.num * a.den;
    }
    friend bool operator!= (const Frac &a, const Frac &b) {
        return a.num * b.den != b.num * a.den;
    }
    friend bool operator< (const Frac &a, const Frac &b) {
        return a.num * b.den < b.num * a.den;
    }
    friend bool operator> (const Frac &a, const Frac &b) {
        return a.num * b.den > b.num * a.den;
    }
    friend bool operator<= (const Frac &a, const Frac &b) {
        return a.num * b.den <= b.num * a.den;
    }
    friend bool operator>= (const Frac &a, const Frac &b) {
        return a.num * b.den >= b.num * a.den;
    }
    friend std::ostream &operator<<(std::ostream &os, Frac x) {
        T g = gcd(x.num, x.den);
        if (x.den == g) {
            return os << x.num / g;
        } else {
            return os << x.num / g << "/" << x.den / g;
        }
    }
};
```
