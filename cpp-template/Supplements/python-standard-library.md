---
topic: "Python"
category: "language-standard-library"
source: "其他语言模板 + 标准库的使用.md"
---

# Python

## Time 类

### 总览对照

| C++ DAY 方法            | Python 对应                                 |
| --------------------- | ----------------------------------------- |
| `is_leap(y)`          | `calendar.isleap(y)`                      |
| `days_in_month(y, m)` | `calendar.monthrange(y, m)[1]`            |
| `valid(...)`          | 构造时自动抛异常                                  |
| `to_ordinal()`        | `date.toordinal()`                        |
| `from_ordinal(n)`     | `date.fromordinal(n)`                     |
| `iso_weekday()`       | `date.isoweekday()`                       |
| `to_serial_seconds()` | `datetime` 转 `timestamp`                  |
| `add_days(k)`         | `date + timedelta(days=k)`                |
| `diff_days(other)`    | `(d2 - d1).days`                          |
| `next_day()`          | `date + timedelta(days=1)`                |
| `to_string()`         | `date.strftime(格式)`                       |
| 解析字符串→日期              | `datetime.strptime(字符串, 格式)` ← **C++没有！** |

---

### Part 1：基础构造 & 合法性检查

```python
from datetime import date, datetime, timedelta
import calendar

# ============================================================
# 构造日期 / 时间
# ============================================================

# 只有日期（年月日）
d = date(2024, 3, 15)
print(d)          # 2024-03-15

# 日期 + 时间（年月日时分秒）
dt = datetime(2024, 3, 15, 10, 30, 45)
print(dt)         # 2024-03-15 10:30:45

# 非法日期会直接抛异常！不需要手写 valid()
try:
    bad = date(2024, 2, 30)   # 2月没有30号
except ValueError as e:
    print(e)      # day is out of range for month
    
try:
    bad = date(2024, 13, 1)   # 没有13月
except ValueError as e:
    print(e)

# 对应 C++ valid() 函数的写法：
def is_valid_date(y, m, d, hh=0, mm=0, ss=0):
    try:
        datetime(y, m, d, hh, mm, ss)
        return True
    except ValueError:
        return False

print(is_valid_date(2024, 2, 29))   # True（2024是闰年）
print(is_valid_date(2023, 2, 29))   # False（2023不是闰年）
```

---

### Part 2：闰年 & 每月天数

```python
import calendar

# ============================================================
# 对应 C++ is_leap()
# ============================================================
print(calendar.isleap(2024))    # True
print(calendar.isleap(2023))    # False
print(calendar.isleap(1900))    # False（能被100整除但不能被400整除）
print(calendar.isleap(2000))    # True（能被400整除）

# ============================================================
# 对应 C++ days_in_month()
# ============================================================
# monthrange(y, m) 返回 (该月第一天是星期几, 该月天数)
print(calendar.monthrange(2024, 2)[1])   # 29（闰年2月）
print(calendar.monthrange(2023, 2)[1])   # 28
print(calendar.monthrange(2024, 1)[1])   # 31

# 封装成函数（和C++完全对应）
def days_in_month(y, m):
    return calendar.monthrange(y, m)[1]
```

---

### Part 3：ordinal（核心！）

这对应 C++ 里最复杂的 `to_ordinal()` 和 `from_ordinal()`，Python 一行搞定：

```python
from datetime import date

# ============================================================
# 对应 C++ to_ordinal()
# 从 0001-01-01 开始计数，那天是第1天
# ============================================================
d = date(2024, 3, 15)
print(d.toordinal())           # 738960

print(date(1, 1, 1).toordinal())   # 1（第一天）
print(date(1, 1, 2).toordinal())   # 2

# ============================================================
# 对应 C++ from_ordinal()
# 从天数编号反推回具体日期
# ============================================================
print(date.fromordinal(738960))    # 2024-03-15
print(date.fromordinal(1))         # 0001-01-01

# ============================================================
# 竞赛实战用法：把日期转成整数处理，再转回来
# ============================================================
d1 = date(2024, 1, 1)
d2 = date(2024, 12, 31)

ord1 = d1.toordinal()
ord2 = d2.toordinal()
print(ord2 - ord1)                 # 365（2024全年天数-1）

# 遍历一段时间内的所有日期
for ord in range(d1.toordinal(), d2.toordinal() + 1):
    cur = date.fromordinal(ord)
    # 对 cur 做任何操作
```

