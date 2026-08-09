class Prefix2D:
    """2D Prefix Sum array with 1-based indexing."""

    def __init__(self, a):
        """Build prefix sums from a 1-based rectangular matrix."""
        self.n = len(a) - 1
        self.m = len(a[0]) - 1 if self.n > 0 else 0
        self.s = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                self.s[i][j] = a[i][j] + self.s[i - 1][j] + self.s[i][j - 1] - self.s[i - 1][j - 1]

    def query(self, x1, y1, x2, y2):
        """Query submatrix sum in bounding region [x1..x2] x [y1..y2]."""
        if x1 > x2 or y1 > y2 or x1 > self.n or x2 < 1 or y1 > self.m or y2 < 1:
            return 0
        x1, x2 = max(1, min(x1, self.n)), max(1, min(x2, self.n))
        y1, y2 = max(1, min(y1, self.m)), max(1, min(y2, self.m))
        if x1 > x2 or y1 > y2:
            return 0
        return self.s[x2][y2] - self.s[x1 - 1][y2] - self.s[x2][y1 - 1] + self.s[x1 - 1][y1 - 1]

    def max_submatrix_sum(self, r, c):
        """Find the maximum sum of any submatrix with fixed dimensions r x c."""
        if r > self.n or c > self.m or r <= 0 or c <= 0:
            return 0
        return max(
            self.query(i - r + 1, j - c + 1, i, j)
            for i in range(r, self.n + 1)
            for j in range(c, self.m + 1)
        )


class Diff2D:
    """2D Difference Array with 1-based indexing."""

    def __init__(self, n=0, m=0):
        """Create an empty n-by-m difference matrix."""
        self.n, self.m = n, m
        self.d = [[0] * (m + 2) for _ in range(n + 2)]

    def insert(self, x1, x2, y1, y2, val=1):
        """Add val to all elements in submatrix [x1..x2] x [y1..y2]."""
        if x1 > x2 or y1 > y2 or x1 > self.n or x2 < 1 or y1 > self.m or y2 < 1:
            return
        x1, x2 = max(1, min(x1, self.n)), max(1, min(x2, self.n))
        y1, y2 = max(1, min(y1, self.m)), max(1, min(y2, self.m))
        if x1 > x2 or y1 > y2:
            return
        self.d[x1][y1] += val
        self.d[x1][y2 + 1] -= val
        self.d[x2 + 1][y1] -= val
        self.d[x2 + 1][y2 + 1] += val

    def to_array(self):
        """Reconstruct and return the 1-based 2D array."""
        a = [[0] * (self.m + 1) for _ in range(self.n + 1)]
        tmp = [row[:] for row in self.d]
        for i in range(1, self.n + 1):
            for j in range(1, self.m + 1):
                tmp[i][j] += tmp[i - 1][j] + tmp[i][j - 1] - tmp[i - 1][j - 1]
                a[i][j] = tmp[i][j]
        return a

    def to_prefix_2d(self):
        """Convert to Prefix2D instance for fast region sum queries."""
        return Prefix2D(self.to_array())
