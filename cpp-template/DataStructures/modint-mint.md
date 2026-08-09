---
topic: "模类 Mint"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 模类 Mint

```C++
constexpr int64_t safe_mod(int64_t x, int64_t m = mod) {
    x %= m;
    if (x < 0) x += m;
    return x;
}
// 快乘法
struct barrett {
    uint32_t _m;
    uint64_t im;
    explicit barrett(uint32_t m) : _m(m), im((uint64_t)(-1) / m + 1) { }
    uint32_t umod() const { return _m; }
    uint32_t mul(uint32_t a, uint32_t b) const {
        uint64_t z = a;
        z *= b;
        uint64_t x = (uint64_t)(((__uint128_t)z * im) >> 64LL);
        uint64_t y = x * _m;
        return (unsigned int)(z - y + (z < y ? _m : 0));
    }
};
// 快速幂
constexpr int64_t pow_mod(int64_t x, int64_t n, const int m = mod) {
    if (m == 1) return 0;
    const uint32_t _m = uint32_t(m);
    uint64_t r = 1;
    uint64_t y = safe_mod(x, m);
    while (n) {
        if (n & 1) r = (r * y) % _m;
        y = (y * y) % _m;
        n >>= 1LL;
    }
    return r;
}

// Miller–Rabin 判质数
constexpr bool is_prime_constexpr(int n) {
    if (n <= 1) return 0;
    if (n == 2 || n == 7 || n == 61) return 1;
    if (n % 2 == 0) return 0;
    int64_t d = n - 1;
    while (d % 2 == 0) d /= 2LL;
    constexpr int64_t bases[3] = {2, 7, 61};
    for (int64_t a : bases) {
        int64_t t = d;
        int64_t y = pow_mod(a, t, n);
        while (t != n - 1 && y != 1 && y != n - 1) {
            y = y * y % n;
            t <<= 1;
        }
        if (y != n - 1 && t % 2 == 0) {
            return 0;
        }
    }
    return 1;
}
template <int n> constexpr bool is_prime = is_prime_constexpr(n);

constexpr std::pair<int64_t, int64_t> inv_gcd(int64_t a, int64_t b) {
    a = safe_mod(a, b);
    if (a == 0) return {b, 0};
    int64_t s = b, t = a;
    int64_t m0 = 0, m1 = 1;

    while (t) {
        int64_t u = s / t;
        s -= t * u;
        m0 -= m1 * u;  // |m1 * u| <= |m1| * s <= b
        auto tmp = s;
        s = t;
        t = tmp;
        tmp = m0;
        m0 = m1;
        m1 = tmp;
    }
    if (m0 < 0) m0 += b / s;
    return {s, m0};
}

constexpr int primitive_root_constexpr(int m) {
    if (m == 2) return 1;
    if (m == 167772161) return 3;
    if (m == 469762049) return 3;
    if (m == 754974721) return 11;
    if (m == 1e9 + 7) return 3;
    int divs[20] = { };
    divs[0] = 2LL;
    int cnt = 1LL;
    int x = (m - 1) / 2LL;
    while (x % 2 == 0) x /= 2LL;
    for (int i = 3; (int64_t)(i) * i <= x; i += 2LL) {
        if (x % i == 0) {
            divs[cnt++] = i;
            while (x % i == 0) { x /= i; }
        }
    }
    if (x > 1) { divs[cnt++] = x; }
    for (int g = 2; ; g++) {
        bool ok = 1;
        for (int i = 0; i < cnt; i++) {
            if (pow_mod(g, (m - 1) / divs[i], m) == 1) {
                ok = 0; break;
            }
        }
        if (ok) return g;
    }
}
template <int m> constexpr int primitive_root = primitive_root_constexpr(m);

template <class T> struct is_signed_int : std::integral_constant<bool, 
                                          std::is_integral<T>::value 
                                       && std::is_signed<T>::value> { };

template <class T> struct is_unsigned_int : std::integral_constant<bool, 
                                            std::is_integral<T>::value 
                                         && std::is_unsigned<T>::value> { };

template <class T> using is_signed_int_t = std::enable_if_t<is_signed_int<T>::value>;

template <class T> using is_unsigned_int_t = std::enable_if_t<is_unsigned_int<T>::value>;

struct modint_base { };

struct static_modint_base : modint_base { };

template <class T> using is_modint = std::is_base_of<modint_base, T>;

template <class T> using is_modint_t = std::enable_if_t<is_modint<T>::value>;

template <int m, std::enable_if_t<(1 <= m)>* = nullptr>
struct static_modint : static_modint_base {
    using mint = static_modint;
  public:
    static constexpr int mod() { return m; }
    static mint raw(int v) {
        mint x;
        x._v = v;
        return x;
    }
    static_modint() : _v(0) { }
    template <class T, is_signed_int_t<T>* = nullptr>
    static_modint(T v) {
        int64_t x = (int64_t)(v % (int64_t)(umod()));
        if (x < 0) x += umod();
        _v = (unsigned int)(x);
    }
    unsigned int val() const { return _v; }

    friend std::ostream& operator<<(std::ostream& os, const mint& x) {
        return os << x.val();
    }
    friend std::istream& operator>>(std::istream& is, mint& x) {
        int64_t v; is >> v;
        x = mint(v);
        return is;
    }
    mint& operator++() {
        _v++;
        if (_v == umod()) _v = 0;
        return *this;
    }
    mint& operator--() {
        if (_v == 0) _v = umod();
        _v--;
        return *this;
    }
    mint operator++(signed) {
        mint result = *this;
        ++*this;
        return result;
    }
    mint operator--(signed) {
        mint result = *this;
        --*this;
        return result;
    }
    mint& operator+=(const mint& r) {
        _v += r._v;
        if (_v >= umod()) _v -= umod();
        return *this;
    }
    mint& operator-=(const mint& r) {
        _v += umod() - r._v;
        if (_v >= umod()) _v -= umod();
        return *this;
    }
    mint& operator*=(const mint& r) {
        uint64_t z = _v;
        z *= r._v;
        _v = (unsigned int)(z % umod());
        return *this;
    }
    mint& operator/=(const mint& r) { return *this = *this * r.inv(); }

    mint operator+() const { return *this; }
    mint operator-() const { return mint() - *this; }

    mint pow(int64_t n) const {
        assert(0 <= n);
        mint x = *this, r = 1;
        while (n) {
            if (n & 1) r *= x;
            x *= x;
            n >>= 1;
        }
        return r;
    }
    mint inv() const {
        if (prime) {
            assert(_v);
            return pow(umod() - 2);
        } else {
            auto eg = inv_gcd(_v, m);
            assert(eg.first == 1);
            return eg.second;
        }
    }
    explicit operator int64_t() const noexcept { 
        return static_cast<int64_t>(_v); 
    }
    explicit operator int32_t() const noexcept { 
        return static_cast<int32_t>(_v); 
    }
    explicit operator uint64_t() const noexcept { 
        return static_cast<int64_t>(_v); 
    }
    explicit operator uint32_t() const noexcept { 
        return static_cast<int32_t>(_v); 
    }
    friend mint operator+(const mint& l, const mint& r) { 
        return mint(l) += r; 
    }
    friend mint operator-(const mint& l, const mint& r) { 
        return mint(l) -= r; 
    }
    friend mint operator*(const mint& l, const mint& r) { 
        return mint(l) *= r; 
    }
    friend mint operator/(const mint& l, const mint& r) { 
        return mint(l) /= r; 
    }
    friend bool operator==(const mint& l, const mint& r) { 
        return l._v == r._v; 
    }
    friend bool operator!=(const mint& l, const mint& r) { 
        return l._v != r._v; 
    }
    void swap(mint& other) noexcept { std::swap(_v, other._v); }
  private:
    unsigned int _v;
    static constexpr unsigned int umod() { return m; }
    static constexpr bool prime = is_prime<m>;
};

template <int id> struct dynamic_modint : modint_base {
    using mint = dynamic_modint;
  public:
    static int mod() { return (int)(bt.umod()); }
    static void set_mod(int m) {
        assert(1 <= m);
        bt = barrett(m);
    }
    static mint raw(int v) {
        mint x;
        x._v = v;
        return x;
    }
    dynamic_modint() : _v(0) { }
    template <class T, is_signed_int_t<T>* = nullptr>
    dynamic_modint(T v) {
        int64_t x = (int64_t)(v % (int64_t)(mod()));
        if (x < 0) x += mod();
        _v = (unsigned int)(x);
    }
    unsigned int val() const { return _v; }

    friend std::ostream& operator<<(std::ostream& os, const mint& x) {
        return os << x.val();
    }    
    friend std::istream& operator>>(std::istream& is, mint& x) {
        int64_t v; is >> v;
        x = mint(v);
        return is;
    }
    mint& operator++() {
        _v++;
        if (_v == umod()) _v = 0;
        return *this;
    }
    mint& operator--() {
        if (_v == 0) _v = umod();
        _v--;
        return *this;
    }
    mint operator++(signed) {
        mint result = *this;
        ++*this;
        return result;
    }
    mint operator--(signed) {
        mint result = *this;
        --*this;
        return result;
    }
    mint& operator+=(const mint& r) {
        _v += r._v;
        if (_v >= umod()) _v -= umod();
        return *this;
    }
    mint& operator-=(const mint& r) {
        _v += umod() - r._v;
        if (_v >= umod()) _v -= umod();
        return *this;
    }
    mint& operator*=(const mint& r) {
        _v = bt.mul(_v, r._v);
        return *this;
    }
    mint& operator/=(const mint& r) { return *this = *this * r.inv(); }
    mint operator+() const { return *this; }
    mint operator-() const { return mint() - *this; }
    mint pow(long long n) const {
        assert(0 <= n);
        mint x = *this, r = 1;
        while (n) {
            if (n & 1) r *= x;
            x *= x;
            n >>= 1;
        }
        return r;
    }
    mint inv() const {
        auto eg = inv_gcd(_v, mod());
        assert(eg.first == 1);
        return eg.second;
    }
    explicit operator int64_t() const noexcept { 
        return static_cast<int64_t>(_v); 
    }
    explicit operator int32_t() const noexcept { 
        return static_cast<int32_t>(_v); 
    }
    explicit operator uint64_t() const noexcept { 
        return static_cast<int64_t>(_v); 
    }
    explicit operator uint32_t() const noexcept { 
        return static_cast<int32_t>(_v); 
    }
    friend mint operator+(const mint& l, const mint& r) { 
        return mint(l) += r;
    }
    friend mint operator-(const mint& l, const mint& r) { 
        return mint(l) -= r;
    }
    friend mint operator*(const mint& l, const mint& r) { 
        return mint(l) *= r;
    }
    friend mint operator/(const mint& l, const mint& r) { 
        return mint(l) /= r;
    }
    friend bool operator==(const mint& l, const mint& r) { 
        return l._v == r._v; 
    }
    friend bool operator!=(const mint& l, const mint& r) { 
        return l._v != r._v; 
    }
    void swap(mint& other) noexcept { std::swap(_v, other._v); }
  private:
    unsigned int _v;
    static barrett bt;
    static unsigned int umod() { return bt.umod(); }
};
template <int id> barrett dynamic_modint<id>::bt = barrett((uint32_t)::mod);

using Dmint = dynamic_modint<-1>;
using mint = static_modint<mod>;

```