---

### Part 4：星期计算

```python
from datetime import date

d = date(2024, 3, 15)

# 对应 C++ iso_weekday()
# Monday=1, Tuesday=2, ..., Sunday=7
print(d.isoweekday())     # 5（星期五）

# 另一种：weekday()
# Monday=0, Tuesday=1, ..., Sunday=6
print(d.weekday())        # 4（同一天，0-based）

# 星期名称
days_cn = ['一','二','三','四','五','六','日']
print(f"星期{days_cn[d.weekday()]}")   # 星期五

# 竞赛常用：判断某天是否是周末
def is_weekend(d: date) -> bool:
    return d.isoweekday() >= 6   # 6=Saturday, 7=Sunday

# 某月第一天是星期几
first_day_weekday = date(2024, 3, 1).isoweekday()
print(first_day_weekday)   # 5（2024年3月1日是星期五）
```

---

### Part 5：日期加减（timedelta，最重要！）

```python
from datetime import date, datetime, timedelta

d = date(2024, 3, 15)

# ============================================================
# 对应 C++ add_days(k)
# ============================================================
print(d + timedelta(days=10))    # 2024-03-25
print(d + timedelta(days=100))   # 2024-06-23（自动跨月跨年！）
print(d - timedelta(days=100))   # 2023-12-06（往前也行）

# ============================================================
# 对应 C++ next_day()
# ============================================================
next_day = d + timedelta(days=1)
print(next_day)    # 2024-03-16

# ============================================================
# 对应 C++ diff_days()
# ============================================================
d1 = date(2024, 1, 1)
d2 = date(2024, 12, 31)
diff = d2 - d1         # 结果是 timedelta 对象
print(diff.days)       # 365

# 两个datetime之差（包含时分秒）
dt1 = datetime(2024, 3, 15, 10, 0, 0)
dt2 = datetime(2024, 3, 16, 12, 30, 45)
delta = dt2 - dt1
print(delta.days)             # 1（天数部分）
print(delta.seconds)          # 9045（剩余秒数：2小时30分45秒）
print(delta.total_seconds())  # 108045.0（总秒数）

# timedelta 可以加减的单位
timedelta(days=1)
timedelta(weeks=2)              # 2周 = 14天
timedelta(hours=3)
timedelta(minutes=30)
timedelta(seconds=45)
timedelta(days=1, hours=2, minutes=30)   # 混合使用
```

---

### Part 6：字符串互转（C++ 没有，Python 强项！）

```python
from datetime import datetime

# ============================================================
# 字符串 → 日期（strptime）
# 竞赛输入格式各种各样，这个非常有用！
# ============================================================

# 标准格式
dt = datetime.strptime("2024-03-15", "%Y-%m-%d")
print(dt)    # 2024-03-15 00:00:00

# 有时分秒
dt = datetime.strptime("2024-03-15 10:30:45", "%Y-%m-%d %H:%M:%S")

# 斜杠分隔
dt = datetime.strptime("15/03/2024", "%d/%m/%Y")

# 中文格式（竞赛偶尔出现）
dt = datetime.strptime("2024年03月15日", "%Y年%m月%d日")

# ============================================================
# 日期 → 字符串（strftime）
# 对应 C++ to_string()
# ============================================================
from datetime import date
d = date(2024, 3, 15)

print(d.strftime("%Y-%m-%d"))      # 2024-03-15
print(d.strftime("%d/%m/%Y"))      # 15/03/2024
print(d.strftime("%Y年%m月%d日"))   # 2024年03月15日
print(d.strftime("%A"))            # Friday（英文星期）

# ============================================================
# 常用格式符速查
# ============================================================
# %Y  →  4位年份   2024
# %m  →  2位月份   03
# %d  →  2位日期   15
# %H  →  24小时制  10
# %M  →  分钟      30
# %S  →  秒        45
# %A  →  英文星期全名  Friday
# %a  →  英文星期缩写  Fri
# %j  →  年内第几天   075
```

---

### Part 7：C++ 里没有的强力功能

