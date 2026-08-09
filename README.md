# ACM/ICPC 算法模板库

笔者打了两年 xcpc，留下了一些笔记 + 板子，可以供大家学习借鉴

有些部分的代码可能来自别人的模板，也有些地方不是很全，同时也欢迎大家补充。

**不保证模板的完全正确，请一定在使用前进行自测。**

## 目录树

<pre>
<a href="./">Template-of-acm</a>
├── <a href="cpptemplate/">cpptemplate/</a> (C++ 算法模板与 Markdown 讲解)
│   ├── <a href="cpptemplate/Supplements/">Supplements/</a>
│   ├── <a href="cpptemplate/NumberTheory/">NumberTheory/</a>
│   ├── <a href="cpptemplate/BasicAlgorithms/">BasicAlgorithms/</a>
│   ├── <a href="cpptemplate/Combinatorics/">Combinatorics/</a>
│   ├── <a href="cpptemplate/LinearAlgebra/">LinearAlgebra/</a>
│   ├── <a href="cpptemplate/Polynomial/">Polynomial/</a>
│   ├── <a href="cpptemplate/Geometry/">Geometry/</a>
│   ├── <a href="cpptemplate/Graph/">Graph/</a>
│   ├── <a href="cpptemplate/DataStructures/">DataStructures/</a>
│   ├── <a href="cpptemplate/DynamicProgramming/">DynamicProgramming/</a>
│   ├── <a href="cpptemplate/Strings/">Strings/</a>
│   ├── <a href="cpptemplate/GameTheory/">GameTheory/</a>
│   ├── <a href="cpptemplate/Probability/">Probability/</a>
│   ├── <a href="cpptemplate/Construct/">Construct/</a>
│   ├── <a href="cpptemplate/GroupTheory/">GroupTheory/</a>
│   ├── <a href="cpptemplate/Tricks/">Tricks/</a>
│   └── <a href="cpptemplate/BasicKnowledge/">BasicKnowledge/</a>
└── <a href="python-template/">python-template/</a> (Python 算法模板库，包含 111 个经典算法模板及全自动化测试驱动)
</pre>

### Python 模板使用与测试

`python-template/` 目录下包含了完整的 Python 算法模板库，涵盖数论、图论、数据结构、字符串、计算几何等 13 大类算法。
在该目录下运行以下命令即可对全量 111 个 Python 算法模板进行微分/对拍测试：

```bash
cd python-template
python3 _verify_all.py
```


## License

No explicit open-source license has been added yet. Unless the repository owner adds a license, all rights are reserved by default.
