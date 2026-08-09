from collections import deque


class AhoCorasick(object):
    """Generic Aho-Corasick automaton for hashable symbols."""

    def __init__(self, alphabet=None):
        """Create an empty automaton with an optional allowed alphabet."""
        self.alphabet = None if alphabet is None else set(alphabet)
        self.next = [{}]
        self.fail = [0]
        self.output = [[]]
        self.built = False
        self._pattern_count = 0

    def add(self, pattern, pattern_id=None):
        """Insert a pattern and return its pattern identifier."""
        if self.built:
            raise RuntimeError('add all patterns before build')
        state = 0
        for symbol in pattern:
            if self.alphabet is not None and symbol not in self.alphabet:
                raise ValueError('symbol is outside the alphabet')
            if symbol not in self.next[state]:
                self.next[state][symbol] = len(self.next)
                self.next.append({})
                self.fail.append(0)
                self.output.append([])
            state = self.next[state][symbol]
        if pattern_id is None:
            pattern_id = self._pattern_count
        self._pattern_count += 1
        self.output[state].append(pattern_id)
        return pattern_id

    def build(self):
        """Build failure links after all patterns are inserted."""
        queue = deque(self.next[0].values())
        while queue:
            state = queue.popleft()
            for symbol, child in self.next[state].items():
                fallback = self.fail[state]
                while fallback and symbol not in self.next[fallback]:
                    fallback = self.fail[fallback]
                self.fail[child] = self.next[fallback].get(symbol, 0)
                self.output[child].extend(self.output[self.fail[child]])
                queue.append(child)
        self.built = True

    def find_all(self, text):
        """Return zero-based end indices paired with pattern identifiers."""
        if not self.built:
            self.build()
        state = 0
        matches = []
        for index, symbol in enumerate(text):
            while state and symbol not in self.next[state]:
                state = self.fail[state]
            state = self.next[state].get(symbol, 0)
            for pattern_id in self.output[state]:
                matches.append((index, pattern_id))
        return matches

    def insert(self, pattern, pattern_id=None):
        """Compatibility alias for add."""
        return self.add(pattern, pattern_id)

    def search(self, text):
        """Return one-based end positions paired with pattern identifiers."""
        return [(position + 1, pattern_id) for position, pattern_id in self.find_all(text)]

    def count(self, text):
        """Return the total number of pattern occurrences in text."""
        return len(self.find_all(text))


class NextPositionAutomaton(object):
    """Find the next occurrence of symbols in a fixed sequence."""

    def __init__(self, sequence):
        """Build suffix transition maps in linear expected time."""
        self.sequence = sequence
        self.length = len(sequence)
        self.next = [None] * (self.length + 1)
        transition = {}
        for position in range(self.length, -1, -1):
            self.next[position] = transition.copy()
            if position:
                transition[sequence[position - 1]] = position

    def next_after(self, position, symbol):
        """Return the first 1-based occurrence after position, or n + 1."""
        if not 0 <= position <= self.length:
            raise IndexError('position is out of range')
        return self.next[position].get(symbol, self.length + 1)

    def is_subsequence(self, pattern, start=0):
        """Return whether pattern occurs as a subsequence after start."""
        position = start
        for symbol in pattern:
            position = self.next_after(position, symbol)
            if position > self.length:
                return False
        return True
