---
topic: "二维计算几何"
category: "06-geometry"
source: "几何 Geometry.md"
---

# 二维计算几何

## 算法模板

```C++
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

// 极角排序
template<typename T = double>
inline void polar_sort(vector<Point<T>> &ps) {
    sort(range(ps), [&](auto a, auto b){
        return a.polar_angle() < b.polar_angle();
    });
}

// 求向量A，B夹角
// 返回在 [0,π] 的较小角
template<typename T = double>
inline double angle(Vector<T> A, Vector<T> B) {
    A = A / A.length(), B = B / B.length();
    return acosl(min<double>(max<double>(A * B, -1), +1));
}
// 三角形面积 = ×积 / 2
template<typename T = double>
inline double area(Point<T> A, Point<T> B, Point<T> C) {
    return abs(((B - A) ^ (C - A))) / 2.0L;
}
// 距离
template<typename T = double>
inline double dist(const Point<T> A, const Point<T> B) {
    double dx = A.x - B.x, dy = A.y - B.y;
    return sqrtl(dx * dx + dy * dy);
}
// 距离^2
template<typename T = double>
inline double dist_2(const Point<T> &A, const Point<T> &B) {
	double dx = A.x - B.x, dy = A.y - B.y;
	return dx * dx + dy * dy;
}
// true：A 在 B 的左边
template<typename T = double>
inline bool left_test(Vector<T> A, Vector<T> B) { 
    return (B ^ A) > 0;
}
// 逆时针旋转 rad°
template<typename T = double>
inline Vector<T> rotate(Vector<T> A, double rad) {
    double c = cosl((double)rad), s = sinl((double)rad);
    return Vector<T>(A.x * c - A.y * s, A.x * s + A.y * c);
}
// 法向量
template<typename T = double>
Vector<T> normal_vector(Vector<T> A) {
    return Vector<T>(-A.y, A.x);
}
// sign: 上半平面或 x 正方向 / 下半平面或 x 负方向
template<typename T = double>
int sign(Point<T> a) {
    return a.y > 0 || (a.y == 0 && a.x > 0) ? 1 : -1;
}

template<typename T = double>  // 减少显示构造
struct Line {
    Point<T> a, b; // 端点
    Point<T> s; Vector<T> v; // s 起点, v 方向向量 (b - a)
    double deg;
    Line() = default;
    Line(Point<T> a_ = Point<T>(), Point<T> b_ = Point<T>()):
        a(a_), b(b_), s(a_), v(b_ - a_) {
        deg = atan2l((double)v.y, (double)v.x);
    }
};

// true ⇒ p 在直线 l 的左侧；
// false ⇒ 在右侧或共线
template<typename T = double>
inline bool point_on_line_left(const Point<T>& p, const Line<T>& l) {
    return sign((double)((l.v) ^ (p - l.s))) > 0; // 修改: 强制 double 计算以适配不同 T
}

// true ⇒ p 在线段 ab 上，含端点
template<typename T = double>
inline bool point_on_segment(const Point<T> &p, const Point<T> &a, const Point<T> &b) {
    double cr = ((p.x - a.x) * (b.y - a.y) - (p.y - a.y) * (b.x - a.x));
    if (sign(cr) != 0) return 0;
    return sign((p - a) ^ (b - a)) == 0 && sign((a - p) * (b - p)) <= 0;
}

// p 在直线 l 上的投影
template<typename T = double>
inline Vector<T> project(Point<T> p, Line<T> l) {
    double denom = l.v.square();
    if (sign(denom) == 0) return l.a; // 退化为点
    double r = ((p - l.a) * l.v) / l.v.square();
    return l.a + l.v * (T)r;
}

// p 到直线 l 的垂足
template<typename T = double>
inline Point<T> foot_point(Point<T> p, Line<T> l) {
    return project(p, l);
}

// p 关于直线 l 的对称点
template<typename T = double>
inline Point<T> reflection(const Point<T> &p, const Line<T> &l) {
    Point<T> H = foot_point<T>(p, l);
    return H * 2 - p;
}

// 直线交点（两直线不平行时）
template<typename T = double>
inline Point<T> line_intersection(const Line<T> &l1, const Line<T> &l2) {
    double denom = l1.v ^ l2.v;
    // 平行?
    if (sign(denom) == 0) return Point<T>();
    double t = ((l2.s - l1.s) ^ l2.v) / denom;
    return l1.s + l1.v * t;
}

// seg_intersection: 返回两个线段（以 Line 表示）的交点情况（这里保持原意：返回 pair<Point,Point>）
template<typename T = double>
pair<Point<T>, Point<T>> seg_intersection(const Line<T> &seg1, const Line<T> &seg2) {
    // 快速外排（bounding box）
    if (max(seg1.a.x, seg1.b.x) < min(seg2.a.x, seg2.b.x) - eps || min(seg1.a.x, seg1.b.x) > max(seg2.a.x, seg2.b.x) + eps ||
        max(seg1.a.y, seg1.b.y) < min(seg2.a.y, seg2.b.y) - eps || min(seg1.a.y, seg1.b.y) > max(seg2.a.y, seg2.b.y) + eps) {
        return {Point<T>(), Point<T>()};
    }
    double denom = (double)(seg1.v ^ seg2.v);
    if (sign(denom) == 0) {
        // 共线或平行
        if (sign((seg1.v) ^ (seg2.a - seg1.a)) != 0) return {Point<T>(), Point<T>()};
        vector<pair<Point<T>,int>> ps = {{seg1.a, 1}, {seg1.b, 1}, {seg2.a, 2}, {seg2.b, 2}};
        sort(ps.begin(), ps.end(), [&](const pair<Point<T>, int>& A, const pair<Point<T>, int>& B){
            if (sign(A.first.x - B.first.x) == 0) return A.first.y < B.first.y;
            return A.first.x < B.first.x;
        });
        Point<T> p1 = ps[1].first, p2 = ps[2].first;
        if (p1 == p2) return {p1, p2}; // 单点相交（端点）
        return {p1, p2}; // 重叠区间
    }
    Point<T> p = line_intersection(seg1, seg2);
    if (point_on_segment(p, seg1.a, seg1.b) && point_on_segment(p, seg2.a, seg2.b)) return {p, p};
    return {Point<T>(), Point<T>()};
}

// 判断两线段是否相交（包含端点）
// **只判断严格相交**，就把整个 {...} 块注释掉
template<typename T = double>
bool is_segment_intersect(const Line<T> &seg1, const Line<T> &seg2) {
    Point<T> A = seg1.a, B = seg1.b, C = seg2.a, D = seg2.b;
    double c1 = (B - A) ^ (C - A);
    double c2 = (B - A) ^ (D - A);
    double c3 = (D - C) ^ (A - C);
    double c4 = (D - C) ^ (B - C);
    {
        if (sign(c1) == 0 && point_on_segment(C, A, B)) return 1;
        if (sign(c2) == 0 && point_on_segment(D, A, B)) return 1;
        if (sign(c3) == 0 && point_on_segment(A, C, D)) return 1;
        if (sign(c4) == 0 && point_on_segment(B, C, D)) return 1;
    }
    // 严格相交：两端异侧
    return sign(c1) * sign(c2) < 0 && sign(c3) * sign(c4) < 0;
}

// 返回值类型：
//  0 — 不相交（no intersection）
//  1 — 严格相交（相交于两段内部，非端点）
//  2 — 重叠（共线且有区间重叠）
//  3 — 端点相交（只在端点处相交）
// 返回值元组：(type, P1, P2)
//   当 type == 0 时，P1、P2 无意义（默认构造点）
//   当 type == 1 或 3 时，P1 = P2 = 交点
//   当 type == 2 时，P1, P2 分别是重叠区间的两个端点
template<typename T = double>
tuple<int, Point<T>, Point<T>> segment_intersection(Line<T> l1, Line<T> l2) {
    // bounding boxes
    if (max(l1.a.x, l1.b.x) < min(l2.a.x, l2.b.x) - eps) return {0, Point<T>(), Point<T>()};
    if (min(l1.a.x, l1.b.x) > max(l2.a.x, l2.b.x) + eps) return {0, Point<T>(), Point<T>()};
    if (max(l1.a.y, l1.b.y) < min(l2.a.y, l2.b.y) - eps) return {0, Point<T>(), Point<T>()};
    if (min(l1.a.y, l1.b.y) > max(l2.a.y, l2.b.y) + eps) return {0, Point<T>(), Point<T>()};

    double c = (double)((l1.b - l1.a) ^ (l2.b - l2.a));
    if (sign(c) == 0) {
        if (sign((l1.b - l1.a) ^ (l2.a - l1.a)) != 0) {
            return {0, Point<T>(), Point<T>()};
        } else {
            auto maxx1 = max(l1.a.x, l1.b.x), minx1 = min(l1.a.x, l1.b.x);
            auto maxy1 = max(l1.a.y, l1.b.y), miny1 = min(l1.a.y, l1.b.y);
            auto maxx2 = max(l2.a.x, l2.b.x), minx2 = min(l2.a.x, l2.b.x);
            auto maxy2 = max(l2.a.y, l2.b.y), miny2 = min(l2.a.y, l2.b.y);
            Point<T> p1( max(minx1, minx2), max(miny1, miny2) );
            Point<T> p2( min(maxx1, maxx2), min(maxy1, maxy2) );
            if (!point_on_segment(p1, l1.a, l1.b)) { std::swap(p1.y, p2.y); }
            if (p1 == p2) return {3, p1, p2}; else return {2, p1, p2};
        }
    }
    auto cp1 = (l2.a - l1.a) ^ (l2.b - l1.a);
    auto cp2 = (l2.a - l1.b) ^ (l2.b - l1.b);
    auto cp3 = (l1.a - l2.a) ^ (l1.b - l2.a);
    auto cp4 = (l1.a - l2.b) ^ (l1.b - l2.b);
    int s1 = sign(cp1), s2 = sign(cp2), s3 = sign(cp3), s4 = sign(cp4);
    if ((s1 > 0 && s2 > 0) || (s1 < 0 && s2 < 0) || (s3 > 0 && s4 > 0) || (s3 < 0 && s4 < 0)) {
        return {0, Point<T>(), Point<T>()};
    }
    Point<T> p = line_intersection(l1, l2);
    if (cp1 != 0 && cp2 != 0 && cp3 != 0 && cp4 != 0) return {1, p, p};
    else return {3, p, p};
}

// p 到直线 l 的距离
template<typename T = double>
double distance_point_to_line(const Point<T> &p, Line<T> &l) {
    return fabsl((p - l.a) ^ l.v) / (l.v.length());
}
template<typename T = double>
double distance_point_to_line(const Point<T> &p, const Point<T> &a, const Point<T> &b) {
	Vector<T> v = b - a;
	return fabsl((p - a) ^ v) / (v.length());
}

// 返回 p 到线段 [a,b] 的 平方距离（不做 sqrt）
// 若投影在线段内部，返回 (c^2) / |v|^2
template<typename T = double>
inline double distance_point_to_segment_2(const Point<T> &p, const Point<T> &a, const Point<T> &b) {
    double vx = b.x - a.x, vy = b.y - a.y;
    double len2 = vx * vx + vy * vy;
    double px = p.x - a.x, py = p.y - a.y;
    if (!sign(len2)) {
        return px * px + py * py;
    }
    double proj = px * vx + py * vy;
    if (proj <= 0) {
        return px * px + py * py;
    }
    if (proj >= len2) {
        double pbx = p.x - b.x, pby = p.y - b.y;
        return pbx * pbx + pby * pby;
    }
    double cr = vx * py - vy * px; // cross(v, p-a)
    return (cr * cr) / len2;
}

// p 到线段 seg 的距离
template<typename T = double>
inline double distance_point_to_segment(const Point<T> &p, Line<T> &l) {
    if (l.a == l.b) return (p - l.a).length();
    Vector<T> v = l.b - l.a;
    Vector<T> u1 = p - l.a;
    Vector<T> u2 = p - l.b;
    if (sign(v * u1) < 0) return u1.length();
    if (sign(v * u2) > 0) return u2.length();
    return distance_point_to_line(p, l);
}

// 线段 s1 到线段 s2 的最短距离
template<typename T = double>
double distance_segment_to_segment(Line<T> &s1, Line<T> &s2) {
    if (is_segment_intersect(s1, s2)) return 0.0L;
    return min({
        distance_point_to_segment(s1.a, s2),
        distance_point_to_segment(s1.b, s2),
        distance_point_to_segment(s2.a, s1),
        distance_point_to_segment(s2.b, s1)
    });
}

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

// Andrew 算法求凸包（最小凸多边形） O(n log n)
template<typename T = double>
Polygon<T> get_hull(vector<Point<T>> p) {
    vector<Point<T>> h, l;
    sort(p.begin(), p.end());
    p.erase(std::unique(p.begin(), p.end()), p.end());
    if (p.size() <= 1) {
        return Polygon<T>(std::move(p));
    }
    for (auto a : p) {                                              //    < / >  ⇒ 线上有点
                                                                    //   <= / >= ⇒ 线上没点
        while (h.size() > 1 && sign((a - h.back()) ^ (a - h[h.size() - 2])) < 0) h.pop_back();
        while (l.size() > 1 && sign((a - l.back()) ^ (a - l[l.size() - 2])) > 0) l.pop_back();
        l.push_back(a);
        h.push_back(a);
    }
    l.pop_back();
    std::reverse(h.begin(), h.end());
    h.pop_back();
    l.insert(l.end(), h.begin(), h.end());
    return Polygon<T>(std::move(l));
}

template<typename T = double>
bool segment_in_polygon(Line<T> l, Polygon<T> p) {
    int n = p.size();
    if (p.in_polygon(l.a) == 0) { return false; } // 注意：in_polygon 返回 0/1/2
    if (p.in_polygon(l.b) == 0) { return false; }
    for (int i = 0; i < n; i++) {
        auto u = p[i];
        auto v = p[(i + 1) % n];
        auto w = p[(i + 2) % n];
        auto [t, p1, p2] = segment_intersection(l, Line<T>(u, v));
        if (t == 1) {
            return false;
        }
        if (t == 0) {
            continue;
        }
        if (t == 2) {
            if (point_on_segment(v, l.a, l.b) && v != l.a && v != l.b) {
                if (((v - u) ^ (w - v)) > 0) {
                    return false;
                }
            }
        } else {
            if (p1 != u && p1 != v) {
                if (point_on_line_left(l.a, Line<T>(v, u))
                    || point_on_line_left(l.b, Line<T>(v, u))) {
                    return false;
                }
            } else if (p1 == v) {
                if (l.a == v) {
                    if (point_on_line_left(u, l)) {
                        if (point_on_line_left(w, l)
                            && point_on_line_left(w, Line<T>(u, v))) {
                            return false;
                        }
                    } else {
                        if (point_on_line_left(w, l)
                            || point_on_line_left(w, Line<T>(u, v))) {
                            return false;
                        }
                    }
                } else if (l.b == v) {
                    if (point_on_line_left(u, Line<T>(l.b, l.a))) {
                        if (point_on_line_left(w, Line<T>(l.b, l.a))
                            && point_on_line_left(w, Line<T>(u, v))) {
                            return false;
                        }
                    } else {
                        if (point_on_line_left(w, Line<T>(l.b, l.a))
                            || point_on_line_left(w, Line<T>(u, v))) {
                            return false;
                        }
                    }
                } else {
                    if (point_on_line_left(u, l)) {
                        if (point_on_line_left(w, Line<T>(l.b, l.a))
                            || point_on_line_left(w, Line<T>(u, v))) {
                            return false;
                        }
                    } else {
                        if (point_on_line_left(w, l)
                            || point_on_line_left(w, Line<T>(u, v))) {
                            return false;
                        }
                    }
                }
            }
        }
    }
    return true;
}

template<typename T = double>
vector<Point<T>> half_plane(vector<Line<T>> lines) {
    sort(range(lines), [&](auto l1, auto l2) {
        auto d1 = l1.b - l1.a;
        auto d2 = l2.b - l2.a;
        if (sign(d1) != sign(d2)) {
            return sign(d1) == 1;
        }
        double cr = (double)(d1 ^ d2);
        if (sign(cr) != 0) return sign(cr) > 0;
        double dp = (double)(d1 * d2);
        return sign(dp) > 0 ? (l1.deg < l2.deg) : (l1.deg < l2.deg);
    });
    deque<Line<T>> ls; deque<Point<T>> ps;
    for (auto l : lines) {
        if (ls.empty()) {
            ls.push_back(l);
            continue;
        }
        while (!ps.empty() && !point_on_line_left(ps.back(), l)) {
            ps.pop_back();
            ls.pop_back();
        }
        
        while (!ps.empty() && !point_on_line_left(ps[0], l)) {
            ps.pop_front();
            ls.pop_front();
        }
        double cr = (double)((l.b - l.a) ^ (ls.back().b - ls.back().a));
        if (sign(cr) == 0) {
            // 平行（可能同向或反向）
            double dp = (double)((l.b - l.a) * (ls.back().b - ls.back().a));
            if (sign(dp) > 0) { // 同向：保留“更靠内侧”的那条线（用点位置判断）
                if (!point_on_line_left(ls.back().a, l)) {
                    assert(ls.size() == 1);
                    ls[0] = l;
                }
                continue;
            }
            // 反向或完全重合但不兼容 -> 无可行半平集合
            return { };
        }
        ps.push_back(line_intersection(ls.back(), l));
        ls.push_back(l);
    }
    while (!ps.empty() && !point_on_line_left(ps.back(), ls[0])) {
        ps.pop_back();
        ls.pop_back();
    }
    if (ls.size() <= 2) {
        return {};
    }
    ps.push_back(line_intersection(ls[0], ls.back()));
    return vector<Point<T>>(ps.begin(), ps.end());
}

template<typename T = double>
struct Circle {  // 显式构造浪费时间
    Point<T> O;
    double r;
    inline Circle() = default;
    inline Circle(Point<T> O_, double r_): O(O_), r(r_) {}
    inline double area() {return r * r * PI;}
    inline Point<T> Point_at(double ang) const { return Point<T>(O.x + r * cosl((double)ang), O.y + r * sinl((double)ang)); }
};
// 提供别名方法名 Point<T>
template<typename T = double>
inline Point<T> circle_point(const Circle<T>& c, double ang) { return c.Point_at(ang); }

template<typename T = double>
int relationship_between_two_circle(Circle<T> A, Circle<T> B) {
    if (A.r < B.r) std::swap(A, B);
    double d = dist(A.O, B.O);
    if (sign(d, A.r + B.r) > 0) return 4;               // separate
    if (sign(d, A.r + B.r) == 0) return 3;              // external tangent
    double dr = fabsl(A.r - B.r);
    if (sign(d, dr) == 0) return 1;                          // internal tangent
    if (sign(d, dr) > 0 && sign(d, A.r + B.r) < 0) return 2; // two line_intersection Point<T>s
    if (sign(d, dr) < 0) return 0;                           // one contains another
    return 0;
}

// 三角形内接圆
template<typename T = double>
Circle<T> in_circle(Polygon<T> tr) {
    double a = dist(tr[2], tr[0]), b = dist(tr[0], tr[1]), c = dist(tr[1], tr[2]);
    Point<T> p = Point<T>((tr[1].x * a + tr[2].x * b + tr[0].x * c) / (a + b + c), (tr[1].y * a + tr[2].y * b + tr[0].y * c) / (a + b + c));
    double s = (a + b + c) / 2.0L;
    double area = fabsl(((tr[2] - tr[1]) ^ (tr[0] - tr[1]))) / 2.0L;
    double r = 0;
    if (sign(s) != 0) r = area / s;
    return Circle<T>(p, r);
}

// 三角形外接圆
template<typename T = double>
Circle<T> circum_circle(Point<T> p1, Point<T> p2, Point<T> p3) {
    Point<T> m12((p1.x + p2.x) / 2.0L, (p1.y + p2.y) / 2.0L);
    Point<T> m13((p1.x + p3.x) / 2.0L, (p1.y + p3.y) / 2.0L);
    Vector<T> v12 = rotate(p2 - p1, PI / 2);
    Vector<T> v13 = rotate(p3 - p1, PI / 2);
    Line<T> u(m12, m12 + v12);
    Line<T> v(m13, m13 + v13);
    Point<T> O = line_intersection(u, v);
    return Circle<T>(O, dist(O, p1));
}
template<typename T = double>
Circle<T> circum_circle(const Polygon<T>& tr) {
    return circum_circle(tr[0], tr[1], tr[2]);
}

// 圆与直线是否相交
template<typename T = double>
bool circle_line_intersect(Circle<T> &o, Line<T> &l) {
    return sign(distance_point_to_line(o.O, l), o.r) <= 0;
}
// 圆线交点（假设相交）
template<typename T = double>
pair<Point<T>, Point<T>> circle_line_intersect_points(const Circle<T> &c, Line<T> &l) {
    Point<T> pr = project(c.O, l);
    double len = (double)l.v.length();
    if (sign(len) == 0) return {Point<T>(), Point<T>()};
    Vector<T> e = l.v / len;
    double base2 = c.r * c.r - (pr - c.O).square();
    if (base2 < 0 && fabsl(base2) < 1e-18L) base2 = 0;
    double base = sqrtl(max((double)0.0L, base2));
    return {Point<T>(pr.x + e.x * (T)base, pr.y + e.y * (T)base), Point<T>(pr.x - e.x * (T)base, pr.y - e.y * (T)base)};
}

// 圆圆交点（假设相交或相切）
template<typename T = double>
pair<Point<T>, Point<T>> circle_circle_intersect_points(const Circle<T> &c1, const Circle<T> &c2) {
    double d = dist(c1.O, c2.O);
    if (sign(d) == 0) return {Point<T>(), Point<T>()};
    double a = (c1.r * c1.r - c2.r * c2.r + d * d) / (2.0L * d);
    double h2 = c1.r * c1.r - a * a;
    if (h2 < 0 && fabsl(h2) < 1e-18L) h2 = 0;
    double h = sqrtl(max((double)0.0L, h2));
    Point<T> P0 = Point<T>(c1.O.x + (c2.O.x - c1.O.x) * (a / d), c1.O.y + (c2.O.y - c1.O.y) * (a / d));
    double rx = - (c2.O.y - c1.O.y) * (h / d);
    double ry = (c2.O.x - c1.O.x) * (h / d);
    return {Point<T>(P0.x + rx, P0.y + ry), Point<T>(P0.x - rx, P0.y - ry)};
}

// 向量角度
template<typename T = double>
double angle_of_vec(Vector<T> v) { return atan2l((double)v.y, (double)v.x); }
// 极坐标向量
template<typename T = double>
Vector<T> polar_vec(double r, double ang) { return Vector<T>(r * cosl((double)ang), r * sinl((double)ang)); }

// 圆 c 关于点 p 的切线
template<typename T = double>
vector<Point<T>> get_circle_point_tangent_points(const Circle<T> &c, Point<T> p) {
    Vector v = p - c.O;
    double d2 = v.square();
    double r2 = c.r * c.r;
    if (sign(d2, r2) < 0) return { };
    if (sign(d2, r2) == 0) return { p };
    double d = sqrtl(d2);
    double alpha = acosl(c.r / d);
    double base = atan2l((double)v.y, (double)v.x);
    return {c.Point_at(base + alpha), c.Point_at(base - alpha)};
}

// 计算两个圆的外/内公切线（返回切点对）

// 1. 若 A.r < B.r，则交换两圆并把数组位置对换（递归实现）以保证 A.r >= B.r，便于统一处理。
// 2. 若两圆同心且半径相等 -> 重合（返回 -1）。
// 3. 若一圆在另一圆内且不相切 -> 无公切线（返回 0）。
// 4. 若内切（一个圆内切于另一个） -> 有 1 条公切线（内切处的切线，接触点方向为连心线方向）。
// 5. 一般情况：先算外公切线（2 条），再算内公切线（0/1/2 条，取决于是否相离/相切/相交）。

template<typename T = double>
int get_circle_circle_tangents(Circle<T>& A, Circle<T>& B, vector<Point<T>>& a, vector<Point<T>>& b) {
    if (A.r < B.r) return get_circle_circle_tangents(B, A, b, a);
    int cnt = 0;
    double d = dist(A.O, B.O);
    double rdiff = A.r - B.r, rsum = A.r + B.r;

    if (sign(d) == 0 && sign(A.r - B.r) == 0) { return -1; }
    if (sign(d, fabsl(rdiff)) < 0) return 0;
    if (sign(d, fabsl(rdiff)) == 0) {
        double base = atan2l((double)(B.O.y - A.O.y), (double)(B.O.x - A.O.x));
        a.push_back(A.Point_at(base));
        b.push_back(B.Point_at(base));
        return ++cnt; // 1
    }
    double base = atan2l((double)(B.O.y - A.O.y), (double)(B.O.x - A.O.x));
    if (sign(d) != 0) {
        double ang = acosl(fabsl(rdiff) / d);
        a.push_back(A.Point_at(base + ang)); b.push_back(B.Point_at(base + ang)); cnt++;
        a.push_back(A.Point_at(base - ang)); b.push_back(B.Point_at(base - ang)); cnt++;
    }

    if (sign(d, rsum) == 0) {
        a.push_back(A.Point_at(base));
        b.push_back(B.Point_at(base + PI));
        cnt++;
    } else if (sign(d, rsum) > 0) {
        double ang2 = acosl(rsum / d);
        a.push_back(A.Point_at(base + ang2)); b.push_back(B.Point_at(base + ang2 + PI)); cnt++;
        a.push_back(A.Point_at(base - ang2)); b.push_back(B.Point_at(base - ang2 + PI)); cnt++;
    }
    return cnt;
}

// 由两点 a,b 求中点
template<typename T = double>
inline Point<T> middle(Point<T> a, Point<T> b) { return Point<T>((a.x + b.x) / 2.0L, (a.y + b.y) / 2.0L); }

// 最小覆盖圆（Welzl 随机增量）
template<typename T = double>
Circle<T> minimum_circle(Polygon<T> a) {
    mt19937 gen(chrono::system_clock::now().time_since_epoch().count());
    int n = a.size();
    shuffle(a.begin(), a.end(), gen);
    Circle ans(Point<T>(0, 0), 0);
    for (int i = 0; i < n; i++)
        if (sign(dist(ans.O, a[i]) - ans.r) > 0) {
            ans = Circle(a[i], 0);
            for (int j = 0; j < i; j++)
                if (sign(dist(ans.O, a[j]) - ans.r) > 0) {
                    ans = Circle(middle(a[i], a[j]), dist(a[i], a[j]) / 2);
                    for (int k = 0; k < j; k++)
                        if (sign(dist(ans.O, a[k]) - ans.r) > 0) {
                            ans = circum_circle(a[i], a[j], a[k]);
                        }
                }
        }
    return ans;
}

template<typename T = int>
struct Frac {
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




这段建议直接放在你 `get_hull()` 后面，后面所有旋转卡壳都优先用它。

```cpp
template<typename T = double>
inline i128 dot_i128(const Point<T> &a, const Point<T> &b) {
    return (i128)a.x * b.x + (i128)a.y * b.y;
}

