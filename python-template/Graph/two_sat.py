class TwoSat(object):
    def __init__(self, variable_count):
        """Initialize the data structure."""
        self.n = variable_count
        self.graph = [[] for _ in range(2 * variable_count)]

    @staticmethod
    def _node(variable, value):
        """Run the internal node step."""
        return 2 * variable + int(bool(value))

    def add_implication(self, a, a_value, b, b_value):
        """Run the add implication operation."""
        self.graph[self._node(a, a_value)].append(self._node(b, b_value))

    def add_or(self, a, a_value, b, b_value):
        """Run the add or operation."""
        self.add_implication(a, not a_value, b, b_value)
        self.add_implication(b, not b_value, a, a_value)

    def solve(self):
        """Run the solve operation."""
        n2 = 2 * self.n
        reverse_graph = [[] for _ in range(n2)]
        for u in range(n2):
            for v in self.graph[u]:
                reverse_graph[v].append(u)
        visited = [False] * n2
        order = []
        for start in range(n2):
            if visited[start]:
                continue
            visited[start] = True
            stack = [(start, 0)]
            while stack:
                u, index = stack[-1]
                if index < len(self.graph[u]):
                    v = self.graph[u][index]
                    stack[-1] = (u, index + 1)
                    if not visited[v]:
                        visited[v] = True
                        stack.append((v, 0))
                else:
                    order.append(u)
                    stack.pop()
        component = [-1] * n2
        component_count = 0
        for start in reversed(order):
            if component[start] != -1:
                continue
            component[start] = component_count
            stack = [start]
            while stack:
                u = stack.pop()
                for v in reverse_graph[u]:
                    if component[v] == -1:
                        component[v] = component_count
                        stack.append(v)
            component_count += 1
        assignment = [False] * self.n
        for variable in range(self.n):
            false_node = 2 * variable
            true_node = false_node + 1
            if component[false_node] == component[true_node]:
                return None
            assignment[variable] = component[true_node] > component[false_node]
        return assignment
