---
topic: "拼接问题经典的例题："
category: "06-geometry"
source: "几何 Geometry.md"
---

# 拼接问题经典的例题：


判定给定的两个简单多边形 $P_1, P_2$ 是否能通过特定的**等距变换**，拼合成一个**轴对齐矩形**，且满足**一刀切**（直线分割）条件。

- **目标图形**：必须是矩形，且边平行于坐标轴。

- **分割方式**：必须是**一刀切**。这意味着两个多边形的公共边界必须是**一条唯一的直线段**。

- **允许变换**：

    - 平移 (Translation)

    - 旋转 (90°, 180°, 270°)

    - 镜像翻转 (Mirror Flip)

    - _注：每个多边形有 8 种可能的朝向（4个旋转角 × 是否翻转）。_

- **拼接要求**：

    - 无重叠、无遗漏（并集为矩形，交集仅为边界）。

    - 面积守恒：$S_{P1} + S_{P2} = S_{Rectangle}$。


* **数据规模：

- 多边形顶点数 $k$：$3 \le k \le 10$（非常小，暗示可以穷举或进行复杂几何分析）。
- 坐标范围：$0$ 到 $10^8$
- 测试案例 $N$：$1 \le N \le 16$。

```cpp
#include <bits/stdc++.h>
#pragma GCC optimize("O3")
#pragma GCC optimize("unroll-loops")
#pragma GCC target("avx2,bmi,bmi2,lzcnt,popcnt")
using namespace std;

template <class F>
struct Y_combinator {
    F f;
    Y_combinator(F f_) : f(std::move(f_)) {}
    template <class... Args>
    decltype(auto) operator()(Args&&... args) {
        return f(*this, std::forward<Args>(args)...);
    }
};
template <class F> Y_combinator(F) -> Y_combinator<F>;

ostream& operator<<(ostream &os, const __int128_t &x) {
    if (x == 0) return os << "0";
    __int128_t tmp = x; string s;
    bool neg = 0;
    if (tmp < 0) { neg = true; tmp = -tmp; }
    while (tmp > 0) {
        s.push_back('0' + (tmp % 10));
        tmp /= 10;
    }
    if (neg) s.push_back('-');
    reverse(s.begin(), s.end());
    return os << s;
}
#if __cplusplus >= 202000
template <class T> requires (ranges::contiguous_range<T> && !is_same_v<remove_cvref_t<T>, string>)
istream& operator>>(istream &in, T &c) {
    for (int i = 1; i < c.size(); i++) { in >> c[i]; }
    return in;
}
#endif
int T_ = 1;
#if __cplusplus >= 202000 and !defined(ONLINE_JUDGE)
template<typename T> ostream& operator<<(ostream& os, const vector<T>& v) 
{ os<<'['; for (size_t i = 0; i < v.size(); i++) os << (i ? ", " : "") << v[i]; return os << ']'; }
static vector<string> splitN(const string&s) { vector<string> res; int d = 0; size_t st = 0;
    for(size_t i = 0; i <= s.size(); i++) { char ch = i == s.size() ? ',' : s[i];
        if (ch == '(' || ch == '{' || ch == '[') ++d;
        else if (ch == ')' || ch == '}' || ch == ']') --d;
        if (ch == ',' && d == 0) { size_t l = st; while(l < s.size() && isspace((unsigned char)s[l])) ++l;
            size_t r = i; while(r > l && isspace((unsigned char) s[r - 1])) --r;
            res.emplace_back(s.substr(l, r - l)); st = i + 1;
        }
    } return res; }
template<class...Args>
void debug_Hz(int tc, int line, const string& names, const Args&...args) {
auto nms = splitN(names); cerr << "T" << T_ << " L" << line << ": {"; int idx = 0LL;
    ((cerr << (idx < (int)nms.size() ? nms[idx] : to_string(idx)) << " = " << args << (++idx < (int)sizeof...(Args) ? ", " : "}\n")), ...);
}
#define debug(...) debug_Hz(T_,__LINE__,#__VA_ARGS__,__VA_ARGS__)
#else
#define debug(...) ((void)0)
#endif

using i64 = int64_t;
using u64 = uint64_t;
using i32 = int32_t;
using i128 = __int128_t;
#define range(a) std::begin(a), std::end(a)
#define range_(a) std::next(std::begin(a)), std::end(a)
#define int long long

typedef pair<int, int> pii;

const i64 N = 2e5 + 10, INF = 1LL << 61;
const i64 mod = 998244353;

// 少用显式构造 可能TLE  sqrt 很慢，少用  积分可能很慢
constexpr long double inf = 1e100L;
#define double long double
const double PI = acosl(-1LL);
constexpr double eps = 1e-10;

int sign(double x) {
    if (fabsl(x) < eps) return 0;
    else return x > 0 ? 1 : -1;
}
int sign(double x, double y) {
    if (fabsl(x - y) < eps) return 0;
    else return x > y ? 1 : -1;
}
template<typename T = double>
struct Vector {
  public:
    T x, y;
    inline Vector(T x_ = (T)inf, T y_ = (T)inf): x(x_), y(y_) { }

    template<typename U>
    operator Vector<U>() { return Vector<U>(U(x), U(y)); }
    inline Vector &operator+= (Vector p) & { x += p.x; y += p.y; return *this; }
    inline Vector &operator-= (Vector p) & { x -= p.x; y -= p.y; return *this; }
    inline Vector &operator*= (T v) & { x *= v; y *= v; return *this; }
    inline Vector &operator/= (T v) & { x /= v; y /= v; return *this; }
    inline Vector operator-() const { return Vector(-x, -y); }
    inline friend Vector operator+ (Vector a, Vector b) { return a += b; }
    inline friend Vector operator- (Vector a, Vector b) { return a -= b; }
    inline friend Vector operator* (Vector a, T b) { return a *= b; }
    inline friend Vector operator* (T a, Vector b) { return b *= a; }
    inline friend Vector operator/ (Vector a, T b) { return a /= b; }
    inline double square() { return (*this) * (*this); }
    inline double length() { return std::sqrt(square()); }
    // |a| * |b| * sin(th)
    inline double operator^ (Vector t) const { return x * t.y - y * t.x; }
    // |a| * |b| * cos(th)
    inline double operator* (Vector t) const { return x * t.x + y * t.y; }
    // CCW -> [0, 2PI)
    inline double polar_angle() { double res = atan2((double)y, (double)x); if (sign(res) < 0) res += PI * 2; return res;}
    inline bool operator== (const Vector &t) const { return sign(x, t.x) == 0 && sign(y, t.y) == 0; }
    inline bool operator!= (const Vector &t) const { return !(*this == t); }
    inline bool operator< (const Vector& t) const { return sign(x, t.x) == 0 ? y < t.y : x < t.x; }
    friend std::istream &operator>>(std::istream &is, Vector &p) { return is >> p.x >> p.y; }
    friend std::ostream &operator<< (std::ostream &out, const Vector p) { return out << '(' << p.x << ", " << p.y << ')'; }
    inline void read() {
        i64 x_, y_; 
        cin >> x_ >> y_;
        x = (double)x_, y = (double)y_;
    }
};

template<typename T = double> using Point = Vector<T>;

template<typename T = double>
struct Polygon: vector<Point<T>> {
    using vector<Point<T>>::vector; // 继承构造器
    Polygon() { }
    Polygon(initializer_list<Point<T>> arg): vector<Point<T>>(arg) {}
    template<typename... argT>
    explicit Polygon(argT &&...args): vector<Point<T>>(forward<argT>(args)...) { }

    inline Point<T> mid_point() const {
        int n = (int)this->size();
        double X = 0, Y = 0;
        if (n == 0) return Point<T>(0, 0); 
        for (int i = 0; i < n; i++) {
            X += (*this)[i].x;
            Y += (*this)[i].y;
        }
        return Point(X / n, Y / n);
    }
    
    inline double perimeter() const {
        int n = (int)this->size();
        double ans = 0;
        for (int i = 0; i < n; i++) {
            ans += dist((*this)[i], (*this)[(i + 1) % n]);
        }
        return ans;
    }

    inline double signed_area_x2() const {
        int n = (int)this->size();
        if (n < 3) return 0;
        double ans = 0;
        for (int i = 0; i < n; i++) {
            ans += (*this)[i] ^ (*this)[(i + 1) % n];
        }
        return ans;
    }
    inline double signed_area() const {
        return signed_area_x2() / 2.0L;
    }
    inline double area() const {
        return fabsl(signed_area_x2()) / 2.0L;
    }
    inline bool is_ccw() const {
        return sign(signed_area_x2()) > 0;
    }
    // 转换为逆时针顺序
    inline void make_ccw() {
        if (!is_ccw()) {
            std::reverse(this->begin(), this->end());
        }
    }
    
    inline bool is_convex() const {
        int n = (int)this->size();
        if (n < 3) return 0;
        double th = 0;
        for (int i = 0; i < n; i++) {
            int j = (i + 1) % n, k = (i + 2) % n;
            th += angle(((*this)[j] - (*this)[i]), ((*this)[k] - (*this)[j]));
        }
        return sign(th - 2 * PI) == 0;
    }

    // 0 - 不在里面
    // 1 - 边上
    // 2 - 严格在里面
    // 注意：inPolygon 热路径使用了 inline Point<T>OnSegment( p, a, b )，避免了 Line 构造
    inline int in_polygon(Point<T> &p) {
        bool f = 0;
        int n = (int)this->size();
        if (n == 0) return 0;
        Point<T> p1, p2;
        for (int i = 0, j = n - 1; i < n; j = i++) {
            p1 = (*this)[i]; p2 = (*this)[j];
            if (point_on_segment(p, p1, p2)) return 1;
            if ((sign(p1.y - p.y) > 0 != sign(p2.y - p.y) > 0) && 
                sign(p.x - (p.y - p1.y) * (p1.x - p2.x) / (p1.y - p2.y) - p1.x) < 0) {
                f = !f;
            }
        }
        return f ? 2 : 0;
    }
};

using point = Point<double>;

void solve()
{
    int n, m;
    cin >> n;
    Polygon<double> A(n);
    for (int i = 0; i < n; i++) {
        A[i].read();
    }
    cin >> m;
    Polygon<double> B(m);
    for (int i = 0; i < m; i++) {
        B[i].read();
    }

    vector<Polygon<double>> B_tran;
    for (int i = 0; i < 2; i++) {
        auto B_ = B;
        if (i == 0) {
            for (auto &p : B_) {
                p.x *= -1;
            }
        }
        for (int j = 0; j < 4; j++) {
            auto B__ = B_;
            for (auto &p : B__) {
                auto x = p.x, y = p.y;
                if (j == 0) {
                    continue;
                } else if (j == 1) {
                    p.x = -y, p.y = x;
                } else if (j == 2) {
                    p.x = -x, p.y = -y;
                } else {
                    p.x = y, p.y = -x;
                }
            }
            B_tran.push_back(B__);
        }
    }

    A.make_ccw();
    double area_A = A.area();
    for (auto B : B_tran) {
        B.make_ccw();
        for (int i = 0; i < A.size(); i++) {
            Vector<double> v1 = A[(i + 1) % n] - A[i];
            for (int j = 0; j < B.size(); j++) {
                Vector<double> v2 = B[(j + 1) % m] - B[j];
                if (v1 == -v2) {
                    double minx = INF, miny = INF, maxx = -INF, maxy = -INF;
                    // A[i] 对齐 B[j + 1]
                    Vector<double> shift = A[i] - B[(j + 1) % (B.size())];
                    for (auto p : A) {
                        minx = min(minx, p.x);
                        miny = min(miny, p.y);
                        maxx = max(maxx, p.x);
                        maxy = max(maxy, p.y); 
                    } 
                    for (auto p : B) {
                        p += shift;
                        minx = min(minx, p.x);
                        miny = min(miny, p.y);
                        maxx = max(maxx, p.x);
                        maxy = max(maxy, p.y); 
                    }

                    double area_B = B.area();
                    double AREA = (maxx - minx) * (maxy - miny);

                    if (sign(area_A + area_B, AREA) == 0) {
                        cout << "YES" << endl;
                        return;
                    }
                }
            }
        }
    }
    cout << "NO" << endl;
}

signed main()
{
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);
    std::cout.tie(0);
    int T = 1;
    cin >> T;
    for (; T_ <= T; T_++) solve();
    return 0;
}
```