template<typename T = double>
inline i128 cross_i128(const Point<T> &a, const Point<T> &b) {
    return (i128)a.x * b.y - (i128)a.y * b.x;
}

template<typename T = double>
inline i128 dist2_i128(const Point<T> &a, const Point<T> &b) {
    i128 dx = (i128)a.x - b.x;
    i128 dy = (i128)a.y - b.y;
    return dx * dx + dy * dy;
}
```

---

**模板 1：经典旋转卡壳，求凸包直径**

前提：

- `ch` 是**严格凸**、**逆时针**
- 你现在这个 `get_hull()` 用了 `<= / >=`，正好就是我想要的这种“去掉共线内点”的 hull

```cpp
template<typename T = double>
i128 convex_diameter2(const Polygon<T> &ch) {
    int n = (int)ch.size();
    if (n <= 1) return 0;
    if (n == 2) return dist2_i128(ch[0], ch[1]);

    int j = 1;
    i128 ans = 0;

    for (int i = 0; i < n; i++) {
        int ni = (i + 1) % n;

        while (cross_i128(ch[ni] - ch[i], ch[(j + 1) % n] - ch[j]) > 0) {
            j = (j + 1) % n;
        }

        ans = max(ans, dist2_i128(ch[i], ch[j]));
        ans = max(ans, dist2_i128(ch[ni], ch[j]));
    }

    return ans;
}
```

这个板子就是最经典那种：

- 枚举一条边 `i -> i+1`
- `j` 去找和这条边“最对着”的点
- `j` 只会单调前进一圈

---

**模板 2：线性函数最值版旋转卡壳**

这个就是你这道题真正该用的板子。

含义：

- 固定一个点 `A`
- `B` 在凸包上按顺序扫
- 对每个 `ab = B - A`
- 在线性时间里维护让 `dot(ab, C - A)` 最小的 `C`

```cpp
template<typename T = double>
i128 min_dot_rotating_calipers(const Polygon<T> &ch, const Point<T> &A) {
    int m = (int)ch.size();
    if (m <= 1) return 0;

    vector<Point<T>> H(m * 2);
    for (int i = 0; i < m; i++) {
        H[i] = H[i + m] = ch[i];
    }

    i128 res = 0;
    int j = 0;

    for (int i = 0; i < m; i++) {
        if (j < i) j = i;

        Point<T> ab = H[i] - A;

        // 如果沿着边 j -> j+1 继续走，dot 还在下降，就继续推 j
        while (j + 1 < i + m && dot_i128(ab, H[j + 1] - H[j]) < 0) {
            j++;
        }

        res = min(res, dot_i128(ab, H[j] - A));
        if (j + 1 < i + m) {
            res = min(res, dot_i128(ab, H[j + 1] - A));
        }
    }

    return res;
}
```

这个板子背后的判断条件你一定要记住：

```cpp
dot_i128(ab, H[j + 1] - H[j]) < 0
```

含义是：

- 从 `H[j]` 走到 `H[j+1]`
- 目标函数 `dot(ab, C - A)` 还在继续减小
- 那就继续推指针

一旦不小了，最优点就在 `j / j+1` 附近。

---

**基于这个板子，Astral Decay 的 `solve()` 可以直接写成这样**

```cpp
void solve() {
    int n;
    cin >> n;
    vector<Point<int>> p(n);
    for (int i = 0; i < n; i++) {
        p[i].read();
    }

    auto ch = get_hull(p);

    i128 ans = 0;
    for (auto &A : p) {
        ans = min(ans, min_dot_rotating_calipers(ch, A));
    }

    cout << ans << '\n';
}
```

---

**如果你想做一个“更通用”的旋转卡壳记忆法**

你可以把旋转卡壳大致分成两类：

1. `边 -> 点`
   典型：凸包直径、最小宽度、最小面积矩形
   判的是 `cross`
2. `方向 -> 支撑点`
   典型：这道题、线性函数在凸包上的最值
   判的是 `dot`

你这次容易绕晕，就是因为把第二类题硬往“点在线哪一侧”上套了。


## 基础知识

### llround()

如果题目要输出整数，而过程中一直用浮点计算，最后一定要调用一下round函数来保证不会出错。

### 极角 atan2

atan2(a.y, a.x) = 0
atan2(b.y, b.x) = 0.785398
atan2(c.y, c.x) = 1.5708
atan2(d.y, d.x) = 2.35619
atan2(e.y, e.x) = 3.04192
atan2(f.y, f.x) = 3.14159
atan2(g.y, g.x) = -3.04192
atan2(h.y, h.x) = -2.35619
atan2(i.y, i.x) = -1.5708
atan2(j.y, j.x) = -0.785398
atan2(k.y, k.x) = -0.0996687

```C++
	Point a = {1, 0}, b = {1, 1}, c = {0, 1}, d = {-1, 1}, e = {-1, 0.1}, f = {-1, 0}, g = {-1, -0.1}, h = {-1, -1}, i = {0, -1}, j = {1, -1}, k = {1, -0.1};
	debug(atan2(a.y, a.x));
	debug(atan2(b.y, b.x));
	debug(atan2(c.y, c.x));
	debug(atan2(d.y, d.x));
	debug(atan2(e.y, e.x));
	debug(atan2(f.y, f.x));
	debug(atan2(g.y, g.x));
	debug(atan2(h.y, h.x));
	debug(atan2(i.y, i.x));
	debug(atan2(j.y, j.x));
	debug(atan2(k.y, k.x));
