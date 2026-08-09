---
topic: "高精度 BigInt"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 高精度 BigInt

```C++
struct big_int {
  public:
    static const int base = 1000;
    static const int base_digits = 3;
    vector<int> a;
    int sign = 1;
    big_int() = default;
    big_int(i64 v) { *this = v; }

    big_int& operator=(i64 v) {
        sign = 1; a.clear();
        if (v < 0) { sign = -1; v = -v; }
        for (; v > 0; v /= base) a.push_back(v % base);
        return *this;
    }

    big_int(const string &s) { read(s); }

    void read(const string &s) {
        sign = 1; a.clear();
        int pos = 0;
        while (pos < (int)s.size() && (s[pos] == '-' || s[pos] == '+')) {
            if (s[pos] == '-') sign = -sign;
            ++pos;
        }
        for (int i = (int)s.size() - 1; i >= pos; i -= base_digits) {
            int x = 0;
            for (int j = max(pos, i - base_digits + 1); j <= i; ++j)
                x = x * 10 + (s[j] - '0');
            a.push_back(x);
        }
        trim();
    }

    friend ostream& operator<<(ostream &os, const big_int &v) {
        if (v.sign == -1 && !v.is_zero()) os << '-';
        if (v.a.empty()) return os << '0';
        os << v.a.back();
        for (int i = (int)v.a.size() - 2; i >= 0; --i)
            os << setw(base_digits) << setfill('0') << v.a[i];
        return os;
    }
    friend istream& operator>>(istream &is, big_int &v) {
        string s; if (!(is >> s)) return is; v.read(s); return is;
    }

    string to_string() {
        stringstream oss;
        oss << *this;
        return oss.str();
    }

    bool is_zero() const { return a.empty() || (a.size() == 1 && a[0] == 0); }

    void trim() {
        while (!a.empty() && a.back() == 0) a.pop_back();
        if (a.empty()) sign = 1;
    }

    static int abs_compare(const big_int &A, const big_int &B) {
        if (A.a.size() != B.a.size()) return A.a.size() < B.a.size() ? -1 : 1;
        for (int i = (int)A.a.size() - 1; i >= 0; --i)
            if (A.a[i] != B.a[i]) return A.a[i] < B.a[i] ? -1 : 1;
        return 0;
    }

    friend bool operator<(const big_int &A, const big_int &B) {
        if (A.sign != B.sign) return A.sign < B.sign;
        int cmp = abs_compare(A, B);
        return A.sign == 1 ? (cmp < 0) : (cmp > 0);
    }
    friend bool operator==(const big_int &A, const big_int &B) {
        return A.sign == B.sign && A.a == B.a;
    }
    friend bool operator!=(const big_int &A, const big_int &B) { return !(A == B); }
    friend bool operator>(const big_int &A, const big_int &B) { return B < A; }
    friend bool operator<=(const big_int &A, const big_int &B) { return !(B < A); }
    friend bool operator>=(const big_int &A, const big_int &B) { return !(A < B); }

    friend big_int operator+(big_int A, const big_int &B) {
        if (A.sign == B.sign) {
            int carry = 0;
            for (size_t i = 0; i < max(A.a.size(), B.a.size()) || carry; ++i) {
                if (i == A.a.size()) A.a.push_back(0);
                A.a[i] += carry + (i < B.a.size() ? B.a[i] : 0);
                carry = A.a[i] >= base;
                if (carry) A.a[i] -= base;
            }
            return A;
        }
        return A - (-B);
    }
    big_int operator+= (const big_int &B) {
        return *this = *this + B;
    }
    friend big_int operator-(big_int A) { A.sign = -A.sign; return A; }
    friend big_int operator-(big_int A, const big_int &B) {
        if (B.is_zero()) return A;
        if (A.sign == B.sign) {
            if (abs_compare(A, B) >= 0) {
                int carry = 0;
                for (size_t i = 0; i < B.a.size() || carry; ++i) {
                    A.a[i] -= carry + (i < B.a.size() ? B.a[i] : 0);
                    carry = A.a[i] < 0;
                    if (carry) A.a[i] += base;
                }
                A.trim();
                return A;
            }
            big_int C = B - A;
            C.sign = -C.sign;
            return C;
        }
        return A + (-B);
    }
    big_int operator-= (const big_int &B) {
        return *this = *this - B;
    }

    big_int& operator++() {
        *this = *this + 1; // uses implicit big_int(i64) conversion for '1'
        return *this;
    }
    big_int operator++(int32_t) {
        big_int old = *this;
        *this = *this + 1;
        return old;
    }

    big_int& operator--() {
        *this = *this - 1; 
        return *this;
    }
    big_int operator--(int32_t) {
        big_int old = *this;
        *this = *this - 1;
        return old;
    }

    // FFT-based multiplication (complex<double>)
    friend big_int operator*(const big_int &A, const big_int &B) {
        big_int res;
        if (A.is_zero() || B.is_zero()) {
            res = 0;
            return res;
        }
        res.sign = A.sign * B.sign;

        vector<double> fa(A.a.begin(), A.a.end()), fb(B.a.begin(), B.a.end());
        size_t n = 1;
        while (n < fa.size() + fb.size()) n <<= 1;

        vector<complex<double>> Afft(n), Bfft(n);
        for (size_t i = 0; i < fa.size(); ++i) Afft[i] = complex<double>(fa[i], 0);
        for (size_t i = 0; i < fb.size(); ++i) Bfft[i] = complex<double>(fb[i], 0);

        const double PI = acos(-1.0);
        auto fft = [&](vector<complex<double>> &a, bool invert) {
            size_t n = a.size();
            for (size_t i = 1, j = 0; i < n; ++i) {
                size_t bit = n >> 1;
                for (; j & bit; bit >>= 1) j ^= bit;
                j ^= bit;
                if (i < j) swap(a[i], a[j]);
            }
            for (size_t len = 2; len <= n; len <<= 1) {
                double ang = 2 * PI / len * (invert ? -1 : 1);
                complex<double> wlen(cos(ang), sin(ang));
                for (size_t i = 0; i < n; i += len) {
                    complex<double> w(1);
                    for (size_t j = 0; j < len/2; ++j) {
                        complex<double> u = a[i+j];
                        complex<double> v = a[i+j+len/2] * w;
                        a[i+j] = u + v;
                        a[i+j+len/2] = u - v;
                        w *= wlen;
                    }
                }
            }
            if (invert) for (size_t i = 0; i < n; ++i) a[i] /= (double)n;
        };

        fft(Afft, false);
        fft(Bfft, false);
        for (size_t i = 0; i < n; ++i) Afft[i] *= Bfft[i];
        fft(Afft, true);

        res.a.assign(n, 0);
        i64 carry = 0;
        for (size_t i = 0; i < n; ++i) {
            i64 t = (i64) llround(Afft[i].real()) + carry;
            res.a[i] = (int)(t % base);
            carry = t / base;
        }
        while (carry > 0) {
            res.a.push_back((int)(carry % base));
            carry /= base;
        }
        res.trim();
        return res;
    }
    big_int operator*= (const big_int &B) {
        return *this = *this * B;
    }

    // multiply by small int (0 <= m < 1e9), returns product
    friend big_int mul_short(const big_int &v, int m) {
        if (m == 0 || v.is_zero()) return big_int(0);
        big_int res; res.sign = v.sign * (m<0 ? -1 : 1);
        i64 mm = m < 0 ? -1LL*m : m;
        res.a.assign(v.a.size(), 0);
        i64 carry = 0;
        for (size_t i = 0; i < v.a.size(); ++i) {
            i64 cur = 1LL * v.a[i] * mm + carry;
            res.a[i] = (int)(cur % base);
            carry = cur / base;
        }
        while (carry > 0) {
            res.a.push_back((int)(carry % base));
            carry /= base;
        }
        res.trim();
        return res;
    }

    // divide by small positive int -> returns quotient (trunc toward zero)
    friend big_int div_short(const big_int &v, int m) {
        big_int res; res.sign = v.sign * (m<0 ? -1 : 1);
        i64 mm = m < 0 ? -1LL*m : m;
        res.a.assign(v.a.size(), 0);
        i64 carry = 0;
        for (int i = (int)v.a.size() - 1; i >= 0; --i) {
            i64 cur = v.a[i] + carry * (i64)base;
            res.a[i] = (int)(cur / mm);
            carry = cur % mm;
        }
        res.trim();
        return res;
    }

    // absolute value
    big_int abs() const { big_int t = *this; t.sign = 1; return t; }

    // compare absolute values
    static bool abs_less(const big_int &A, const big_int &B) { return abs_compare(A,B) < 0; }

    // shift right (插入低位0)，用于长除
    void shift_right() { if (a.empty()) a.push_back(0); a.insert(a.begin(), 0); }

    // long division: returns {quotient, remainder}, division trunc toward zero (like C++)
    friend pair<big_int, big_int> divmod(const big_int &a1, const big_int &b1) {
        if (b1.is_zero()) throw runtime_error("Division by zero");

        big_int a = a1.abs();
        big_int b = b1.abs();
        if (abs_compare(a, b) < 0) {
            big_int q = 0;
            big_int r = a1;
            r.sign = a1.sign;
            return {q, r};
        }

        int f = base / (b.a.back() + 1);
        big_int an = mul_short(a, f); // a * f
        big_int bn = mul_short(b, f); // b * f
        big_int q; q.a.assign(an.a.size(), 0);
        big_int r; r = 0;
        for (int i = (int)an.a.size() - 1; i >= 0; --i) {
            r.shift_right();
            r.a[0] = an.a[i];
            r.trim();
            i64 qt = 0;
            if (r.a.size() >= bn.a.size()) {
                i64 r_hi = (i64) ( r.a.size() > bn.a.size() ? r.a[bn.a.size()] : 0 );
                i64 r_lo = (i64) r.a[bn.a.size() - 1];
                i64 b_hi = (i64) bn.a.back();
                qt = ( (r_hi * base) + r_lo ) / b_hi;
                if (qt >= base) qt = base - 1;
            } else qt = 0;
            big_int t = mul_short(bn, (int)qt);
            while (abs_compare(r, t) < 0) {
                --qt;
                t = mul_short(bn, (int)qt);
            }
            r = r - t;
            q.a[i] = (int)qt;
        }
        q.sign = a1.sign * b1.sign;
        r.sign = a1.sign;
        q.trim();
        r.trim();
        r = div_short(r, f);
        return {q, r};
    }
    friend big_int operator/ (const big_int &A, const big_int &B) {
        return divmod(A,B).first;
    }
    big_int operator/= (const big_int &B) {
        return *this = *this / B;
    }
    friend big_int operator% (const big_int &A, const big_int &B) {
        return divmod(A,B).second;
    }
    big_int operator%= (const big_int &B) {
        return *this = *this % B;
    }
};
static big_int big_INF() {
    string s(10000, '9');
    return big_int(s);
}

#define int big_int
void solve() {
    int A, B, C, X, Y, D;
    cin >> A >> B >> C >> X >> Y >> D;
    int ans = big_INF();

    int res1 = 0; {
        res1 = A;
        if (D >= X) res1 += (D - X) * B;
        if (D >= X + Y) res1 += (C - B) * (D - (X + Y));
    }
    ans = min(ans, res1);

    if (D <= X) {
        cout << ans << endl;
        return;
    }

    if (D >= X + Y) {
        int T = X + Y;
        int res2 = (D / T) * (A + B * Y) + C * (D % T);
        ans = min(ans, res2);
    } 

    int res3 = 0; {
        res3 = ((D + (X - 1)) / X) * A;
    }
    ans = min(ans, res3);

    int res4 = 0; {
        int k = (D + X + Y - 1) / (X + Y);
        int rem = max(big_int(0), D - k * (X));
        res4 = k * A + rem * B;
    }
    ans = min(ans, res4);

    int res5 = 0; {
        int k = D / X, t = D % X;
        if (k * Y >= t) {
            res5 = k * A + t * B;
        } else {
            res5 = k * A + k * B * Y + (D - k * (X + Y)) * C;
        }
    }
    ans = min(ans, res5);

    int res6 = 0; {
        int k = D / X, t = D % X;
        if (t >= Y) {
            res6 = k * A + Y * B + (D - k * X - Y) * C;
            ans = min(ans, res6);
        }
    }   
    cout << ans << endl;
}
#undef int big_int
```
