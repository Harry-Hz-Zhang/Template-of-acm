import random


class _Node(object):
    __slots__ = ('key', 'priority', 'count', 'size', 'left', 'right')

    def __init__(self, key):
        """Initialize the data structure."""
        self.key = key
        self.priority = random.random()
        self.count = 1
        self.size = 1
        self.left = None
        self.right = None


def _size(node):
    """Run the internal size step."""
    return node.size if node else 0


def _pull(node):
    """Run the internal pull step."""
    if node:
        node.size = node.count + _size(node.left) + _size(node.right)


def _rotate_right(node):
    """Run the internal rotate right step."""
    root = node.left
    node.left = root.right
    root.right = node
    _pull(node)
    _pull(root)
    return root


def _rotate_left(node):
    """Run the internal rotate left step."""
    root = node.right
    node.right = root.left
    root.left = node
    _pull(node)
    _pull(root)
    return root


class TreapMultiset(object):
    def __init__(self):
        """Initialize the data structure."""
        self.root = None

    def insert(self, key):
        """Run the insert operation."""
        def add(node):
            """Run the add operation."""
            if node is None:
                return _Node(key)
            if key == node.key:
                node.count += 1
            elif key < node.key:
                node.left = add(node.left)
                if node.left.priority < node.priority:
                    node = _rotate_right(node)
            else:
                node.right = add(node.right)
                if node.right.priority < node.priority:
                    node = _rotate_left(node)
            _pull(node)
            return node

        self.root = add(self.root)

    def erase(self, key):
        """Run the erase operation."""
        erased = [False]

        def remove(node):
            """Run the remove operation."""
            if node is None:
                return None
            if key < node.key:
                node.left = remove(node.left)
            elif key > node.key:
                node.right = remove(node.right)
            else:
                erased[0] = True
                if node.count > 1:
                    node.count -= 1
                elif node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                elif node.left.priority < node.right.priority:
                    node = _rotate_right(node)
                    node.right = remove(node.right)
                else:
                    node = _rotate_left(node)
                    node.left = remove(node.left)
            _pull(node)
            return node

        self.root = remove(self.root)
        return erased[0]

    def count_less(self, key):
        """Run the count less operation."""
        node = self.root
        answer = 0
        while node:
            if key <= node.key:
                node = node.left
            else:
                answer += _size(node.left) + node.count
                node = node.right
        return answer

    def rank(self, key):
        """Return the 1-based rank of key."""
        return self.count_less(key) + 1

    def predecessor(self, key):
        """Run the predecessor operation."""
        node = self.root
        answer = None
        while node:
            if node.key < key:
                answer = node.key
                node = node.right
            else:
                node = node.left
        return answer

    def successor(self, key):
        """Run the successor operation."""
        node = self.root
        answer = None
        while node:
            if node.key > key:
                answer = node.key
                node = node.left
            else:
                node = node.right
        return answer

    # C++ naming aliases.
    delete = erase
    prev = predecessor
    next = successor

    def kth(self, k):
        """Return the 1-based k-th key."""
        if k < 1 or k > _size(self.root):
            raise IndexError('k is out of range')
        k -= 1
        node = self.root
        while node:
            left_size = _size(node.left)
            if k < left_size:
                node = node.left
            elif k < left_size + node.count:
                return node.key
            else:
                k -= left_size + node.count
                node = node.right

    def __len__(self):
        """Implement the len operator."""
        return _size(self.root)
