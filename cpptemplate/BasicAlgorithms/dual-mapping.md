---
topic: "双映射"
category: "02-basic"
source: "基础算法 Basic.md"
---

# 双映射

```C++
// map_actual[i]：实际巢号 i 当前对应的内部编号
vector<int> map_actual(N + 1);
// map_internal[j]：内部编号 j 当前对应的实际巢号
vector<int> map_internal(N + 1);
for (int i = 1; i <= N; i++){
	map_actual[i] = i;
	map_internal[i] = i;
}
// pigeon[i] 表示鸽子 i 当前所属的内部编号
vector<int> pigeon(N + 1);
for (int i = 1; i <= N; i++){
	pigeon[i] = i;
}
while(Q--){
	int op;
	cin >> op;
	if(op == 1){
		int a, b;
		cin >> a >> b;
		// 移动鸽子 a 到实际巢 b：
		// 取出实际巢 b 当前对应的内部编号
		pigeon[a] = map_actual[b];
	} 
	else if(op == 2){
		int a, b;
		cin >> a >> b;
		// 交换实际巢 a 与实际巢 b：
		// 先记录交换前对应的内部编号
		int X = map_actual[a], Y = map_actual[b];
		// 交换 map_actual 中对应的值
		swap(map_actual[a], map_actual[b]);
		// 更新逆映射
		map_internal[X] = b;
		map_internal[Y] = a;
	} 
	else if(op == 3){
		int a;
		cin >> a;
		// 查询鸽子 a 所在的实际巢号：
		// 通过鸽子 a 的内部编号，再查 map_internal 得到实际巢号
		cout << map_internal[pigeon[a]] << "\n";
	}
}
```
