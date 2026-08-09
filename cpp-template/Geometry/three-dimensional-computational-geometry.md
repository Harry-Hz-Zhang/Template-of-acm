---
topic: "三维计算几何"
category: "06-geometry"
source: "几何 Geometry.md"
---

# 三维计算几何

## 球面几何
### 球冠面积
$$S(α) = r^2*∫_{0}^{2π}​∫_0^{α}​sinθdθdϕ= r^2 *2π(1−cosα)$$
### 球面二角形
$$S = 2 r^2 α$$
### 球面三角形
$$ S = r^2 * (α + β + γ - \pi)$$
### 球面余弦定理和正弦定理

球面三角形任一角的余弦等于其它两角余弦的乘积冠以负号加上这两角的正弦及其夹边余弦的连乘积。

球面三角形任一边的余弦等于其它两边余弦的乘积加上这两边的正弦及其夹角余弦的连乘积。

$$cosA=－cosBcosC+sinBsinCcosa$$
$$cosB=－cosCcosA+sinCsinAcosb$$
$$cosC=－cosAcosB+sinAsinBcosc$$
$$cosa=cosbcosc+sinbsinccosA$$
$$cosb=cosc cosa+sincsinacosB$$
$$cosc=cosacosb+sinasinbcosC$$

球面三角形三组边的正弦与角的正弦比值相等。

sin⁡A / sin⁡a=sin⁡B / sin⁡b=sin⁡C / sin⁡c

### 两球冠相交的面积

<!-- image removed -->

求解 $点AB$ 和两条弧构成的相交面积：

两球面三角形 $PAQ,PBQ$ ，两个部分球盖 $PAB,QAB$.

进行一个简单的面积容斥：记 $x1=∠PAQ$,  $x2=∠APQ$.

$$S_1​+2S_△​=\frac{4x_2}{2π}​​S(α)$$

$S_1$ 即要求相交部分的面积

又由于**球面三角形面积公式**和**球冠面积公式**：$$S = r^2 * (α + β + γ - \pi)$$
得： $$S_1​=2π−2x_1​−4x_2​cosα$$
### 直角球面三角形的 Napier 关系

对于一个「带有一个直角」的球面三角形（设直角在顶点 $M$）：

正切公式（之一）：

如果以小写 $m,p,h$ 分别表示与大写角 $M,P,H$ 对应的**对边弧长**，那么

$$tan(p)=tan(P)sin(h),$$
$$tan(h)=tan(H)sin(p),$$
$$cos(p)=cos(h)cos(m).$$


## 求体积 V

$$体积=∫^{z = b}_{z=a} ​f(z)dz$$
### 对于球体

利用对称性（上下对称），我们可以写成
$$\text{体积} = 2\int_{z=0}^{R} f(z)\, dz.$$
$$\text{球在该高度的半径} = f(z) = \sqrt{R^2 - z^2}$$

* 对于一些经过加减之后的体积 $f(z)= R+s(z).$


## 基础模板

```C++
const long double PI = acosl(-1);
const long double eps = 1e-10;
int sign(long double x) {
	if (fabsl(x) < eps) return 0;
    else return x > 0 ? 1 : -1;
}
int dcmp(long double x, long double y) {
	if (fabsl(x - y) < eps) return 0;
    else return x > y ? 1 : -1;
}
struct Vector {
	long double x, y, z;
	Vector(long double x_ = INF, long double y_ = INF, long double z_ = INF): x(x_), y(y_), z(z_) { }
	Vector operator+ (Vector t) const { return Vector(x + t.x, y + t.y, z + t.z); }
	Vector operator- (Vector t) const { return Vector(x - t.x, y - t.y, z - t.z); }
	long double operator* (Vector t) const { return x * t.x + y * t.y + z * t.z; }
	Vector operator^ (Vector t) const {
		return Vector(y * t.z - z * t.y,
					  z * t.x - x * t.z,
					  x * t.y - y * t.x);
	}
	Vector operator* (const long double &r) const { return Vector(x * r, y * r, z * r); }
	Vector operator/ (const long double &r) const { return Vector(x / r, y / r, z / r); }
    long double length() const { return sqrtl(*this * *this); }
    bool operator == (const Vector A) const {
        return dcmp(x, A.x) == 0 && dcmp(y, A.y) == 0 && dcmp(z, A.z) == 0;
    }
    void read() { cin >> x >> y >> z; }
};
using Point = Vector;

long double dist(Point a, Point b) {
    long double dx = a.x - b.x, dy = a.y - b.y, dz = a.z - b.z;
    return sqrtl(dx * dx + dy * dy + dz * dz);
}

struct Line {
    Point A, B;
    Line() = default;
    Line(Vector a, Vector b): A(a), B(b) { }
};

struct Plane {
    Vector A, B, C;
    Plane() = default;
    Plane(Vector a_, Vector b_, Vector c_): A(a_), B(b_), C(c_) { }
    Vector normalVector() {
        return Vector((B - A) ^ (C - A));
    }
};
// 球(圆)心角 传入向量，返回 theta rad // 弧度
long double central_angle(const Point &A, const Point &B) {
    long double num = A * B;
    long double den = A.length() * B.length();  // 单位化
    return acosl( min<long double>( max<long double>(num/den, -1), +1) );
}
// 根据球心角 a 计算球冠表面积
long double spherical_cap_Area(long double angle) {
    return 2.0L * PI * (1.0L - cosl(angle));
}

void solve()
{
    long double r;
    cin >> r;
    Point p, s, t;
    p.read(), s.read(), t.read();
    p = p / p.length(), s = s / s.length(), t = t / t.length();

    Vector N = s ^ t;
    Point h = ((p ^ N) ^ N) * -1;

    h = h / h.length();
    long double ans = min(centralAngle(p, s), centralAngle(p, t));
    if (dcmp(centralAngle(s, h) + centralAngle(t, h), centralAngle(s, t)) == 0) {
        ans = centralAngle(p, h);
    }
    ans *= r;
    cout << fixed << setprecision(15);
    cout << ans << endl;
}
```

