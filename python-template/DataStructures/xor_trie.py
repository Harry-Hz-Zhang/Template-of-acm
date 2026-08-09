class XorTrie(object):
    def __init__(self, max_bit=30):
        """Initialize the data structure."""
        self.max_bit = max_bit
        self.children = [[-1, -1]]
        self.count = [0]

    def insert(self, value, amount=1):
        """Run the insert operation."""
        if amount <= 0:
            raise ValueError('amount must be positive')
        node = 0
        self.count[node] += amount
        for bit in range(self.max_bit, -1, -1):
            digit = (value >> bit) & 1
            if self.children[node][digit] == -1:
                self.children[node][digit] = len(self.children)
                self.children.append([-1, -1])
                self.count.append(0)
            node = self.children[node][digit]
            self.count[node] += amount

    def erase(self, value, amount=1):
        """Run the erase operation."""
        if amount <= 0:
            raise ValueError('amount must be positive')
        node = 0
        path = [0]
        for bit in range(self.max_bit, -1, -1):
            node = self.children[node][(value >> bit) & 1]
            if node == -1:
                return 0
            path.append(node)
        erased = min(amount, self.count[node])
        for node in path:
            self.count[node] -= erased
        return erased

    def max_xor(self, value):
        """Run the max xor operation."""
        if self.count[0] == 0:
            raise ValueError('trie is empty')
        node = 0
        answer = 0
        for bit in range(self.max_bit, -1, -1):
            digit = (value >> bit) & 1
            wanted = digit ^ 1
            next_node = self.children[node][wanted]
            if next_node != -1 and self.count[next_node] > 0:
                answer |= 1 << bit
                node = next_node
            else:
                node = self.children[node][digit]
        return answer

    def min_xor(self, value):
        """Return the minimum value of value xor y."""
        if self.count[0] == 0:
            raise ValueError('trie is empty')
        node = 0
        answer = 0
        for bit in range(self.max_bit, -1, -1):
            digit = (value >> bit) & 1
            same = self.children[node][digit]
            if same != -1 and self.count[same] > 0:
                node = same
            else:
                answer |= 1 << bit
                node = self.children[node][digit ^ 1]
        return answer

    def count_xor_less(self, value, limit):
        """Run the count xor less operation."""
        node = 0
        answer = 0
        for bit in range(self.max_bit, -1, -1):
            if node == -1:
                break
            value_bit = (value >> bit) & 1
            limit_bit = (limit >> bit) & 1
            if limit_bit:
                same = self.children[node][value_bit]
                if same != -1:
                    answer += self.count[same]
                node = self.children[node][value_bit ^ 1]
            else:
                node = self.children[node][value_bit]
        return answer
