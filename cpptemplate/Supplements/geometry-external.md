---
topic: "别人的几何模板"
category: "geometry-external"
source: "别人的几何模板.md"
---

```C++

/*
https://blog.csdn.net/qq_34731703/article/details/53769806?
POJ: 1113 2318 1556 1696 2826 2074 1873 3252 2187 3608
LuoGu: 3187
*/
/*
floor();//向下取整  ceil();//向上取整  round();//四舍五入
判等时不要直接使用=
*/
//#include<bits/stdc++.h>
#include<map>
#include<set>
#include<cmath>
#include<queue>
#include<cstdio>
#include<vector>
#include<climits>
#include<cstring>
#include<cstdlib>
#include<iostream>
#include<algorithm>
using namespace std;
const double pi = acos(-1.0);
const double inf = 1e100;
/*
误差判断
*/
const double eps = 1e-10;
//大小判断 
int dcmp(double x, double y){
    if(fabs(x - y) < eps)
        return 0;
    if(x > y)
        return 1;
    return -1;
}
//符号判断 
int sgn(double d){
    if(fabs(d) < eps)
        return 0;
    if(d > 0)
        return 1;
    return -1;
}
/*---------------------------------------------------------------------------------------*/
//点
struct Point{
	double x, y;
    Point(double x = 0, double y = 0):x(x),y(y){}
};
//向量
typedef Point Vector;
//运算
Vector operator + (Vector A, Vector B){
    return Vector(A.x+B.x, A.y+B.y);
}
Vector operator - (Vector A, Vector B){
    return Vector(A.x-B.x, A.y-B.y);
}
Vector operator * (Vector A, double p){
    return Vector(A.x*p, A.y*p);
}
Vector operator / (Vector A, double p){
    return Vector(A.x/p, A.y/p);
}
bool operator == (Point A,Point B){
	return sgn(A.x-B.x)==0&&sgn(A.y-B.y)==0;
}
bool P_cmp1(Point a,Point b){
    if(a.x==b.x)
    	return a.y<b.y;
    return a.x<b.x;
}
//向量数量积  向量α在向量β的投影于向量β的长度乘积（带方向）
double Dot(Vector A, Vector B){
    return A.x*B.x + A.y*B.y;
}
//向量向量积  向量α与β所张成的平行四边形的有向面积
double Cross(Vector A, Vector B){
    return A.x*B.y-A.y*B.x;
}
//取模
double Length(Vector A){
    return sqrt(Dot(A, A));
}
//计算夹角
double Angle(Vector A, Vector B){
    return acos(Dot(A, B) / Length(A) / Length(B));
}
//向量旋转
Vector Rotate(Vector A, double rad){//rad为弧度 且为逆时针旋转的角
    return Vector(A.x*cos(rad)-A.y*sin(rad), A.x*sin(rad)+A.y*cos(rad));
}
Vector Normal(Vector A){//向量A左转90°的单位法向量
    double L = Length(A);
    return Vector(-A.y/L, A.x/L);
}
//三角形外接圆圆心
Point Excenter(Point a, Point b, Point c){
    double a1 = b.x - a.x;
    double b1 = b.y - a.y;
    double c1 = (a1*a1 + b1*b1)/2;
    double a2 = c.x - a.x;
    double b2 = c.y - a.y;
    double c2 = (a2*a2 + b2*b2)/2;
    double d = a1*b2 - a2*b1;
    return Point(a.x + (c1*b2 - c2*b1)/d, a.y + (a1*c2 - a2*c1)/d);
}
//两点距离
double dis(Point a,Point b){
	return sqrt((a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y));
}
double dis2(Point a,Point b){
	return ((a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y));
}
//极角排序 
Point Tmp(0,0);//选好的起点
int Quadrant(Point a){// 象限
    if(a.x>0&&a.y>=0)  return 1;
    if(a.x<=0&&a.y>0)  return 2;
    if(a.x<0&&a.y<=0)  return 3;
    if(a.x>=0&&a.y<0)  return 4;
}
bool Polar_angle_cmp(Point a,Point b){
    if(Quadrant(a-Tmp)==Quadrant(b-Tmp)){
        double ans=Cross(a-Tmp,b-Tmp);
        if(ans==0)return a.x<b.x;
        return ans>0;
    }
    return Quadrant(a-Tmp)<Quadrant(b-Tmp);
}


//线
struct Line{//直线定义
    Point v, p;
    Line(){}
    Line(Point v, Point p):v(v), p(p){}
};
//判断点是否在线上
bool PointOnline(Line A,Point a){
	Vector v1(A.p.x-a.x,A.p.y-a.y);
	Vector v2(A.v.x-a.x,A.v.y-a.y);
	return !(Cross(v1,v2));
}
//计算两直线交点 必须保证直线相交，否则将会出现除以零的情况
Point GetLineIntersection(Point a1, Point a2, Point b1, Point b2){
	Vector v = a1-a2;
	Vector w = b1-b2;
	Vector u = a1-b1;
    double t = Cross(w, u)/Cross(v, w);
    return a1+v*t;
}
//点P到直线AB距离公式
double DistanceToLine(Point P, Point A, Point B){
    Vector v1 = B-A, v2 = P-A;
    return fabs(Cross(v1, v2)/Length(v1));
}
//点A到线段BC距离公式
double DistanceToSegment(Point A, Point B, Point C){
    if(dis(B,C)<eps)       return dis2(A,B);
    if(Dot(B-C,A-C)<0)    return dis2(A,C);
    if(Dot(A-B,C-B)<0)    return dis2(A,B);
    return fabs((Cross(B-A,C-A)*Cross(B-A,C-A)/dis2(B,C)));
} 
//点P在直线AB上的投影点
Point GetLineProjection(Point P, Point A, Point B){
    Vector v = B-A;
    return A+v*(Dot(v, P-A)/Dot(v, v));
}
//判断点是否在线段上
bool OnSegment(Point p, Point a1, Point a2){
    return dcmp(Cross(a1-p, a2-p),0) == 0 && dcmp(Dot(a1-p, a2-p),0) <= 0;
}
//判断线段相交
bool SegmentProperIntersection(Point a1, Point a2, Point b1, Point b2){
    double c1 = Cross(a2-a1, b1-a1), c2 = Cross(a2-a1, b2-a1);
    double c3 = Cross(b2-b1, a1-b1), c4 = Cross(b2-b1, a2-b1);
    //if判断控制是否允许线段在端点处相交，根据需要添加
    if(!sgn(c1) || !sgn(c2) || !sgn(c3) || !sgn(c4)){
        bool f1 = OnSegment(b1, a1, a2);
        bool f2 = OnSegment(b2, a1, a2);
        bool f3 = OnSegment(a1, b1, b2);
        bool f4 = OnSegment(a2, b1, b2);
        bool f = (f1|f2|f3|f4);
        return f;
    }
    return (sgn(c1)*sgn(c2) < 0 && sgn(c3)*sgn(c4) < 0);
}
//点c是否在线段ab的左侧 左1 线上0 右-1
int ToLeftTest(Point a, Point b, Point c){
    if( Cross(b - a, c - b) > 0) return 1;
    else if( Cross(b - a, c - b) == 0) return 0;
    else return -1;
}


//多边形
//求凸包 多边形p  凸包ch 
int ConvexHull(Point *p,int n,Point *ch){
	n=unique(p,p+n)-p;//去重
	sort(p,p+n,P_cmp1);//整理凸包 
	int v=0;
	for(int i=0;i<n;i++){ 
		while(v>1&&Cross(ch[v-1]-ch[v-2],p[i]-ch[v-1])<=0)
			v--;
		ch[v++]=p[i];
	}
	int j=v;
	for(int i=n-2;i>=0;i--){
		while(v>j&&Cross(ch[v-1]-ch[v-2],p[i]-ch[v-1])<=0)
			v--;
		ch[v++]=p[i];
	}
	if(n>1) v--;
	return v;
}
//逆时针排序:整理凸包
void anticlockwise_sort(Point* P,int N){
    for(int i=0;i<N-2;i++){
        int tmp=Cross(P[i+1]-P[i],P[i+2]-P[i]);
        if(tmp >0)
            return ;
        else if(tmp<0){
            reverse(P,P+N);
            return;
        }
    }
}
//求凸包周长
double CofCH(Point *ch,int m){
	double C=0;
	for(int i=0;i<m;i++)
		C+=dis(ch[i],ch[(i+1)%m]);
	return C;
}
//多边形有向面积
double PolygonArea(Point* p, int n){//p为端点集合，n为端点个数
    double s = 0;
    for(int i = 1; i < n-1; ++i)
        s += Cross(p[i]-p[0], p[i+1]-p[0]);
    return s;
}
//判断点是否在多边形内，若点在多边形内返回1，在多边形外部返回0，在多边形上返回-1
int isPointInPolygon(Point p, Point *poly,int n){
    int wn = 0;
    for(int i = 0; i < n; ++i){
        if(OnSegment(p, poly[i], poly[(i+1)%n])) return -1;
        int k = sgn(Cross(poly[(i+1)%n] - poly[i], p - poly[i]));
        int d1 = sgn(poly[i].y - p.y);
        int d2 = sgn(poly[(i+1)%n].y - p.y);
        if(k > 0 && d1 <= 0 && d2 > 0) wn++;
        if(k < 0 && d2 <= 0 && d1 > 0) wn--;
    }
    if(wn != 0)
        return 1;
    return 0;
}
//旋转卡壳
//求最远点对
double RTJ_PP(Point *poly,int n){
	poly[n]=poly[0];
	double res=0;
	for(int i=0,j=1;i<n;i++){
		while(Cross(poly[i]-poly[j],poly[i+1]-poly[j])<Cross(poly[i]-poly[j+1],poly[i+1]-poly[j+1]))
			j=(j+1)%n;
		res=max(res,max(dis(poly[i],poly[j]),dis(poly[i+1],poly[j])));
	}
	return res;
} 
//凸包最近点对 (算两次)
double PTJ_CHCH(Point *P,int N,Point *Q,int M){
	anticlockwise_sort(P,N);
	anticlockwise_sort(Q,M);
	int yminP=0,ymaxQ=0;
    for(int i=0;i<N;i++)    if(P[yminP].y>P[i].y)   yminP=i;
    for(int i=0;i<M;i++)    if(Q[ymaxQ].y<Q[i].y)   ymaxQ=i;
	P[N]=P[0];
    Q[M]=Q[0];
    double arg,ans=inf;
    for(int i=0;i<N;i++)//以P为主图形，以yminP为起点 所有点跑一圈
    {
        while(arg=Cross(P[yminP+1]-P[yminP],Q[ymaxQ+1]-P[yminP])-Cross(P[yminP+1]-P[yminP],Q[ymaxQ]-P[yminP])>0 )
            ymaxQ=(ymaxQ+1)%M;
        double asd=min(
		min(DistanceToSegment(P[yminP],Q[ymaxQ],Q[ymaxQ+1]),DistanceToSegment(P[yminP+1],Q[ymaxQ],Q[ymaxQ+1])),
		min(DistanceToSegment(Q[ymaxQ],P[yminP],P[yminP+1]),DistanceToSegment(Q[ymaxQ+1],P[yminP],P[yminP+1]))
		);
		ans=min(ans,asd);
        yminP=(yminP+1)%N;
	}
    return ans;
}
//求凸多边形最小面积外接矩阵
double PTJ_MAEM(Point *ch,int n,Point *MX){
	ch[n]=ch[0];
	double ans=inf;
	int j=1,k=1,l;
	for(int i=0;i<n;i++){
		//最上点 
		while(Cross(ch[i]-ch[j],ch[i+1]-ch[j])<=Cross(ch[i]-ch[j+1],ch[i+1]-ch[j+1]))
			j=(j+1)%n;
		//最左点
		while(Dot(ch[i+1]-ch[i],ch[k+1]-ch[i])>=Dot(ch[i+1]-ch[i],ch[k]-ch[i]))
			k=(k+1)%n;
		//最右点
		//1
		if(i==0)l=k;
		while(Dot(ch[i+1]-ch[i],ch[l+1]-ch[i])<=Dot(ch[i+1]-ch[i],ch[l]-ch[i]))	
			l=(l+1)%n;
		Point ll=GetLineProjection(ch[l],ch[i],ch[i+1]);
		Point kk=GetLineProjection(ch[k],ch[i],ch[i+1]);
		double h=DistanceToLine(ch[j],ch[i],ch[i+1]);
		double d=dis(ll,ch[i])+dis(ch[i],ch[i+1])+dis(kk,ch[i+1]);
		double cmp=h*d;
		if(ans>cmp){
			ans=cmp;
			MX[0]=ll,MX[1]=kk;
			MX[2]=kk+Normal(ch[i+1]-ch[i])*h;
			MX[3]=ll+Normal(ch[i+1]-ch[i])*h;
		}
	}
	return ans;	
} 
/*-----------------------------------------------------------------------------------*/
//半平面
struct Hplane{
	Point p;//直线上一点  
	Vector v;//方向向量 他的左边是半平面
	double ang;//极角
	Hplane(){};
	Hplane(Point p,Vector v):p(p),v(v){ang=atan2(v.y,v.x);}
	bool operator < (Hplane &L){return ang<L.ang;}//用于排序 
}; 
//p是否在半平面内 
bool OnLeft(Hplane L,Point p){return sgn(Cross(L.v,p-L.p))>0;}
//半平面交点 
Point Cross_point(Hplane a,Hplane b){
	Vector u=a.p-b.p;
	double t=Cross(b.v,u)/Cross(a.v,b.v);
	return a.p+a.v*t;
} 
//求半平面交凸包 
int HalfplaneIntersection(Hplane* L, int n, Point* poly){
    sort(L, L + n);//按照极角排序
    int fst = 0, lst = 0;//双端队列的第一个元素和最后一个元素
    Point *P = new Point[n];//p[i] 为 q[i]与q[i + 1]的交点
    Hplane *q = new Hplane[n];//双端队列
    q[fst = lst = 0] = L[0];//初始化为只有一个半平面L[0]
    for(int i = 1; i < n; ++i){
        while(fst < lst && !OnLeft(L[i], P[lst - 1])) --lst;
        while(fst < lst && !OnLeft(L[i], P[fst])) ++fst;
        q[++lst] = L[i];
        if(fabs(Cross(q[lst].v, q[lst - 1].v))<eps){//这里改了，更保证精度准确 
            //两向量平行且同向，取内侧一个
            --lst;
            if(OnLeft(q[lst], L[i].p)) q[lst] = L[i];
        }
        if(fst < lst)
            P[lst - 1] = Cross_point(q[lst - 1], q[lst]);
    }
    while(fst < lst && !OnLeft(q[fst], P[lst - 1])) --lst;
    //删除无用平面
    if(lst - fst <= 1)
		return 0;	
	//空集
    P[lst] = Cross_point(q[lst], q[fst]);//计算首尾两个半平面的交点
    //从deque复制到输出中
    int m = 0;
    for(int i = fst; i <= lst; ++i) poly[m++] = P[i];
    return m;
}
//将边往里推r的距离 
void PushIn(Hplane *poly,double r,int n,Hplane *C_poly){
	for(int i=0;i<n;i++){
		C_poly[i]=poly[i];
		C_poly[i].p=poly[i].p+Normal(poly[i].v)*r;
	}
}
/*------------------------------------------------------------------------------------------*/
//三维点
struct Point3{
	double x,y,z;
	Point3(){}
	Point3(double x,double y,double z):x(x),y(y),z(z){}
}; 
//三维向量
typedef Point3 Vector3;
//运算
Vector3 operator + (Vector3 A, Vector3 B){
    return Vector3(A.x+B.x, A.y+B.y,A.z+B.z);
}
Vector3 operator - (Vector3 A, Vector3 B){
    return Vector3(A.x-B.x, A.y-B.y,A.z-B.z);
}
Vector3 operator * (Vector3 A, double p){
    return Vector3(A.x*p, A.y*p,A.z*p);
}
Vector3 operator / (Vector3 A, double p){
    return Vector3(A.x/p, A.y/p,A.z/p);
}
bool operator == (Point3 A,Point3 B){
	return sgn(A.x-B.x)==0&&sgn(A.y-B.y)==0&&sgn(A.z-B.z);
}
//向量数量积  向量α在向量β的投影于向量β的长度乘积（带方向）
double Dot(Vector3 A, Vector3 B){
    return A.x*B.x + A.y*B.y+A.z*B.z;
}
//向量向量积  向量α与β所张成的平行四边形的有向面积
Vector3 Cross(Vector3 A, Vector3 B){
    return Point3(A.y*B.z-A.y*B.x,A.x*B.z-A.z*B.x,A.x*B.y-A.y*B.x);
}
//取模
double Length(Vector3 A){
    return sqrt(Dot(A, A));
}
//计算夹角
double Angle(Vector3 A, Vector3 B){
    return acos(Dot(A, B) / Length(A) / Length(B));
}
//两点距离
double dis(Point3 a,Point3 b){
	return sqrt((a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y)+(a.z-b.z)*(a.z-b.z));
}
//计算三角形面积*2
double Area2(Point3 A,Point3 B,Point3 C){
	return Length(Cross(B-A,C-A));
} 
/*-----------------------------------------------------------------------------------------*/
//三维线
struct Line3{
	Point3 p,v;
	Line3(){}
	Line3(Point3 p,Point3 v):p(p),v(v){}
}; 
//判断点是否在线上
bool PointOnline(Line3 A,Point3 a){
	return sgn(Length(Cross(A.p-a,A.v-a)))==0&&sgn(Dot(A.p-a,A.v-a))==0;
}
//点到直线的投影
Point3  GetLineProjection(Point3 p,Point3 a,Point3 b){
	double k=Dot(b-a,p-a)/Dot(b-a, b-a);
	return a+(b-a)*k;
} 
//点到直线的距离
double  DistanceToLine(Point3 p,Point3 a,Point3 b){
	return dis(p,GetLineProjection(p,a,b));
}
//点到线段的距离
double  DistanceToSegment(Point3 p,Point3 a,Point3 b){
	if(sgn(Dot(p-a,b-a))<0||sgn(Dot(p-b,a-b))<0){
		return min(dis(a,p),dis(b,p));
	}
	return DistanceToLine(p,a,b);
}
/*-----------------------------------------------------------------------------------*/
//面
struct Plane{
	Point3 p1,p2,p3;
	Vector3 Pvec;
	Plane(){}
	Plane(Point3 p1,Point3 p2,Point3 p3):p1(p1),p2(p2),p3(p3){
		Pvec=Cross(p2-p1,p3-p1);
	}
}; 
//求法向量
Vector3 GetPvec(Point3 p1,Point3 p2,Point3 p3){
	return Cross(p2-p1,p3-p1);
} 
Vector3 GetPvec(Plane f){
	return Cross(f.p2-f.p1,f.p3-f.p1);
} 
//四点共面
bool Four_point_coplanar(Point3 A,Point3 B,Point3 C,Point3 D){
	return sgn(Dot(GetPvec(A,B,C),D-A))==0;	
} 
//两平面平行
bool Parallel(Plane f1,Plane f2){
	return Length(Cross(GetPvec(f1),GetPvec(f2)))<eps;
} 
//两平面垂直
bool Vertical(Plane f1,Plane f2){
	return sgn(Dot(GetPvec(f1),GetPvec(f2)))==0;
}  
//直线与平面的交点
int Line_cross_plane(Line3 u,Plane f,Point3 &p){
	Point3 v=GetPvec(f);
	double x=Dot(v,u.v-f.p1);
	double y=Dot(v,u.p-f.p1);
	double d=x-y;
	if(sgn(x)==0&&sgn(y)==0)return -1;//u在f上
	if(sgn(d)==0)return 0;//平行
	p=((u.p*x)-(u.v*y))/d;
	return 1; 
} 
//求四面体体积*6
double volume4(Point3 a,Point3 b,Point3 c,Point3 d){
	return Dot(Cross(b-a,c-a),d-a);
} 
/*------------------------------------------------------------------*/
struct Circle{
	Point o;
	double r;
	Circle(){};
	Circle(Point a,Point b){
		o=(a+b)/2;
		r=dis(a,b)/2;
	}
};
/************************************************************************************/
Point p[5000],ch[5000];
int main()
{
	int n,q;
	cin>>n>>q;
	for(int i=0;i<n;i++)
		cin>>p[i].x>>p[i].y;
	int m=ConvexHull(p,n,ch);
//	for(int i=0;i<m;i++)
//		cout<<ch[i].x<<' '<<ch[i].y<<endl;
	while(q--)
	{
		Point a,b;
		cin>>a.x>>a.y>>b.x>>b.y;
		Circle c(a,b);
		double RR2=c.r*c.r/2;
		if(isPointInPolygon(c.o,ch,m)!=0)
		{
			printf("%.10lf\n",RR2);
			continue;
		}
		anticlockwise_sort(ch,m);
		ch[m]=ch[0];
		double ans=inf;
		//cout<<c.o.x<<' '<<c.o.y<<endl;
		for(int i=0;i<m;i++)
		{
			ans=min(ans,DistanceToSegment(c.o,ch[i],ch[i+1]));
			//cout<<ans<<endl;
		}
		printf("%.10lf\n",ans+RR2);
	}
} 
```


