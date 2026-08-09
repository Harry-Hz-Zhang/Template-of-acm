"""Li Chao tree for full-domain or segment-restricted line queries."""

from math import inf


class LiChaoTree:
    """Maintain y = slope*x + intercept on an integer x-domain.

    ``objective`` accepts ``"min"``, ``"max"``, or a pair comparator.
    Equal values use the smaller insertion id by default.
    """

    def __init__(self, left, right, objective="min"):
        """Initialize the data structure."""
        if left > right:
            raise ValueError("invalid domain")
        self.left_bound, self.right_bound = left, right
        self.lines = [None]
        self.node_line = [-1]
        self.left_child = [-1]
        self.right_child = [-1]
        if callable(objective):
            self._better = objective
            self._empty = None
        elif objective == "min":
            self._better = lambda a, b: a if a[0] < b[0] or (a[0] == b[0] and a[1] < b[1]) else b
            self._empty = inf
        elif objective == "max":
            self._better = lambda a, b: a if a[0] > b[0] or (a[0] == b[0] and a[1] < b[1]) else b
            self._empty = -inf
        else:
            raise ValueError("objective must be 'min', 'max', or a comparator")

    @staticmethod
    def _value(line, x):
        """Run the internal value step."""
        return line[0] * x + line[1]

    def _at(self, line_id, x):
        """Run the internal at step."""
        line = self.lines[line_id]
        return self._value(line, x), line_id

    def _new_node(self):
        """Run the internal new node step."""
        self.node_line.append(-1)
        self.left_child.append(-1)
        self.right_child.append(-1)
        return len(self.node_line) - 1

    def _insert(self, node, left, right, line_id, query_left, query_right):
        """Run the internal insert step."""
        if query_right < left or right < query_left:
            return
        if query_left <= left and right <= query_right:
            current = self.node_line[node]
            if current == -1:
                self.node_line[node] = line_id
                return
            middle = (left + right) // 2
            if self._better(self._at(line_id, middle), self._at(current, middle))[1] == line_id:
                self.node_line[node], line_id = line_id, current
            if left == right:
                return
            current = self.node_line[node]
            if self._better(self._at(line_id, left), self._at(current, left))[1] == line_id:
                child = self.left_child[node]
                if child == -1:
                    child = self.left_child[node] = self._new_node()
                self._insert(child, left, middle, line_id, query_left, query_right)
            elif self._better(self._at(line_id, right), self._at(current, right))[1] == line_id:
                child = self.right_child[node]
                if child == -1:
                    child = self.right_child[node] = self._new_node()
                self._insert(child, middle + 1, right, line_id, query_left, query_right)
            return

        middle = (left + right) // 2
        if query_left <= middle:
            child = self.left_child[node]
            if child == -1:
                child = self.left_child[node] = self._new_node()
            self._insert(child, left, middle, line_id, query_left, query_right)
        if middle < query_right:
            child = self.right_child[node]
            if child == -1:
                child = self.right_child[node] = self._new_node()
            self._insert(child, middle + 1, right, line_id, query_left, query_right)

    def add_segment(self, slope, intercept, left=None, right=None):
        """Insert a line active only on the closed interval [left, right]."""
        left = self.left_bound if left is None else max(self.left_bound, left)
        right = self.right_bound if right is None else min(self.right_bound, right)
        line_id = len(self.lines)
        self.lines.append((slope, intercept))
        if left <= right:
            self._insert(0, self.left_bound, self.right_bound, line_id, left, right)
        return line_id

    def add_line(self, slope, intercept):
        """Run the add line operation."""
        return self.add_segment(slope, intercept)

    def _query(self, node, left, right, x):
        """Run the internal query step."""
        current = self.node_line[node]
        answer = (self._empty, -1) if current == -1 else self._at(current, x)
        if left == right:
            return answer
        middle = (left + right) // 2
        child = self.left_child[node] if x <= middle else self.right_child[node]
        if child != -1:
            child_answer = self._query(child, left, middle, x) if x <= middle else self._query(child, middle + 1, right, x)
            if answer[1] == -1:
                answer = child_answer
            elif child_answer[1] != -1:
                answer = self._better(child_answer, answer)
        return answer

    def query_with_id(self, x):
        """Run the query with id operation."""
        if x < self.left_bound or x > self.right_bound:
            raise ValueError("x is outside the domain")
        return self._query(0, self.left_bound, self.right_bound, x)

    def query(self, x):
        """Run the query operation."""
        return self.query_with_id(x)[0]
