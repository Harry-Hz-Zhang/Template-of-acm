---
topic: "关于在字符串中查找某个子串并删除的操作"
category: "17-basic-knowledge"
source: "Z 基础知识.md"
---

# 关于在字符串中查找某个子串并删除的操作
```C++
for (int i = 0; i < n; i++) {  
	pos = 0; // 初始化查找位置为0  
	//从pos的位置开始查违禁词，查到就替换为特殊的符号
	while ((pos = ss.find(s[i], pos)) != std::string::npos) {  
		ss.erase(pos, s[i].size());  //删除字符串
		ss.insert(pos, sss);  //插入特殊的字符
		pos += sss.size(); // 从替换后的位置继续查找  
		count++;  
	}
}
```
***