#

```C++
//#pragma GCC optimize("Ofast")

#include "bits/stdc++.h"


#define rep(i, n) for (int i = 0; i < (n); ++i)
#define rep1(i, n) for (int i = 1; i < (n); ++i)
#define rep1n(i, n) for (int i = 1; i <= (n); ++i)
#define repr(i, n) for (int i = (n) - 1; i >= 0; --i)
//#define pb push_back
#define eb emplace_back
#define all(a) (a).begin(), (a).end()
#define rall(a) (a).rbegin(), (a).rend()
#define each(x, a) for (auto &x : a)
#define ar array
#define vec vector
#define range(i, n) rep(i, n)

using namespace std;

using ll = long long;
using ull = unsigned long long;
using ld = long double;
using str = string;
using pi = pair<int, int>;
using pl = pair<ll, ll>;

using vi = vector<int>;
using vl = vector<ll>;
using vpi = vector<pair<int, int>>;
using vvi = vector<vi>;

int Bit(int mask, int b) { return (mask >> b) & 1; }

template<class T>
bool ckmin(T &a, const T &b) {
    if (b < a) {
        a = b;
        return true;
    }
    return false;
}

template<class T>
bool ckmax(T &a, const T &b) {
    if (b > a) {
        a = b;
        return true;
    }
    return false;
}

// [l, r)
template<typename T, typename F>
T FindFirstTrue(T l, T r, const F &predicat) {
    --l;
    while (r - l > 1) {
        T mid = l + (r - l) / 2;
        if (predicat(mid)) {
            r = mid;
        } else {
            l = mid;
        }
    }
    return r;
}


template<typename T, typename F>
T FindLastFalse(T l, T r, const F &predicat) {
    return FindFirstTrue(l, r, predicat) - 1;
}

const int INFi = 2e9;
const ll INF = 2e18;

bool Equal(ll A, ll B) {
    return A == B;
}

bool Less(ll A, ll B) {
    return A < B;
}

bool Greater(ll A, ll B) {
    return A > B;
}

bool LessOrEqual(ll A, ll B) {
    return A <= B;
}

bool GreaterOrEqual(ll A, ll B) {
    return A >= B;
}

const ld EPS = 1e-6;

bool Equal(ld A, ld B) {
    return abs(A - B) < EPS;
}

bool Less(ld A, ld B) {
    return A + EPS < B;
}

bool Greater(ld A, ld B) {
    return A > B + EPS;
}

bool LessOrEqual(ld A, ld B) {
    return A <= B + EPS;
}

bool GreaterOrEqual(ld A, ld B) {
    return A + EPS >= B;
}

template<typename T, typename Q>
bool LessOrEqual(T A, Q B) {
    using C = std::common_type_t<T, Q>;
    return LessOrEqual(static_cast<C>(A), static_cast<C>(B));
}

template<typename T, typename Q>
bool Equal(T A, Q B) {
    using C = std::common_type_t<T, Q>;
    return Equal(static_cast<C>(A), static_cast<C>(B));
}

template<typename T, typename Q>
bool Less(T A, Q B) {
    using C = std::common_type_t<T, Q>;
    return Less(static_cast<C>(A), static_cast<C>(B));
}

template<typename T, typename Q>
bool Greater(T A, Q B) {
    using C = std::common_type_t<T, Q>;
    return Greater(static_cast<C>(A), static_cast<C>(B));
}

template<typename T, typename Q>
bool GreaterOrEqual(T A, Q B) {
    using C = std::common_type_t<T, Q>;
    return GreaterOrEqual(static_cast<C>(A), static_cast<C>(B));
}

template<typename T>
ll sgn(T x) {
    if (Equal(x, 0)) return 0;
    return Less(x, 0) ? -1 : 1;
}


template<typename T>
struct Point {
    T x;
    T y;

    Point(T x_ = 0, T y_ = 0) : x(x_), y(y_) {}

    template<typename Q>
    Point(const Point<Q> &other) {
        x = static_cast<T>(other.x);
        y = static_cast<T>(other.y);
    }
    template<typename Q>
    Point(Point<Q> &&other) {
        x = static_cast<T>(other.x);
        y = static_cast<T>(other.y);
    }

    template<typename Q>
    Point<std::common_type_t<T, Q>> operator+(const Point<Q> &oth) const {
        return Point{x + oth.x, y + oth.y};
    }

    template<typename Q>
    Point<std::common_type_t<T, Q>> operator-(const Point<Q> &oth) const {
        return {x - oth.x, y - oth.y};
    }

    template<typename Q>
    bool operator==(const Point<Q> &oth) const {
        return x == oth.x && y == oth.y;
    }

    template<typename Q>
    bool operator<(const Point<Q> &oth) const {
        return make_pair(x, y) < make_pair(oth.x, oth.y);
    }

    template<typename Q>
    requires (is_integral_v<Q> || is_floating_point_v<Q>)
    Point<std::common_type_t<Q, T>> operator*(const Q &b) const {
        return {x * b, y * b};
    }
    template<typename Q>
    requires (is_integral_v<Q> || is_floating_point_v<Q>)
    Point<ld> operator/(const Q &b) const {
        return {(ld) x / b, (ld) y / b};
    }

    template<typename Q>
    std::common_type_t<Q, T> operator*(const Point<Q> &oth) const {
        return x * oth.y - y * oth.x;
    }

    template<typename Q>
    std::common_type_t<Q, T> operator%(const Point<Q> &oth) const {
        return x * oth.x + y * oth.y;
    }

    Point &operator+=(const Point &other) {
        x += other.x;
        y += other.y;
        return *this;
    }

    Point &operator-=(const Point &other) {
        x -= other.x;
        y -= other.y;
        return *this;
    }

    friend ostream &operator<<(ostream &stream, const Point &P) {
        stream << P.x << ' ' << P.y;
        return stream;
    }


    friend istream &operator>>(istream &stream, Point &P) {
        stream >> P.x >> P.y;
        return stream;
    }
};

template<typename T>
Point<T> rotateCW(const Point<T> &P) {
    return {P.y, -P.x};
}

template<typename T>
Point<T> rotateCCW(const Point<T> &P) {
    return {-P.y, P.x};
}

template<typename T, typename Q>
bool Equal(const Point<T> &a, const Point<Q> &b) {
    return Equal(a.x, b.x) && Equal(a.y, b.y);
}

template<typename T, typename Q>
bool Less(const Point<T> &a, const Point<Q> &b) {
    if (!Equal(a.x, b.x)) return Less(a.y, b.y);
    return Less(a.y, b.y);
}

template<typename T, typename Q>
bool Greater(const Point<T> &a, const Point<Q> &b) {
    if (!Equal(a.x, b.x)) return Greater(a.y, b.y);
    return Greater(a.y, b.y);
}

template<typename T>
Point<T> operator-(const Point<T> &a) {
    return {-a.x, -a.y};
}


template<typename T>
T len2(const Point<T> &a) {
    return a % a;
}

template<typename T>
ld len(const Point<T> &a) {
    return sqrtl(len2(a));
}

template<typename T, typename Q>
T dist2(const Point<T> &a, const Point<Q> &b) {
    return len2(a - b);
}

template<typename T, typename Q>
ld dist(const Point<T> &a, const Point<Q> &b) {
    return len(a - b);
}

using pt = Point<ll>;
using ptd = Point<ld>;

template<typename T = ld>
const Point<T> NULL_POINT = {T(-INFi - 1337), T(INFi + 228)};

template<typename T>
struct Segment;

template<typename T>
struct Ray;

template<typename T>
struct Line {
    T a, b, c;
    // ax + by = c
    template<class Q>
    Line(const Line<Q> &other) {
        a = other.a;
        b = other.b;
        c = other.c;
    }

    Line(const Point<T> &F, Point<T> V, bool isDirection = false) {
        if (!isDirection) {
            V -= F;
        }
        a = V.y;
        b = -V.x;
        c = a * F.x + b * F.y;
    }


    Line(const T &a1 = 0, const T &b1 = 0, const T &c1 = 0) {
        a = a1;
        b = b1;
        c = c1;
    }

    T get(const Point<T> &P) {
        return P.x * a + P.y * b - c;
    }

    template<class Q>
    explicit Line(const Segment<Q> &other) : Line(other.A, other.B, false) {
    }

    template<class Q>
    explicit Line(const Ray<Q> &other) : Line(other.A, other.V, true) {
    }

    pair<ptd, ptd> GetPointAndDirection() const {
        ptd V = {-b, a};
        ptd A;
        if (!Equal(a, 0)) {
            A.y = 0;
            A.x = c / (ld) a;
        } else if (!Equal(b, 0)) {
            A.x = 0;
            A.y = c / (ld) b;
        } else {
            assert(0);
        }
        return {A, V};
    }

    template<class Q>
    ptd Proj(const Point<Q> &P) const {
        auto [A, V] = GetPointAndDirection();
        ld value = (P - A) % V;
        value /= (ld) len2(V);
        return ptd(A) + (ptd(V) * value);
    }

    template<class Q>
    bool Contains(const Point<Q> &P) const {
        return Equal(GetValue(P), c);
    }

    template<typename Q>
    ld Dist(const Point<Q> &P) const {
        return dist(Proj(P), P);
    }

    template<typename Q>
    std::common_type_t<Q, T> GetValue(const Point<Q> &P) const {
        return a * P.x + b * P.y;
    }

    friend ostream &operator<<(ostream &stream, const Line &L) {
        stream << L.a << ' ' << L.b << ' ' << L.c;
        return stream;
    }


    friend istream &operator>>(istream &stream, Line &L) {
        stream >> L.a >> L.b >> L.c;
        return stream;
    }
};


template<typename Q, typename U>
ld Dist(const Point<Q> &A, const Line<U> &line) {
    return line.Dist(A);
}

template<typename Q, typename U>
Point<ld> Intersect(const Line<Q> &line1, const Line<U> &line2) {
    using C = std::common_type_t<Q, U>;
    C det = line1.a * line2.b - line1.b * line2.a;
    if (Equal(det, 0)) return NULL_POINT<ld>;
    C detx = line1.c * line2.b - line1.b * line2.c;
    C dety = line1.a * line2.c - line1.c * line2.a;
    return {(ld) detx / (ld) det, (ld) dety / (ld) det};
}

template<typename Q, typename U>
bool IsParallel(const Line<Q> &line1, const Line<U> &line2) {
    return Equal(line1.a * line2.b - line1.b * line2.a, 0);
}

template<typename Q, typename U>
ld Dist(const Line<Q> &line1, const Line<U> &line2) {
    if (IsParallel(line1, line2)) {
        return line1.Dist(line2.A);
    }
    return 0;
}


template<typename T, typename U, typename V>
bool IsCollinear(const Point<T> &a, const Point<U> &b, const Point<V> &c) {
    return Equal((c - a) * (b - a), 0);
}

template<typename T, typename U, typename V>
bool IsInside(T L, U R, V P) {
    return LessOrEqual(L, P) && LessOrEqual(P, R);
}

template<typename T>
struct Segment {
    Point<T> A, B;

    Segment(const Point<T> &a = {0, 0}, const Point<T> &b = {0, 0}) : A(a), B(b) {
    }


    template<class Q>
    Segment(const Segment<Q> &other) : A(other.A), B(other.B) {
    }

    T len2() const {
        return dist2(A, B);
    }

    ld len() const {
        return dist(A, B);
    }

    template<class Q>
    bool Contains(const Point<Q> &P) const {
        if (!IsCollinear(A, B, P)) {
            return false;
        }
        return IsInside(min(A.x, B.x), max(A.x, B.x), P.x) && IsInside(min(A.y, B.y), max(A.y, B.y), P.y);
    }

    template<typename Q>
    ld Dist(const Point<Q> &P) const {
        ld answer = min(dist(P, A), dist(P, B));
        ptd Ap = Line<ld>(*this).Proj(P);
        if (Contains(Ap)) {
            answer = dist(Ap, P);
        }
        return answer;
    }
};


template<typename Q, typename U>
ld Dist(const Point<Q> A, const Segment<U> &seg) {
    return seg.Dist(A);
}


template<typename U, typename V>
bool isIntersected(const Segment<U> &seg1, const Segment<V> &seg2) {
    ll s1 = sgn((seg1.B - seg1.A) * (seg2.A - seg1.A)) * sgn((seg1.B - seg1.A) * (seg2.B - seg1.A));
    if (s1 > 0) return false;
    ll s2 = sgn((seg2.B - seg2.A) * (seg1.A - seg2.A)) * sgn((seg2.B - seg2.A) * (seg1.B - seg2.A));
    if (s2 > 0) return false;
    return s1 < 0 || s2 < 0 || seg1.Contains(seg2.A) || seg1.Contains(seg2.B) || seg2.Contains(seg1.A);
}

template<typename U, typename V>
ld Dist(const Segment<U> &seg1, const Segment<V> &seg2) {
    if (isIntersected(seg1, seg2)) {
        return 0;
    }
    return min(min(seg1.Dist(seg2.A), seg1.Dist(seg2.B)), min(seg2.Dist(seg1.A), seg2.Dist(seg1.B)));
}

template<typename U, typename V>
bool isIntersected(const Segment<U> &seg, const Line<V> &line) {
    return sgn((seg.A - line.A) * line.V) * sgn((seg.B - line.A) * line.V) <= 0;
}

template<typename Q, typename U>
ld Dist(const Segment<Q> &seg, const Line<U> &line) {
    if (isIntersected(seg, line)) {
        return 0;
    }
    return min(line.Dist(seg.A), line.Dist(seg.B));
}

template<typename T>
struct Ray {
    Point<T> A, V;

    Ray(const Point<T> &a = {0, 0}, const Point<T> &v = {1, 0}, bool isDirection = false) {
        if (isDirection) {
            A = a;
            V = v;
        } else {
            A = a;
            V = v - a;
        }
    }

    template<class Q>
    Ray(const Ray<Q> &other) : A(other.A), V(other.V) {
    }

    template<class Q>
    Ray(const Segment<Q> &other) : A(other.A), V(other.B - other.A) {
    }

    template<class Q>
    bool Contains(const Point<Q> &P) const {
        return Equal(V * (P - A), 0) && GreaterOrEqual(V % (P - A), 0);
    }

    template<typename Q>
    ld Dist(const Point<Q> &P) const {
        ld answer = dist(P, A);
        ptd Ap = Line<ld>(*this).Proj(P);
        if (Contains(Ap)) {
            answer = dist(Ap, P);
        }
        return answer;
    }
};


template<typename Q, typename U>
ld Dist(const Point<Q> A, const Ray<U> &ray) {
    return ray.Dist(A);
}


template<typename U, typename V>
bool isIntersected(const Segment<U> &seg, const Ray<V> &ray) {
    ll sA = sgn((seg.A - ray.A) * ray.V);
    ll sB = sgn((seg.B - ray.A) * ray.V);
    if (sA * sB > 0) return false;
    if (sA == 0 || sB == 0) return ray.Contains(seg.A) || ray.Contains(seg.B);
    ll sAB = sgn((seg.A - ray.A) * (seg.B - ray.A));
    return sAB == 0 || sAB == sA;
}


template<typename U, typename V>
ld Dist(const Segment<U> &seg, const Ray<V> &ray) {
    if (isIntersected(seg, ray)) {
        return 0;
    }
    return min(min(ray.Dist(seg.A), ray.Dist(seg.B)), seg.Dist(ray.A));
}


template<typename U, typename V>
bool isIntersected(const Ray<U> &ray1, const Ray<V> &ray2) {
    auto mid = Intersect(Line<U>(ray1), Line<V>(ray2));
    if (ray1.Contains(mid) && ray2.Contains(mid)) return true;
    return ray1.Contains(ray2.A) || ray2.Contains(ray1.A);
}

template<typename U, typename V>
ld Dist(const Ray<U> &ray1, const Ray<V> &ray2) {
    if (isIntersected(ray1, ray2)) {
        return 0;
    }
    return min(ray1.Dist(ray2.A), ray2.Dist(ray1.A));
}

template<typename U, typename V>
bool isIntersected(const Ray<U> &ray, const Line<V> &line) {
    auto mid = Intersect(Line<U>(ray), line);
    if (ray.Contains(mid)) return true;
    return line.Contains(ray.A);
}

template<typename U, typename V>
ld Dist(const Ray<U> &ray, const Line<V> &line) {
    if (isIntersected(ray, line)) {
        return 0;
    }
    return line.Dist(ray.A);
}

const ld PI = atan2(0, -1);

template<typename T = ld>
struct Circle {
    Point<T> O;
    T R;

    Circle(const Point<T> &o = {0, 0}, const T &r = 0) : O(o), R(r) {}

    template<typename Q>
    Circle(const Circle<Q> &other) : O(other.O), R(other.R) {}

    template<typename Q>
    Circle(Circle<Q> &&other) : O(other.O), R(other.R) {}

    ld Area() const {
        return R * R * PI;
    }


    template<typename U, typename V>
    Point<ld> GetCircleCenterWithZero(const Point<U> &b,
                                      const Point<V> &c) {
        ld B = len2(b);
        ld C = len2(c);
        ld D = b * c;
        return {(c.y * B - b.y * C) / (2 * D),
                (b.x * C - c.x * B) / (2 * D)};
    }

    template<typename U, typename V, typename W>
    Circle(const Point<U> &A, const Point<V> &B,
           const Point<W> &C) {
        static_assert(std::is_same_v<T, ld>);
        O = GetCircleCenterWithZero(B - A, C - A);
        R = len(O);
        O += A;
    }

    template<typename U, typename V>
    Circle(const Point<U> &A, const Point<V> &B) {
        static_assert(std::is_same_v<T, ld>);
        O = (A + B) / (ld) 2;
        R = (ld) dist(A, B) / (ld) 2;
    }

    template<typename U>
    bool isInside(const Point<U> &P) const {
        return LessOrEqual(dist(P, O), R);
    }
};

// return (L, R) points in counter-clock-wise order related circle1
// if no intersect or coincide return (NULL_POINT, NULL_POINT)
template<typename T, typename U>
pair<Point<ld>, Point<ld>> Intersect(const Circle<T> &circle1, const Circle<U> &circle2) {
    if (Equal(circle1.O, circle2.O) && Equal(circle2.R, circle1.R)) return {NULL_POINT<ld>, NULL_POINT<ld>};
    auto d2 = dist2(circle2.O, circle1.O);
    if (Equal(d2, 0)) return {NULL_POINT<ld>, NULL_POINT<ld>};
    if (Less((circle1.R + circle2.R) * (circle2.R + circle1.R), d2) ||
        Less(d2, (circle1.R - circle2.R) * (circle1.R - circle2.R)))
        return {NULL_POINT<ld>, NULL_POINT<ld>};
    ld d = sqrtl(d2);
    ld A = (d2 - circle2.R * circle2.R + circle1.R * circle1.R) / (2 * d);
    ld B = sqrtl(max((ld) 0, circle1.R * circle1.R - A * A));
    Point<ld> V = (circle2.O - circle1.O) / d;
    Point<ld> M = circle1.O + V * A;
    V = rotateCCW(V) * B;
    return {M - V, M + V};
}

template<typename T, typename U>
pair<Point<ld>, Point<ld>> Intersect(const Circle<T> &circle, const Line<U> &line) {
    auto [a, b] = line.GetPointAndDirection();
    a -= circle.O;
    auto A = len2(b);
    auto B = a % b;
    auto C = len2(a) - circle.R * circle.R;
    auto D = B * B - A * C;
    if (Less(D, 0)) return {NULL_POINT<ld>, NULL_POINT<ld>};
    if (D < 0) D = 0;
    Point<ld> result = circle.O + a;
    return {result + b * (-B + sqrtl(D)) / (ld) A,
            result + b * (-B - sqrtl(D)) / (ld) A};
}

template<typename U, typename V>
ld IntersectionArea(const Circle<U> &circle1, const Circle<V> &circle2) {
    ld d = dist(circle1.O, circle2.O);
    if (GreaterOrEqual(d, circle1.R + circle2.R)) {
        return 0;
    }
    if (LessOrEqual(d + circle1.R, circle2.R)) {
        return circle1.Area();
    }
    if (LessOrEqual(d + circle2.R, circle1.R)) {
        return circle2.Area();
    }
    ld alpha = acos((circle1.R * circle1.R + d * d - circle2.R * circle2.R) / (2 * circle1.R * d)) * 2;
    ld beta = acos((circle2.R * circle2.R + d * d - circle1.R * circle1.R) / (2 * circle2.R * d)) * 2;
    return 0.5 * circle2.R * circle2.R * (beta - sin(beta)) +
           0.5 * circle1.R * circle1.R * (alpha - sin(alpha));
}


template<typename U, typename V>
ld UnionArea(const Circle<U> &circle1, const Circle<V> &circle2) {
    return circle1.Area() + circle2.Area() - IntersectionArea(circle1, circle2);
}

mt19937 rng(123212);

template<typename T, typename U>
bool IsContainsPoints(const Circle<T> &c, const vector<Point<U>> &pts) {
    for (auto &p: pts) {
        if (!c.isInside(p)) {
            return false;
        }
    }
    return true;
}

template<typename T>
Circle<ld> MinCircle(vector<Point<T>> &pts) {
    int n = pts.size();
    Circle<ld> C(pts[0], (ld) 0);
    for (int i = 1; i < n; i++) {
        if (!C.isInside(pts[i])) {
            C = Circle<ld>(pts[i], (ld) 0);
            for (int j = 0; j < i; j++) {
                if (!C.isInside(pts[j])) {
                    C = Circle<ld>(pts[i], pts[j]);
                    for (int k = 0; k < j; k++) {
                        if (!C.isInside(pts[k])) {
                            C = Circle<ld>(pts[i], pts[j], pts[k]);
                        }
                    }
                }
            }
        }
    }
    return C;
}


template<typename T>
vector<Point<T>> ConvexHull(vector<Point<T>> pts) {
    int min_idx = min_element(all(pts)) - pts.begin();
    swap(pts[0], pts[min_idx]);

    sort(pts.begin() + 1, pts.end(), [&](const Point<T> &a, const Point<T> &b) {
        auto val = (a - pts[0]) * (b - pts[0]);
        if (val != 0) return val > 0;
        return dist2(a, pts[0]) < dist2(b, pts[0]);
    });
    vector<Point<T>> convex_hull = {pts[0]};
    int sz = 0;
    for (int i = 1; i < (int) pts.size(); ++i) {
        while (sz && LessOrEqual((convex_hull[sz] - convex_hull[sz - 1]) * (pts[i] - convex_hull[sz]), 0)) {
            convex_hull.pop_back();
            --sz;
        }
        convex_hull.push_back(pts[i]);
        ++sz;
    }
    return convex_hull;
}

template<typename T, typename U>
bool VComp(const Point<T> &a, const Point<U> &b) {
    bool upA = a.y > 0 || (a.y == 0 && a.x >= 0);
    bool upB = b.y > 0 || (b.y == 0 && b.x >= 0);
    if (upA != upB) return upA;
    auto val = a * b;
    if (val != 0) return val > 0;
    return len2(a) < len2(b);
}

template<typename T, typename U>
bool VCompNoLen(const Point<T> &a, const Point<U> &b) {
    bool upA = a.y > 0 || (a.y == 0 && a.x >= 0);
    bool upB = b.y > 0 || (b.y == 0 && b.x >= 0);
    if (upA != upB) return upA;
    auto val = a * b;
    return val > 0;
}

template<typename T>
T SignedArea(vector<Point<T>> &pts) {
    int n = pts.size();
    T res = 0;
    rep(i, n) {
        res += pts[i] * pts[(i + 1) % n];
    }
    return res;
}

template<typename T>
T Area(vector<Point<T>> &pts) {
    return abs(SignedArea(pts));
}


template<typename T>
void NormalizeConvexPoly(vector<Point<T>> &A) {
    if (SignedArea(A) < 0) {
        reverse(all(A));
    }
    int min_idx = min_element(all(A), [&](const Point<T> &a, const Point<T> &b) {
        return make_pair(a.y, a.x) < make_pair(b.y, b.x);
    }) - A.begin();
    rotate(A.begin(), A.begin() + min_idx, A.end());
}

template<typename T>
vector<Point<T>> MinkowskiSum(vector<Point<T>> A, vector<Point<T>> B) {
    NormalizeConvexPoly(A);
    NormalizeConvexPoly(B);
    if (A.empty()) return B;
    if (B.empty()) return A;
    Point<T> S = A[0] + B[0];
    vector<Point<T>> edges;
    int n = A.size(), m = B.size();
    rep(i, n) edges.push_back(A[(i + 1) % n] - A[i]);
    rep(i, m) edges.push_back(B[(i + 1) % m] - B[i]);
    sort(all(edges), VComp<T, T>);
    rotate(edges.begin(), edges.end() - 1, edges.end());
    edges[0] = S;
    for (int i = 1; i < edges.size(); ++i) {
        edges[i] += edges[i - 1];
    }
    return edges;
}

template<typename T>
ld DistConvexPolygons(const vector<Point<T>> &A, vector<Point<T>> B) {
    for (auto &p: B) p = -p;
    auto C = MinkowskiSum(A, B);
    NormalizeConvexPoly(C);
    int n = C.size();
    bool ok = true;
    rep(i, n) ok &= ((C[i] * C[(i + 1) % n]) >= 0);
    if (ok) return 0;
    Point<T> mid(0, 0);
    ld d = dist(mid, C[0]);
    rep(i, n) d = min(d, Dist(mid, Segment(C[(i + 1) % n], C[i])));
    return d;
}


template<typename T, typename U>
pair<int, int> GetTangents(const vector<Point<T>> &poly, const Line<U> &line) {
    int n = poly.size();
    auto start = line.GetValue(poly[0]);
    bool isUp = line.GetValue(poly[1]) >= start;
    pair<int, int> result = {-1, -1};
    if (isUp) {
        result.first = FindLastFalse(0, n, [&](const int &i) {
            if (!i) return false;
            auto val = line.GetValue(poly[i]);
            if (val < start) return true;
            auto valp = line.GetValue(poly[i - 1]);
            if (valp > val) return true;
            return false;
        });
        result.second = FindLastFalse(0, n, [&](const int &i) {
            if (i <= 1) return false;
            auto val = line.GetValue(poly[i]);
            if (val >= start) return false;
            auto valp = line.GetValue(poly[i - 1]);
            if (valp < val) return true;
            return false;
        });
    } else {
        result.first = FindLastFalse(0, n, [&](const int &i) {
            if (i <= 1) return false;
            auto val = line.GetValue(poly[i]);
            if (val <= start) return false;
            auto valp = line.GetValue(poly[i - 1]);
            if (valp > val) return true;
            return false;
        });
        result.second = FindLastFalse(0, n, [&](const int &i) {
            if (!i) return false;
            auto val = line.GetValue(poly[i]);
            if (val > start) return true;
            auto valp = line.GetValue(poly[i - 1]);
            if (valp < val) return true;
            return false;
        });
    }
    for (int i: {0, 1, n - 2, n - 1}) {
        if (i < 0 || i >= (int) poly.size()) continue;
        if (line.GetValue(poly[result.first]) < line.GetValue(poly[i])) result.first = i;
        if (line.GetValue(poly[result.second]) > line.GetValue(poly[i])) result.second = i;
    }
    return result;
}

template<typename T, typename U>
pair<int, int> GetTangents(const vector<Point<T>> &poly, const Point<U> &P) {
    int n = poly.size();
    auto GetDirection = [&](int i, int j) {
        if (i < 0) i += n;
        if (j < 0) j += n;
        if (i >= n) i -= n;
        if (j >= n) j -= n;
        if (i == j) return 0;
        auto val = (poly[i] - P) * (poly[j] - P);
        if (val > 0) return -2;
        if (val < 0) return 2;
        auto q = dist2(poly[i], P) - dist2(poly[j], P);
        if (q > 0) return -1;
        if (q < 0) return 1;
        assert(false);
        return 0;
    };
    ll d01 = GetDirection(0, 1);
    pair<int, int> result = {-1, -1};
    if (d01 == -1) {
        result.first = 0;
    } else if (d01 == -2) {
        result.first = FindFirstTrue(0, n, [&](const int &i) {
            if (!i) return false;
            if (GetDirection(0, i) >= -1) return true;
            if (GetDirection(i, i + 1) == -2) return false;
            return true;
        }) % n;
    } else {
        assert(d01 == 1 || d01 == 2);
        result.first = FindFirstTrue(0, n, [&](const int &i) {
            ll v = GetDirection(0, i);
            assert(v != -1);
            if (v >= 2) return false;
            if (GetDirection(i, i + 1) == -2) return false;
            return true;
        }) % n;
    }
    assert(GetDirection(result.first, result.first + 1) >= -1 && GetDirection(result.first, result.first - 1) >= -1);
    if (d01 == 1) {
        result.second = 1;
    } else if (d01 == 2) {
        result.second = FindFirstTrue(0, n, [&](const int &i) {
            if (!i) return false;
            if (GetDirection(0, i) <= 1) return true;
            if (GetDirection(i, i + 1) >= 1) return false;
            return true;
        }) % n;
    } else {
        assert(d01 == -1 || d01 == -2);
        result.second = FindFirstTrue(0, n, [&](const int &i) {
            if (!i) return false;
            ll v = GetDirection(0, i);
            assert(v != 1);
            if (v <= -2) return false;
            if (GetDirection(i, i + 1) >= 1) return false;
            return true;
        }) % n;
    }
    assert(GetDirection(result.second, result.second + 1) <= 1 && GetDirection(result.second, result.second - 1) <= 1);
    return result;
}


vector<pt> read_poly() {
    int n;
    cin >> n;
    vector<pt> a(n);
    rep(i, n) cin >> a[i];

    return a;
}

ll check(const vector<pt> &S, int i, Line<ll> &ta) {
    int n = S.size();
    ll m = 0;
    for (int j = i - 1; j <= i + 1; ++j) {
        auto p = S[(j + n) % n];
        ll val = sgn(ta.get(p));
        if (val == 0) continue;
        if (m == 0) m = val;
        if (val != m) return 0;
    }
    assert(m);
    return m;
}

void solve() {
    int n;
    ll L, R;
    cin >> n >> L >> R;

    auto S = read_poly();

    int ns = S.size();

    vector<pair<ld, int>> events;

    int balance = 0;
    rep(_, n) {
        auto M = read_poly();

        int sz = M.size();

        vector<ld> bL, bR;

        rep(i, sz) {
            auto p = M[i];

            auto [j1, j2] = GetTangents(S, p);

            for (int j: {j1, j2}) {
                auto q = S[j];

                // p -> q

                Line<ll> ta(p, q);

                ll vS = check(S, j, ta);
                ll vM = check(M, i, ta);

                if (vS == 0 || vM == 0) continue;

                if (vS == vM) continue;

                if (p.y == q.y) {
//                    if (p.y == 0) {
//
//                    }
                    continue;
                }

                // q.y p.y 0
                if (q.y < p.y && p.y < 0) {

                    ld x = (ld) ta.c / ta.a;

                    if (vS > 0) {
                        bL.push_back(x);
//                        rq = min(rq, x);
                    } else {
                        bR.push_back(x);
//                        lq = max(lq, x);
                    }

                }


                if (q.y > p.y && p.y > 0) {

                    ld x = (ld) ta.c / ta.a;

                    if (vS < 0) {
                        bL.push_back(x);
//                        rq = min(rq, x);
                    } else {
                        bR.push_back(x);
//                        lq = max(lq, x);
                    }

                }
            }
        }

        if (bL.empty() && bR.empty()) {
            balance++;
            continue;
        }
        assert(!bL.empty() || !bR.empty());
        if (bL.empty()) {
            events.emplace_back(bR.front(), 1);
        } else if (bR.empty()) {
            events.emplace_back(bL.front(), -1);
            balance++;
        } else {
            balance++;
            events.emplace_back(bL.front(), -1);
            events.emplace_back(bR.front(), 1);
        }
    }

    events.emplace_back(L, 1);
    events.emplace_back(R, -1);

    int must = n + 1;
    for (auto &[x, y]: events) y *= -1;


    ld x = -INF;
    sort(all(events));

    ld ans = 0;


    bool ok = false;

    for (auto &[new_x, tp]: events) {
        if (true) {
            if (balance == must) {
                ans += new_x - x;
                if ((abs((ld) L - x) > EPS && abs((ld) R - x) > EPS) || abs(x - new_x) > EPS) ok = true;

//                cerr << x << ' ' << new_x << endl;
            }
            x = new_x;
        }
        balance -= tp;
    }
//    cerr << ok << endl;
    if (!ok) {
        cout << "-1\n";
        return;
    }

    cout << ans << '\n';
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout << setprecision(12) << fixed;
    int t = 1;

    cin >> t;
    rep(i, t) {
        solve();
    }
    return 0;
}
```