```

### 极角排序

```C++
    double X = 0, Y = 0;
    vector<Point> p(n);
    for (int i = 0; i < n; i++) {
        p[i].read();
        X += p[i].x, Y += p[i].y;
    }
    Point mid = Point(X / (double)n, Y / (double)n);
    vector<int> it(n);
    iota(it.begin(), it.end(), 0);
    sort(it.begin(), it.end(), [&](int i, int j) {
        auto a = p[i], b = p[j];
        return atan2(a.y - mid.y, a.x - mid.x) < atan2(b.y - mid.y, b.x - mid.x);
    });
```

### 把 O be 化为极轴
```C++
	for (auto &a : ang) {  // 本身 ang 中点角度以 OX 为极轴
		a -= be.polarAngle();
		if (a < 0) a += PI * 2;
	}
	sort(ang.begin(), ang.end());
```

## 结论定理

* Pick定理 （根据点在多边形内和边界的个数求面积）
	$a = S − \frac{b}{2} ​+ 1$

	**其中a表示多边形内部的点数，b表示多边形边界上的点数，S表示多边形的面积。**

* 任意凸多边形的内角和 (n - 2) * 180°

```C++
弧长 L = PI * r （弧度 * 半径）
```

## 一些算法

### 关于可以框住三个矩形范围的最小面积

三个矩形必须保持水平，垂直放置

```C++
三个矩形横着摆一行
ans = min(ans, (b[0].x + b[1].x + b[2].x) * max({b[0].y, b[1].y, b[2].y}));

