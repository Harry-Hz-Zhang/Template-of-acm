---
topic: "三分"
category: "02-basic"
source: "基础算法 Basic.md"
---

# 三分

* 当函数是凸形函数时，二分法就无法适用，这时就需要用到三分法。
```C++
double solve(double l,double r) {
    while(fabs(r-l) > esp) {
        double lmid = l + (r-l)/3,rmid = r - (r-l)/3;
        if(val(lmid) >= val(rmid))  //求极大值
        /*if(val(lmid) <= val(rmid))    //求极小值 */
            r = rmid;
        else
            l = lmid;
    }
    return val(l);
}
```