```python
import calendar
from datetime import date

# ============================================================
# 获取某月的完整日历（返回按周分组的列表）
# ============================================================
# monthcalendar(y, m) 返回 [[周一到周日], ...]
# 0 表示不属于这个月

cal = calendar.monthcalendar(2024, 3)
for week in cal:
    print(week)
# [0, 0, 0, 0, 1, 2, 3]
# [4, 5, 6, 7, 8, 9, 10]
# ...

# 竞赛应用：某月有几个完整的周末
def count_weekends(y, m):
    cal = calendar.monthcalendar(y, m)
    count = 0
    for week in cal:
        if week[5] != 0: count += 1   # 周六不为0
        if week[6] != 0: count += 1   # 周日不为0
    return count

# ============================================================
# 某年某月第N个星期X是几号
# 竞赛经典题：美国感恩节是11月第4个周四
# ============================================================
def nth_weekday_of_month(y, m, weekday, n):
    """
    weekday: 0=Monday, 6=Sunday
    n: 第几个（1-based）
    """
    cal = calendar.monthcalendar(y, m)
    days = [week[weekday] for week in cal if week[weekday] != 0]
    return days[n - 1]

thanksgiving = nth_weekday_of_month(2024, 11, 3, 4)   # 11月第4个周四
print(f"2024年感恩节：11月{thanksgiving}日")   # 11月28日

# ============================================================
# 两个日期之间有多少个特定星期几
# ============================================================
def count_weekday_between(d1: date, d2: date, weekday: int) -> int:
    """weekday: 1=Monday, 7=Sunday (isoweekday)"""
    total = (d2 - d1).days + 1
    # 方法：用整除直接算
    full_weeks, extra = divmod(total, 7)
    count = full_weeks
    start_wd = d1.isoweekday()
    for i in range(extra):
        if (start_wd - 1 + i) % 7 + 1 == weekday:
            count += 1
    return count

# 2024年有多少个星期五？
d1 = date(2024, 1, 1)
d2 = date(2024, 12, 31)
print(count_weekday_between(d1, d2, 5))   # 52

# ============================================================
# 今天的日期（竞赛本地调试用）
# ============================================================
print(date.today())          # 当前日期
print(datetime.now())        # 当前日期+时间
```

---

### Part 8：竞赛实战完整模板

```python
import sys
import calendar
from datetime import date, datetime, timedelta

input = lambda: sys.stdin.readline().strip()

# ============================================================
# 竞赛日期题万能工具箱
# ============================================================

def read_date(fmt="%Y-%m-%d"):
    """从输入读一个日期"""
    return datetime.strptime(input(), fmt).date()

def read_datetime(fmt="%Y-%m-%d %H:%M:%S"):
    """从输入读一个日期+时间"""
    return datetime.strptime(input(), fmt)

def diff_days(d1: date, d2: date) -> int:
    """d2 - d1 的天数（d2在后为正）"""
    return (d2 - d1).days

def add_days(d: date, k: int) -> date:
    return d + timedelta(days=k)

def is_leap(y: int) -> bool:
    return calendar.isleap(y)

def days_in_month(y: int, m: int) -> int:
    return calendar.monthrange(y, m)[1]

def to_ordinal(d: date) -> int:
    return d.toordinal()

def from_ordinal(n: int) -> date:
    return date.fromordinal(n)

def weekday_name_cn(d: date) -> str:
    names = ['一','二','三','四','五','六','日']
    return '星期' + names[d.weekday()]

# ============================================================
# 使用示例（对应各种竞赛题型）
# ============================================================
def example():
    # 题型1：给两个日期，求相差天数
    d1 = date(2024, 1, 1)
    d2 = date(2024, 12, 31)
    print(diff_days(d1, d2))   # 365

    # 题型2：给一个日期，求它是星期几
    d = date(2024, 3, 15)
    print(d.isoweekday())          # 5（星期五）
    print(weekday_name_cn(d))      # 星期五

    # 题型3：给一个日期加N天，求结果
    print(add_days(d, 100))        # 2024-06-23

    # 题型4：某年是否闰年
    print(is_leap(2024))           # True

    # 题型5：某月有多少天
    print(days_in_month(2024, 2))  # 29

    # 题型6：枚举一段时间（用ordinal最快）
    start = date(2024, 1, 1).toordinal()
    end   = date(2024, 12, 31).toordinal()
    for ord in range(start, end + 1):
        cur = date.fromordinal(ord)
        if cur.isoweekday() == 5:  # 所有星期五
            pass

example()
```