三个矩形竖着摆一列
ans = min(ans, (b[0].y + b[1].y + b[2].y) * max({b[0].x, b[1].x, b[2].x}));

两个矩形横着摆，第三个矩形放在下面
do {
    ans = min(ans,
              max(b[p[0]].x + b[p[1]].x, b[p[2]].x) *
              (max(b[p[0]].y, b[p[1]].y) + b[p[2]].y));
} while (next_permutation(p, p + 3));
```

### 极角排序

* 以OX 为极轴，逆时针进行排序

```C++
Point O = P[i], X = P[i] + Vector(1, 0);
sort(t.begin(), t.end(), [&](const Point &A, const Point &B) -> bool {
	double cA = (X - O) ^ (A - O);
	double cB = (X - O) ^ (B - O);
	if (sign(cA) == 0 && sign((X.x - O.x) * (A.x - O.x)) > 0) return 1;
	if (sign(cB) == 0 && sign((X.x - O.x) * (B.x - O.x)) > 0) return 0;
	if ((sign(cA) > 0) != sign(cB) > 0) return sign(cA) > 0;
	return sign((A - O) ^ (B - O)) > 0;
});
```

### 平面最近点对

```C++
bool cmpx(Point A, Point B)
{
	if (dcmp(A.x, B.x) == 0) return A.y < B.y;
	return A.x < B.x;
}
bool cmpy(Point A, Point B)
{
	return A.y < B.y;
}
double get_dist2(Point A, Point B)
{
	double dx = A.x - B.x, dy = A.y - B.y;
	return dx * dx + dy * dy;
}

