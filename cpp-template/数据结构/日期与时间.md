---
topic: "日期 时间 DAY"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## 日期 时间 DAY

 **精简版**

```cpp
int month_days[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

auto is_leap = [&](int y) -> bool {
	return (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
};
auto get_days = [&](int y, int m, int d) -> int {
	int res = 0;
	int y_ = y - 1;
	res += y_ * 365 + (y_ / 4 - y_ / 100 + y_ / 400);
	for (int i = 1; i < m; i++) {
		res += month_days[i] + (i == 2 && is_leap(y));
	}
	res += d;
	return res;
};
```


```C++
struct DAY {
  public:
    int y, m, d;      // 1-based
    int hh, mm, ss;      // 0..23, 0..59, 0..59
    DAY(int _y = 1, int _m = 1, int _d = 1, int _hh = 0, int _mm = 0, int _ss = 0)
        : y(_y), m(_m), d(_d), hh(_hh), mm(_mm), ss(_ss) { }
    static bool is_leap(int y) {
        return (y % 400 == 0) || (y % 4 == 0 && y % 100 != 0);
    }
    static int days_in_month(int y, int m) {
        static const int md[13] = {0,31,28,31,30,31,30,31,31,30,31,30,31};
        if (m == 2) return is_leap(y) ? 29 : 28;
        return md[m];
    }
    
    //判断当前时间是否合法
    static bool valid(int y, int m, int d, int hh = 0, int mm = 0, int ss = 0) {
        if (y < 1 || m < 1 || m > 12 || d < 1) return false;
        if (d > days_in_month(y, m)) return false;
        if (hh < 0 || hh > 23) return false;
        if (mm < 0 || mm > 59) return false;
        if (ss < 0 || ss > 59) return false;
        return true;
    }
    // 是年份 1..(y - 1) 的天数总和
    static inline i64 days_before_year(int y) {
        i64 n = (i64)y - 1;
        return 365LL * n + n / 4 - n / 100 + n / 400;
    }
    // 当年在 m 月之前的天数之和
    static inline int days_before_month(int y, int m) {
        static const int pref[13] = {0,0,31,59,90,120,151,181,212,243,273,304,334};
        static const int pref_leap[13] = {0,0,31,60,91,121,152,182,213,244,274,305,335};
        return (is_leap(y) ? pref_leap[m] : pref[m]);
    }
    // 计算当天是第从 0001-01-01 => 1 开始的第几天
    i64 to_ordinal() const {
        return days_before_year(y) + (i64)days_before_month(y, m) + (i64)d;
    }
    // 把第几天转化成具体的日期形式
    static DAY from_ordinal(i64 ord) {
        if (ord < 1) ord = 1;
        // Find y such that days_before_year(y) < ord <= days_before_year(y + 1)
        i64 lo = 1;
        i64 hi = max(1LL, ord / 365 + 2LL); // heuristic upper bound
        while (days_before_year((int)hi) < ord) hi <<= 1;
        while (lo + 1 < hi) {
            i64 mid = (lo + hi) >> 1;
            if (days_before_year((int)mid) < ord) lo = mid;
            else hi = mid;
        }
        int y = (int)lo;
        i64 day_of_year = ord - days_before_year(y);
        int m = 1;
        while (m <= 12) {
            int dim = days_in_month((int)y, m);
            if (day_of_year > dim) { day_of_year -= dim; ++m; }
            else break;
        }

        int d = (int)day_of_year;
        return DAY((int)y, m, d, 0, 0, 0);
    }
    // 跳转至下一天同一时刻 (time kept the same)
    DAY next_day() const {
        int ny = y, nm = m, nd = d + 1;
        if (nd > days_in_month(ny, nm)) {
            nd = 1; nm++;
            if (nm > 12) { nm = 1; ny++; }
        }
        return DAY(ny, nm, nd, hh, mm, ss);
    }
    // ISO weekday: Monday=1 .. Sunday=7
    // 计算具体的星期
    int iso_weekday() const {
        i64 ord = to_ordinal();
        return (int)(((ord - 1) % 7) + 1);
    }
    // Seconds since 0001-01-01 00:00:00 (0-based)
    // 从 0 开始的秒数
    i64 to_serial_seconds() const {
        i64 ord = to_ordinal();
        i64 sec = (ord - 1) * 86400LL + (i64)hh * 3600LL + (i64)mm * 60LL + (i64)ss;
        return sec;
    }
    // 从具体的秒数反推回具体的时间
    static DAY from_serial_seconds(i64 sec) {
        if (sec < 0) sec = 0LL;
        i64 ord = sec / 86400LL + 1LL;
        i64 rem = (sec % 86400LL);
        int hh = (int)(rem / 3600LL); rem %= 3600LL;
        int mm = (int)(rem / 60LL); int ss = (int)(rem % 60LL);
        DAY d = from_ordinal(ord);
        d.hh = hh; d.mm = mm; d.ss = ss;
        return d;
    }
    // 增加具体的天数
    DAY add_days(int k) const {
        i64 ord = to_ordinal();
        i64 nOrd = ord + (i64)k;
        if (nOrd < 1) nOrd = 1;
        DAY d2 = from_ordinal(nOrd);
        d2.hh = hh; d2.mm = mm; d2.ss = ss;
        return d2;
    }
    // 两个时间中相差的天数
    int diff_days(const DAY& other) const {
        return (int)(other.to_ordinal() - to_ordinal());
    }
    bool operator<(const DAY& o) const {
        if (y != o.y) return y < o.y;
        if (m != o.m) return m < o.m;
        if (d != o.d) return d < o.d;
        if (hh != o.hh) return hh < o.hh;
        if (mm != o.mm) return mm < o.mm;
        return ss < o.ss;
    }
    bool operator==(const DAY& o) const {
        return y == o.y && m == o.m && d == o.d && hh == o.hh && mm == o.mm && ss == o.ss;
    }
    string to_string() const {
        char buf[64];
        sprintf(buf, "%lld-%02lld-%02lld %02lld:%02lld:%02lld", (int64_t)y, (int64_t)m, (int64_t)d, (int64_t)hh, (int64_t)mm, (int64_t)ss);
        return string(buf);
    }
};
```