## 三维凸包

```C++
#include<iostream>
#include<algorithm>
#include<cstring>
#include<vector>
#include<cmath>

using namespace std;

const int N = 5010;
const double eps = 1e-12;

int n, m;
int g[N][N];

double rand_eps()
{
	return ((double)rand() / RAND_MAX - 0.5) * eps;
}

struct Point
{
	double x, y, z;

	Point(double x = 0, double y = 0, double z = 0) :x(x), y(y), z(z) { }
	Point operator- (Point& t) { return Point(x - t.x, y - t.y, z - t.z); }
	Point operator+ (Point& t) { return Point(x + t.x, y + t.y, z + t.z); }
	void shake()
	{
		x += rand_eps(), y += rand_eps(), z += rand_eps();
	}
	double len()		//求向量的模长，三个坐标也能存向量
	{
		return sqrt(x * x + y * y + z * z);
	}
}P[N];

typedef Point Vector;

double dot(Vector a, Vector b)
{
	return a.x * b.x + a.y * b.y + a.z * b.z;
}

double length(Vector a)
{
	return sqrt(dot(a, a));
}

Vector cross(Vector a, Vector b)
{
	return Vector(a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x);
}


struct Face
{
	int v[3];

	Face() { }
	Face(int a, int b, int c)
	{
		v[0] = a, v[1] = b, v[2] = c;
	}
	Vector Normal()
	{
		return cross(P[v[1]] - P[v[0]], P[v[2]] - P[v[0]]);
	}
	int Cansee(int i)
	{
		return dot(P[i] - P[v[0]], Normal()) > 0;
	}
	double area()		//求一平面的面积
	{
		return Normal().len() / 2;	//法向量的模长除以2
	}
}ch[N], tp[N];

void convex()
{
	ch[m++] = Face( 0, 1, 2 ), ch[m++] = Face( 2, 1, 0 );
	for (int i = 3; i < n; i++)
	{
		int cnt = 0;
		for (int j = 0; j < m; j++)
		{
			bool fg = ch[j].Cansee(i);
			if (!fg)
				tp[cnt++] = ch[j];
			for (int k = 0; k < 3; k++)
				g[ch[j].v[k]][ch[j].v[(k + 1) % 3]] = fg;
		}
		for (int j = 0; j < m; j++)
		{
			for (int k = 0; k < 3; k++)
			{
				int a = ch[j].v[k], b = ch[j].v[(k + 1) % 3];
				if (g[a][b] && !g[b][a]) tp[cnt++] = { a, b, i };
			}
		}
		m = cnt;
		for (int j = 0; j < m; j++)
			ch[j] = tp[j];
	}
}

int main()
{
	cin >> n;
	for (int i = 0; i < n; i++)
	{
		cin >> P[i].x >> P[i].y >> P[i].z;
		P[i].shake();
	}

	convex();

	double ans = 0;
	for (int i = 0; i < m; i++) ans += ch[i].area();
	printf("%.3lf", ans);

	return 0;
}

```