sort(p + 1, p + 1 + n, cmpx);

double merge(Point p[], int l, int r)
{
	double d = INF;
	if (l == r) return d;
	if (l + 1 == r) return get_dist2(p[l], p[r]);

	int mid = l + r >> 1;
	d = min(merge(p, l, mid), merge(p, mid + 1, r));

	int cnt = 0;
	vector<Point> tmp(r - l + 3);
	for (int i = l; i <= r; i++)
		if ((p[mid].x - p[i].x) * (p[mid].x - p[i].x) <= d)
			tmp[++cnt] = p[i];

	sort(tmp.begin() + 1, tmp.begin() + cnt + 1, cmpy);

	for (int i = 1; i <= cnt; i++)
		for (int j = i + 1; j <= cnt; j++)
		{
			if ((tmp[j].y - tmp[i].y) * (tmp[j].y - tmp[i].y) > d) break;
			d = min(d, get_dist2(tmp[i], tmp[j]));
		}

	return d;
}
```

### 辛普森积分（simpson）

```C++
/*  
    接口（示例）:
    // 一维
    double res = adaptive_simpson([](double x)->double { return sin(x); }, 0.0, M_PI, 1e-9);
    // 二维
    double res2 = integrate2D(0,1, 0,1, [](double x,double y)->double { return x*y; }, 1e-8);
    // 三维
    double res3 = integrate3D(0,1, 0,1, 0,1, [](double x,double y,double z)->double { return x*y*z; }, 1e-7);

*/

