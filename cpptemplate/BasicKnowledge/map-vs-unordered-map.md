---
topic: "map 比 unorder_map 慢的多"
category: "17-basic-knowledge"
source: "Z 基础知识.md"
---

# map 比 unorder_map 慢的多

* 关于 `map` 以及 `unorder_map` 的一些使用方式：
	1. 为了减少一些代码上的不知名错误，不建议在查询时直接使用`map[ ]` 的形式，而是采用 `map.find() != map.end()` 的方式来写，这样很严谨。

***
