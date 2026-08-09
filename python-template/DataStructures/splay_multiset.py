class _Node(object):
    __slots__ = ('value', 'count', 'size', 'left', 'right', 'parent')

    def __init__(self, value, parent=None):
        """Initialize the data structure."""
        self.value = value
        self.count = self.size = 1
        self.left = self.right = None
        self.parent = parent


def _size(node):
    """Run the internal size step."""
    return node.size if node else 0


def _pull(node):
    """Run the internal pull step."""
    node.size = node.count + _size(node.left) + _size(node.right)


class SplayMultiset(object):
    """Splay multiset: insert/discard, rank, kth, predecessor and successor."""

    def __init__(self):
        """Initialize the data structure."""
        self.root = None

    @staticmethod
    def _rotate(node):
        """Run the internal rotate step."""
        parent = node.parent
        grand = parent.parent
        if node is parent.left:
            parent.left = node.right
            if node.right:
                node.right.parent = parent
            node.right = parent
        else:
            parent.right = node.left
            if node.left:
                node.left.parent = parent
            node.left = parent
        parent.parent = node
        node.parent = grand
        if grand:
            if grand.left is parent:
                grand.left = node
            else:
                grand.right = node
        _pull(parent)
        _pull(node)

    def _splay(self, node):
        """Run the internal splay step."""
        while node.parent:
            parent = node.parent
            grand = parent.parent
            if grand:
                if (grand.left is parent) == (parent.left is node):
                    self._rotate(parent)
                else:
                    self._rotate(node)
            self._rotate(node)
        self.root = node

    def _find(self, value):
        """Run the internal find step."""
        node = self.root
        last = None
        while node:
            last = node
            if value == node.value:
                self._splay(node)
                return node
            node = node.left if value < node.value else node.right
        if last:
            self._splay(last)
        return None

    def insert(self, value):
        """Run the insert operation."""
        if not self.root:
            self.root = _Node(value)
            return
        node = self.root
        while True:
            if value == node.value:
                node.count += 1
                _pull(node)
                self._splay(node)
                return
            side = 'left' if value < node.value else 'right'
            child = getattr(node, side)
            if child:
                node = child
            else:
                child = _Node(value, node)
                setattr(node, side, child)
                self._splay(child)
                return

    def discard(self, value):
        """Run the discard operation."""
        node = self._find(value)
        if node is None:
            return False
        if node.count > 1:
            node.count -= 1
            _pull(node)
            return True
        left, right = node.left, node.right
        if left:
            left.parent = None
        if right:
            right.parent = None
        if not left:
            self.root = right
            return True
        self.root = left
        node = left
        while node.right:
            node = node.right
        self._splay(node)
        node.right = right
        if right:
            right.parent = node
        _pull(node)
        return True

    def rank(self, value):
        """Return 1-based rank: number of elements strictly smaller plus one."""
        node, result = self.root, 1
        while node:
            if value <= node.value:
                node = node.left
            else:
                result += _size(node.left) + node.count
                node = node.right
        return result

    def count_less(self, value):
        """Return the number of elements strictly smaller than value."""
        return self.rank(value) - 1

    def kth(self, index):
        """Return the 1-based k-th smallest value."""
        if index < 1 or index > len(self):
            raise IndexError('k is out of range')
        index -= 1
        node = self.root
        while node:
            left_size = _size(node.left)
            if index < left_size:
                node = node.left
            elif index < left_size + node.count:
                self._splay(node)
                return node.value
            else:
                index -= left_size + node.count
                node = node.right

    def predecessor(self, value):
        """Run the predecessor operation."""
        node, result = self.root, None
        while node:
            if node.value < value:
                result = node.value
                node = node.right
            else:
                node = node.left
        return result

    def successor(self, value):
        """Run the successor operation."""
        node, result = self.root, None
        while node:
            if node.value > value:
                result = node.value
                node = node.left
            else:
                node = node.right
        return result

    # C++ naming aliases.
    delete = discard
    prev = predecessor
    next = successor

    def __len__(self):
        """Implement the len operator."""
        return _size(self.root)