// 单段辛普森（使用已计算的端点值）
template<typename F>
inline double simpson_segment(F &f, double a, double b, double fa, double fm, double fb) {
    return (fa + 4.0 * fm + fb) * (b - a) / 6.0;
}

// 递归自适应辛普森核心（传入已知端点与中点值，减少重复计算）
// depth 用于限制递归深度，避免极端情况下栈溢出
template<typename F>
double adaptive_simpson_core(F &f, double a, double b, double eps, double whole,
                             double fa, double fm, double fb, int depth=0) {
    double mid = 0.5 * (a + b);
    double lm = 0.5 * (a + mid);
    double rm = 0.5 * (mid + b);

    double flm = f(lm);
    double frm = f(rm);

    double left = simpson_segment(f, a, mid, fa, flm, fm);
    double right = simpson_segment(f, mid, b, fm, frm, fb);

    double diff = left + right - whole;
    if (depth >= 60) { // 极端保护：深度太大 -> 返回合并估计（保守）
        return left + right + diff / 15.0;
    }
    if (fabs(diff) <= 15.0 * eps) {
        // Romberg 修正
        return left + right + diff / 15.0;
    }
    // 继续细分，误差等分到子区间（eps/2）
    return adaptive_simpson_core(f, a, mid, eps / 2.0, left, fa, flm, fm, depth + 1)
         + adaptive_simpson_core(f, mid, b, eps / 2.0, right, fm, frm, fb, depth + 1);
}

