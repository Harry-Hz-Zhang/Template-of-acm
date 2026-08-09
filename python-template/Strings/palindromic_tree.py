class PalindromicTree(object):
    """Palindromic automaton (eertree) for arbitrary hashable symbols."""

    def __init__(self):
        """Initialize the data structure."""
        self.length = [-1, 0]
        self.link = [0, 0]
        self.next = [{}, {}]
        self.occurrences = [0, 0]
        self.sequence = []
        self.last = 1

    def add(self, symbol):
        """Run the add operation."""
        position = len(self.sequence)
        self.sequence.append(symbol)
        current = self.last
        while position - self.length[current] - 1 < 0 or self.sequence[position - self.length[current] - 1] != symbol:
            current = self.link[current]
        if symbol in self.next[current]:
            self.last = self.next[current][symbol]
            self.occurrences[self.last] += 1
            return self.last
        node = len(self.length)
        self.length.append(self.length[current] + 2)
        self.link.append(1)
        self.next.append({})
        self.occurrences.append(1)
        self.next[current][symbol] = node
        if self.length[node] > 1:
            suffix = self.link[current]
            while position - self.length[suffix] - 1 < 0 or self.sequence[position - self.length[suffix] - 1] != symbol:
                suffix = self.link[suffix]
            self.link[node] = self.next[suffix][symbol]
        self.last = node
        return node

    @classmethod
    def from_sequence(cls, sequence):
        """Run the from sequence operation."""
        tree = cls()
        for symbol in sequence:
            tree.add(symbol)
        return tree

    def distinct_count(self):
        """Run the distinct count operation."""
        return len(self.length) - 2

    def propagate_occurrences(self):
        """Run the propagate occurrences operation."""
        result = self.occurrences[:]
        for node in sorted(range(2, len(self.length)), key=self.length.__getitem__, reverse=True):
            result[self.link[node]] += result[node]
        return result
