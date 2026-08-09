class SuffixAutomaton(object):
    def __init__(self):
        """Initialize the data structure."""
        self.next = [{}]
        self.link = [-1]
        self.length = [0]
        self.occurrences = [0]
        self.last = 0

    def extend(self, symbol):
        """Run the extend operation."""
        current = len(self.next)
        self.next.append({})
        self.length.append(self.length[self.last] + 1)
        self.link.append(0)
        self.occurrences.append(1)
        p = self.last
        while p != -1 and symbol not in self.next[p]:
            self.next[p][symbol] = current
            p = self.link[p]
        if p == -1:
            self.link[current] = 0
        else:
            q = self.next[p][symbol]
            if self.length[p] + 1 == self.length[q]:
                self.link[current] = q
            else:
                clone = len(self.next)
                self.next.append(self.next[q].copy())
                self.length.append(self.length[p] + 1)
                self.link.append(self.link[q])
                self.occurrences.append(0)
                while p != -1 and self.next[p].get(symbol) == q:
                    self.next[p][symbol] = clone
                    p = self.link[p]
                self.link[q] = self.link[current] = clone
        self.last = current

    @classmethod
    def from_sequence(cls, sequence):
        """Run the from sequence operation."""
        automaton = cls()
        for symbol in sequence:
            automaton.extend(symbol)
        return automaton

    def contains(self, sequence):
        """Run the contains operation."""
        state = 0
        for symbol in sequence:
            if symbol not in self.next[state]:
                return False
            state = self.next[state][symbol]
        return True

    def count_distinct_substrings(self):
        """Run the count distinct substrings operation."""
        return sum(self.length[state] - self.length[self.link[state]]
                   for state in range(1, len(self.next)))

    def propagate_occurrences(self):
        """Run the propagate occurrences operation."""
        order = sorted(range(1, len(self.next)), key=self.length.__getitem__, reverse=True)
        for state in order:
            self.occurrences[self.link[state]] += self.occurrences[state]