// 对外的一维自适应辛普森接口（自动计算端点与中点）
template<typename F>
double adaptive_simpson(F f, double a, double b, double eps = 1e-9) {
    double fa = f(a);
    double fb = f(b);
    double fm = f(0.5 * (a + b));
    double whole = simpson_segment(f, a, b, fa, fm, fb);
    return adaptive_simpson_core(f, a, b, eps, whole, fa, fm, fb);
}

// 二维积分（嵌套自适应辛普森）
// integrate2D(x1,x2, y1,y2, f(x,y), eps)
// 简单地把 eps 一分为二给外层和内层，实际应用中可根据需要调整
template<typename F2>
double integrate2D(double x1, double x2, double y1, double y2, F2 f, double eps = 1e-8) {
    auto inner = [&](double x)->double {
        auto fy = [&](double y)->double {
            return f(x, y);
        };
        // 内层 eps 取 eps/2（内外各一半）
        return adaptive_simpson(fy, y1, y2, eps * 0.5);
    };
    return adaptive_simpson(inner, x1, x2, eps * 0.5);
}

// 三维积分（嵌套）
// integrate3D(x1,x2, y1,y2, z1,z2, f(x,y,z), eps)
template<typename F3>
double integrate3D(double x1, double x2, double y1, double y2, double z1, double z2, F3 f, double eps = 1e-7) {
    auto inner2 = [&](double x, double y)->double {
        auto fz = [&](double z)->double {
            return f(x,y,z);
        };
        return adaptive_simpson(fz, z1, z2, eps * 0.25);
    };
    auto inner1 = [&](double x)->double {
        auto fy = [&](double y)->double {
            return inner2(x,y);
        };
        return adaptive_simpson(fy, y1, y2, eps * 0.25);
    };
    return adaptive_simpson(inner1, x1, x2, eps * 0.5);
}
```
