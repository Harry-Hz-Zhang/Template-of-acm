---
topic: "模板"
category: "05-polynomial"
source: "多项式 Polynomial.md"
---

# 模板

```C++
int qpow(int a, int k) {
    i64 res = 1 % mod;
    while(k) {
        if (k & 1) res = (i64)res * a % mod;
        a = (i64)a * a % mod;
        k >>= 1;
    }
    return res;
}
int inv(int x) {
    return qpow(x, mod - 2);
}

// 寻找模 mod 的一个原始根 i
int findPrimitiveRoot(i64 mod) {
    int i = 2;
    int k = __builtin_ctz(mod - 1);
    while (true) {
        if (qpow(i, (mod - 1) / 2) != 1) {
            break;
        }
        i += 1;
    }
    return qpow(i, (mod - 1) >> k);
}
int primitiveRoot;
vector<int> rev, roots{0, 1};

// NTT 变换（离散傅里叶变换）
void dft(vector<int>& a) {
    int n = a.size();
    if (rev.size() != n) {
        int k = __builtin_ctz(n) - 1;
        rev.resize(n);
        for (int i = 0; i <= n - 1; i++) {
            rev[i] = rev[i >> 1] >> 1 | (i & 1) << k;
        }
    }
    for (int i = 0; i < n; i++) {
        if (rev[i] < i) swap(a[i], a[rev[i]]);
    }
    if (roots.size() < n) {
        int k = __builtin_ctz(roots.size());
        roots.resize(n);
        while((1 << k) < n) {
            int e = qpow(primitiveRoot, (mod - 1) >> (k + 1));
            for (int i = 1 << (k - 1); i < (1 << k); i++) {
                roots[2 * i] = roots[i];
                roots[2 * i + 1] = roots[i] * e % mod;
            }
            k++;
        }
    }
    for (int k = 1; k < n; k *= 2) {
        for (int i = 0; i < n; i += 2 * k) {
            for (int j = 0; j < k; j++) {
                int u = a[i + j] % mod;
                int v = a[i + j + k] * roots[k + j] % mod;
                a[i + j] = (u + v) % mod;
                a[i + j + k] = (u - v + mod) % mod;
            }
        }
    }
}
void idft(vector<int> &a) {
    int n = a.size();
    reverse(a.begin() + 1, a.end());
    dft(a);
    int invf = inv(n);
    for (int i = 0; i < n; i++) a[i] = a[i] * invf % mod;
}

class Poly: public vector<int> {
    public:
    Poly() { }
    Poly(int n): vector<int>(n) { }
    Poly(const vector<int> &a): vector<int>(a) { }
    Poly(std::initializer_list<int> _init): vector<int> (_init) { }
    Poly(int n, int a): vector<int>(n, a) { }

    // 移位：乘 x^k 或除 x^(-k)
    Poly shift(int k) const {
        if (k >= 0) {   // 多项式乘以 x^k
            auto b = *this;
            b.insert(b.begin(), k, 0);
            return b;
        } else if (this->size() <= -k) {  // 多项式除以 x^k
            return Poly();
        } else {        // 多项式除以 x^k
            return Poly(vector<int>(this->begin() + (-k), this->end()));
        }
    }

    // 保留低 k 次，多余舍弃或补 0
    Poly trunc(int k) const {   // 保留前 k 项系数
        Poly f = *this;
        f.resize(k);
        return f;
    }
    friend Poly operator+(const Poly &a, const Poly &b) {
        Poly res((int)max(a.size(), b.size()), 0);
        for (int i = 0; i < a.size(); i++) {
            (res[i] += a[i]) %= mod;
        }
        for (int i = 0; i < b.size(); i++) {
            (res[i] += b[i]) %= mod;
        }
        return res;
    }
    friend Poly operator- (const Poly a, const Poly &b) {
        Poly res(std::max(a.size(), b.size()), 0);
        for (int i = 0; i < a.size(); i++) {
            (res[i] += a[i]) %= mod;
        }
        for (int i = 0; i < b.size(); i++) {
            ((res[i] -= b[i]) += mod) %= mod;
        }
        return res;
    }

    friend Poly operator* (Poly a, Poly b) {
        if (a.size() == 0 || b.size() == 0) {
            return Poly();
        }
        if (a.size() < b.size()) {
            std::swap(a, b);
        }
        int n = 1, tot = a.size() + b.size() - 1;
        while (n < tot) {
            n *= 2;
        }
        if (((mod - 1) & (n - 1)) != 0 || b.size() < 128) {
            Poly c(a.size() + b.size() - 1, 0);
            for (int i = 0; i < a.size(); i++) {
                for (int j = 0; j < b.size(); j++) {
                    (c[i + j] += a[i] * b[j] % mod) %= mod;
                }
            }
            return c;
        }
        a.resize(n); b.resize(n);
        dft(a); dft(b);
        for (int i = 0; i < n; ++i) {
            (a[i] *= b[i]) %= mod;
        }
        idft(a); a.resize(tot);
        return a;
    }

    friend Poly operator*(Poly a, int b) {
        for (int i = 0; i < a.size(); i++) {
            (a[i] *= b % mod) %= mod;
        }
        return a;
    }

    // 多项式除法：商与余式
    friend pair<Poly, Poly> operator/ (Poly a, Poly b) {
        int deg = a.size() - b.size() + 1;
        if (deg <= 0) return {Poly(), a};
        reverse(a.begin(), a.end()); reverse(b.begin(), b.end());
        Poly q = (a * b.inverse(deg)).trunc(deg);
        reverse(q.begin(), q.end());
        reverse(a.begin(), a.end());
        reverse(b.begin(), b.end());
        Poly r = (a - b * q).trunc(b.size() - 1);   // 用正常顺序a、b算余数
        return {q, r};
    }

    Poly &operator+= (Poly b) {
        return (*this) = (*this) + b;
    }
    Poly &operator-= (Poly b) {
        return (*this) = (*this) - b;
    }
    Poly &operator*= (Poly b) {
        return (*this) = (*this) * b;
    }

    // 导数 f'
    Poly deriv() const {
        if (this->empty()) {
            return Poly();
        }
        Poly res(this->size() - 1);
        for (int i = 0; i < this->size() - 1; ++i) {
            res[i] = (i + 1) * (*this)[i + 1] % mod;
        }
        return res;
    }

    // 不定积分 ∫f dx
    Poly integr() const {
        Poly res(this->size() + 1);
        for (int i = 0; i < this->size(); ++i) {
            res[i + 1] = (*this)[i] * inv(i + 1) % mod;
        }
        return res;
    }

    // 求逆元 f^{-1} mod x^m
    Poly inverse(int m) const {
        Poly x { inv((*this)[0]) };
        int k = 1;
        while (k < m) {
            k *= 2;
            x = (x * (Poly{2} - trunc(k) * x)).trunc(k);
        }
        return x.trunc(m);
    }

    Poly log(int m) const {
        return (deriv() * inverse(m)).integr().trunc(m);
    }

    // 指数 exp f, 需 f[0] = 0
	Poly exp(int m) const {
		Poly x{1};
		int k = 1;
		while (k < m) {
			k *= 2;
			x = (x * (Poly{1} - x.log(k) + trunc(k))).trunc(k);
		}
		return x.trunc(m);
	}
	// 幂运算 f^k
    Poly pow(int k) const {
        if (k == 0) return Poly(1, 1);
        int last = this->size() - 1;

        while (last >= 0 && (*this)[last] == 0) last--;
        if (last < 0) { return Poly(); }
        i64 want = 1LL * last * k + 1;
        const i64 hh = 1LL << 20;
        int cap = min(want, hh);

        Poly base = this->trunc(cap);
        for (int &x : base) x = x ? 1 : 0;
        while (!base.empty() && base.back() == 0) base.pop_back();
        Poly res(1, 1);
        int K = k;
        while (K > 0) {
            if (K & 1) {
                res = res * base;
                if ((int)res.size() > cap) res.resize(cap);
                for (int &x : res) x = x ? 1 : 0;
                while (!res.empty() && res.back() == 0) res.pop_back();
            }
            K >>= 1;
            if (K) {
                base = base * base;
                if ((int)base.size() > cap) base.resize(cap);
                for (int &x : base) x = x ? 1 : 0;
                while (!base.empty() && base.back() == 0) base.pop_back();
            }
        }
        return res;
    }
    // 开方 sqrt(f), 需 f[0] = 1
	Poly sqrt(int m) const {
		Poly x{1};
		int k = 1;
		while (k < m) {
			k *= 2;
			x = (x + (trunc(k) * x.inverse(k)).trunc(k)) * inv(2);
		}
		return x.trunc(m);
	}
    Poly mulT(Poly b) const {
        if (b.size() == 0) {
            return Poly();
        }
        int n = b.size();
        reverse(b.begin(), b.end());
        return ((*this) * b).shift(-(n - 1));
    }

    // 多点求值: eval at x[0..sz)
    vector<int> eval(vector<int> x) const {
        if (this->empty()) {
            return vector<int>(x.size(), 0);
        }
        const int n = max(x.size(), this->size());
        vector<Poly> q(4 * n);
        vector<int> ans(x.size());
        x.resize(n);
        function<void(int, int, int)> build = [&](int p, int l, int r) {
            if (r - l == 1) {
                q[p] = Poly{1, -x[l]};
            } else {
                int m = l + r >> 1;
                build(p << 1, l, m);
                build(p << 1 | 1, m, r);
                q[p] = q[p << 1] * q[p << 1 | 1];
            }
        };
        build(1, 0, n);
        function<void(int, int, int, const Poly &)> dfs = [&](int p, int l, int r, const Poly &num) {
            if (r - l == 1) {
                if (l < ans.size()) ans[l] = num[0];
            } else {
                int m = l + r >> 1;
                dfs(p << 1, l, m, num.mulT(q[p << 1 | 1]).trunc(m - l));
                dfs(p << 1 | 1, m, r, num.mulT(q[p << 1]).trunc(r - m));
            }
        };
        dfs(1, 0, n, this->mulT(q[1].inverse(n)));
        return ans;
    }
};
// solve() 中 
void solve() {
    primitiveRoot = findPrimitiveRoot(mod);
}
```
***
