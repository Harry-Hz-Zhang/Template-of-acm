---
topic: "AC自动机"
category: "09-data-structure"
source: "数据结构 Data Structure.md"
---

## AC自动机

```C++
class AhoCorasick {
    static constexpr int ALPHABET = 26;
    
  public:
    struct Node {
        int len, fail;
        std::array<int, ALPHABET> next;
        std::vector<int> ids;

        Node(): len(0), fail(0), next{} {}
    };
    vector<Node> t;
    AhoCorasick() {
        init();
    }
    void init() {
        t.assign(2, Node());
        t[0].next.fill(1);  // 哨兵节点，所有转移都指向 1
        t[0].len = -1;
    }
    int newNode() {
        t.emplace_back();
        return (int)t.size() - 1;
    }

    int add(const string &a, int id) {
        int p = 1;  // 从实际根节点 t[1] 开始
        for (auto c : a) {
            int x = c - 'a';
            if (t[p].next[x] == 0) {
                t[p].next[x] = newNode();
                t[t[p].next[x]].len = t[p].len + 1;
            }
            p = t[p].next[x];
        }
        t[p].ids.push_back(id);
        return p;
    }
    void get_fail() {
        queue<int> q;
        q.push(1);
        while (!q.empty()) {
            int x = q.front();
            q.pop();
            for (int i = 0; i < ALPHABET; i++) {
                if (t[x].next[i] == 0) {
                    // 如果没有该字符的转移，则继承自 fail 指针
                    t[x].next[i] = t[t[x].fail].next[i];
                } else {
                    // 如果有该字符的转移，则设置子节点的 fail
                    t[t[x].next[i]].fail = t[t[x].fail].next[i];
                    q.push(t[x].next[i]);
                }
            }
        }
    }
    // 返回当前节点的所有模式串ID引用
    vector<int>& Endid(int p) {
        return t[p].ids;
    }
    int next(int p, int x) {
        return t[p].next[x];
    }
    int fail(int p) {
        return t[p].fail;
    }
    int len(int p) {
        return t[p].len;
    }
    int size() {
        return (int)t.size();
    }
};

void solve()
{
    int n;
    while(cin >> n, n) {
        AhoCorasick ac;
        vector<string> pat(n + 1);
        vector<int> end(n + 1);
        for (int i = 1; i <= n; i++) {
            cin >> pat[i];
            end[i] = ac.add(pat[i], i);
        }
        ac.get_fail();
        string t;
        cin >> t;
        int u = 1;  // 从根节点开始
        vector<int> f(ac.size(), 0);
        for (auto ch : t) {
            int c = ch - 'a';
            u = ac.next(u, c);
            f[u]++;   // u节点的匹配次数++
        }
        vector<vector<int>> e(ac.size());
        for (int i = 2; i < ac.size(); i++) {
            int p = ac.fail(i);
            e[p].push_back(i);
        }
        auto dfs = [&](auto self, int u) -> void {
            for (auto v : e[u]) {
                self(self, v);
                f[u] += f[v];
            }
        };
        dfs(dfs, 1);
        int Max = 0;
        for (int i = 1; i <= n; i++) {
            Max = max(Max, f[end[i]]);
        }
        cout << Max << endl;
        for (int i = 1; i <= n; i++) {
            if (f[end[i]] == Max) {
                cout << pat[i] << endl;
            }
        }
    }
}
```
