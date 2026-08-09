from Strings.aho_corasick import AhoCorasick


class TrieNode(object):
    __slots__ = ('children', 'word_count', 'prefix_count')

    def __init__(self):
        """Initialize the data structure."""
        self.children = {}
        self.word_count = 0
        self.prefix_count = 0


class Trie(object):
    """Trie for strings or arbitrary sequences of hashable items."""

    def __init__(self):
        """Initialize the data structure."""
        self.root = TrieNode()

    def insert(self, sequence, count=1):
        """Run the insert operation."""
        if count <= 0:
            raise ValueError('count must be positive')
        node = self.root
        node.prefix_count += count
        for item in sequence:
            node = node.children.setdefault(item, TrieNode())
            node.prefix_count += count
        node.word_count += count
        return node.word_count

    def search(self, sequence):
        """Run the search operation."""
        node = self.root
        for item in sequence:
            node = node.children.get(item)
            if node is None:
                return 0
        return node.word_count

    def count_prefix(self, prefix):
        """Run the count prefix operation."""
        node = self.root
        for item in prefix:
            node = node.children.get(item)
            if node is None:
                return 0
        return node.prefix_count

    def starts_with(self, prefix):
        """Run the starts with operation."""
        return self.count_prefix(prefix) > 0

    def erase(self, sequence, count=1):
        """Run the erase operation."""
        if count <= 0:
            raise ValueError('count must be positive')
        items = tuple(sequence)
        path = [self.root]
        node = self.root
        for item in items:
            node = node.children.get(item)
            if node is None:
                return 0
            path.append(node)
        erased = min(count, node.word_count)
        if erased == 0:
            return 0
        node.word_count -= erased
        for current in path:
            current.prefix_count -= erased
        for index in range(len(items) - 1, -1, -1):
            parent = path[index]
            child = path[index + 1]
            if child.prefix_count == 0:
                del parent.children[items[index]]
            else:
                break
        return erased

    def erase_all(self, sequence):
        """Run the erase all operation."""
        items = tuple(sequence)
        count = self.search(items)
        return self.erase(items, count) if count else 0

    def longest_common_prefix(self, sequence):
        """Run the longest common prefix operation."""
        node = self.root
        result = []
        for item in sequence:
            node = node.children.get(item)
            if node is None or node.prefix_count == 0:
                break
            result.append(item)
        return ''.join(result) if isinstance(sequence, str) else result

    def get_all_with_prefix(self, prefix):
        """Run the get all with prefix operation."""
        is_string = isinstance(prefix, str)
        prefix_items = list(prefix)
        node = self.root
        for item in prefix_items:
            node = node.children.get(item)
            if node is None:
                return []
        results = []
        stack = [(node, prefix_items)]
        while stack:
            current, path = stack.pop()
            results.extend([path] * current.word_count)
            for item, child in current.children.items():
                if child.prefix_count:
                    stack.append((child, path + [item]))
        if is_string:
            return [''.join(items) for items in results]
        return [items[:] for items in results]
