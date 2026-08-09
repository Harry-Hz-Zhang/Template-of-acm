"""Generic lazy segment tree with 1-based closed intervals.

Info must implement ``__add__`` and ``apply(tag, length)``. Tag must implement
``apply(other)``.
"""

from copy import deepcopy


class AddTag:
    """Range-add tag."""

    __slots__ = ("add",)

    def __init__(self, add=0):
        """Initialize the data structure."""
        self.add = add

    def apply(self, other):
        """Run the apply operation."""
        self.add += other.add

    def is_identity(self):
        """Run the is identity operation."""
        return self.add == 0


class SumInfo:
    """Range-sum info for ``AddTag`` or ``AffineTag``."""

    __slots__ = ("sum",)

    def __init__(self, value=0):
        """Initialize the data structure."""
        self.sum = value

    def __add__(self, other):
        """Implement the add operator."""
        return type(self)(self.sum + other.sum)

    def apply(self, tag, length):
        """Run the apply operation."""
        if hasattr(tag, "mul"):
            self.sum = self.sum * tag.mul + tag.add * length
        else:
            self.sum += tag.add * length


class AffineTag:
    """Affine tag ``x -> mul*x + add``."""

    __slots__ = ("mul", "add")

    def __init__(self, mul=1, add=0):
        """Initialize the data structure."""
        self.mul, self.add = mul, add

    def apply(self, other):
        """Run the apply operation."""
        self.mul *= other.mul
        self.add = self.add * other.mul + other.add

    def is_identity(self):
        """Run the is identity operation."""
        return self.mul == 1 and self.add == 0


class MinAddInfo:
    """Range minimum and position, used with ``AddTag``."""

    __slots__ = ("minimum", "position")

    def __init__(self, minimum=float("inf"), position=0):
        """Initialize the data structure."""
        self.minimum, self.position = minimum, position

    def __add__(self, other):
        """Implement the add operator."""
        if self.minimum < other.minimum:
            return type(self)(self.minimum, self.position)
        if other.minimum < self.minimum:
            return type(self)(other.minimum, other.position)
        return type(self)(self.minimum, min(self.position, other.position))

    def apply(self, tag, length=1):
        """Run the apply operation."""
        self.minimum += tag.add


class MinCountInfo:
    """Range minimum and its count, used with ``AddTag``."""

    __slots__ = ("minimum", "count")

    def __init__(self, minimum=float("inf"), count=0):
        """Initialize the data structure."""
        self.minimum, self.count = minimum, count

    def __add__(self, other):
        """Implement the add operator."""
        minimum = min(self.minimum, other.minimum)
        count = (self.count if self.minimum == minimum else 0) + (
            other.count if other.minimum == minimum else 0
        )
        return type(self)(minimum, count)

    def apply(self, tag, length=1):
        """Run the apply operation."""
        self.minimum += tag.add


class MaxAddInfo:
    """Range maximum and position, used with ``AddTag``."""

    __slots__ = ("maximum", "position")

    def __init__(self, maximum=float("-inf"), position=0):
        """Initialize the data structure."""
        self.maximum, self.position = maximum, position

    def __add__(self, other):
        """Implement the add operator."""
        if self.maximum > other.maximum:
            return type(self)(self.maximum, self.position)
        if other.maximum > self.maximum:
            return type(self)(other.maximum, other.position)
        return type(self)(self.maximum, min(self.position, other.position))

    def apply(self, tag, length=1):
        """Run the apply operation."""
        self.maximum += tag.add


class ChminTag:
    """Tag that applies ``value = min(value, cap)``."""

    __slots__ = ("cap",)

    def __init__(self, cap=float("inf")):
        """Initialize the data structure."""
        self.cap = cap

    def apply(self, other):
        """Run the apply operation."""
        self.cap = min(self.cap, other.cap)

    def is_identity(self):
        """Run the is identity operation."""
        return self.cap == float("inf")


class ChminInfo:
    """Range minimum info for ``chmin`` updates."""

    __slots__ = ("minimum", "position")

    def __init__(self, minimum=float("inf"), position=0):
        """Initialize the data structure."""
        self.minimum, self.position = minimum, position

    def __add__(self, other):
        """Implement the add operator."""
        if self.minimum < other.minimum:
            return type(self)(self.minimum, self.position)
        if other.minimum < self.minimum:
            return type(self)(other.minimum, other.position)
        return type(self)(self.minimum, min(self.position, other.position))

    def apply(self, tag, length=1):
        """Run the apply operation."""
        if self.minimum > tag.cap:
            self.minimum = tag.cap


class BinaryTag:
    """Binary assign/flip tag; ``assign=None`` means no assignment."""

    __slots__ = ("assign", "flip")

    def __init__(self, assign=None, flip=False):
        """Initialize the data structure."""
        self.assign, self.flip = assign, bool(flip)

    def apply(self, other):
        """Run the apply operation."""
        if other.assign is not None:
            self.assign = other.assign
            self.flip = other.flip
        elif other.flip:
            if self.assign is not None:
                self.assign ^= 1
            else:
                self.flip = not self.flip

    def is_identity(self):
        """Run the is identity operation."""
        return self.assign is None and not self.flip


class BinaryInfo:
    """Count of ones, used with ``BinaryTag``."""

    __slots__ = ("ones",)

    def __init__(self, ones=0):
        """Initialize the data structure."""
        self.ones = ones

    def __add__(self, other):
        """Implement the add operator."""
        return type(self)(self.ones + other.ones)

    def apply(self, tag, length):
        """Run the apply operation."""
        if tag.assign is not None:
            self.ones = tag.assign * length
        if tag.flip:
            self.ones = length - self.ones


class BitwiseAndTag:
    """Range bitwise-AND tag; all ones is the identity."""

    __slots__ = ("mask",)

    def __init__(self, mask=~0):
        """Initialize the data structure."""
        self.mask = mask

    def apply(self, other):
        """Run the apply operation."""
        self.mask &= other.mask

    def is_identity(self):
        """Run the is identity operation."""
        return self.mask == ~0


class BitwiseAndInfo:
    """C++ ``f/g`` info for range AND and first-bit search."""

    __slots__ = ("f", "g")

    def __init__(self, f=0, g=~0):
        """Initialize the data structure."""
        self.f, self.g = f, g

    def __add__(self, other):
        """Implement the add operator."""
        return type(self)((self.f & other.g) | (other.f & self.g), self.g & other.g)

    def apply(self, tag, length):
        """Run the apply operation."""
        self.g &= tag.mask
        self.f = self.f & tag.mask if length > 1 else ~self.g


class LazySegmentTree:
    """Lazy tree with custom Info/Tag types and 1-based closed intervals."""

    def __init__(self, data, info_type=None, tag_type=None,
                 merge=None, info_factory=None, tag_factory=None):
        """Initialize the data structure."""
        if isinstance(data, int):
            data = [0] * max(0, data)
        else:
            data = list(data)
        self.n = len(data)
        self._generic = any(value is not None and hasattr(value, "apply") for value in data)
        self._generic = self._generic or info_type is not None or tag_type is not None
        if self._generic:
            if info_type is None and data:
                info_type = type(data[0])
            if tag_type is None:
                tag_type = AddTag
            self.info_type = info_type
            self.tag_type = tag_type
            self._merge = merge or (lambda left, right: left + right)
            self._info_factory = info_factory or self._make_info
            self._tag_factory = tag_factory
        else:
            self.info_type = self.tag_type = None
            self._merge = lambda left, right: left + right
            self._info_factory = lambda value: value
            self._tag_factory = None
        self.info = [self._neutral_info() for _ in range(4 * self.n + 5)]
        self.tag = [self._neutral_tag() for _ in range(len(self.info))]
        self.tree = self.info
        self.lazy = self.tag
        if self.n:
            values = [self._info_factory(value) for value in data]
            self._build(1, 1, self.n, values)

    def _make_info(self, value=0):
        """Run the internal make info step."""
        if self.info_type is None:
            return value
        if isinstance(value, self.info_type):
            return value
        return self.info_type(value)

    def _make_tag(self, value=0):
        """Run the internal make tag step."""
        if self.tag_type is None:
            return value
        if isinstance(value, self.tag_type):
            return value
        return self.tag_type(value)

    def _neutral_info(self):
        """Run the internal neutral info step."""
        if self._generic:
            return self.info_type()
        return 0

    def _neutral_tag(self):
        """Run the internal neutral tag step."""
        if self._generic:
            return self.tag_type()
        return 0

    def _build(self, node, left, right, values):
        """Run the internal build step."""
        if left == right:
            self.info[node] = values[left - 1]
            return
        middle = (left + right) // 2
        self._build(node * 2, left, middle, values)
        self._build(node * 2 + 1, middle + 1, right, values)
        self._pull(node)

    def _pull(self, node):
        """Run the internal pull step."""
        self.info[node] = self._merge(self.info[node * 2], self.info[node * 2 + 1])

    def _tag_is_identity(self, value):
        """Run the internal tag is identity step."""
        if not self._generic:
            return value == 0
        checker = getattr(value, "is_identity", None)
        if checker is not None:
            return checker() if callable(checker) else bool(checker)
        neutral = self._neutral_tag()
        if value == neutral:
            return True
        fields = getattr(value, "__slots__", ())
        if fields:
            return all(getattr(value, field) == getattr(neutral, field) for field in fields)
        return getattr(value, "__dict__", None) == getattr(neutral, "__dict__", None)

    def _apply(self, node, left, right, value):
        """Run the internal apply step."""
        if self._tag_factory is not None:
            value = self._tag_factory(value)
        else:
            value = self._make_tag(value)
        if self._generic:
            updated_info = self.info[node].apply(value, right - left + 1)
            if updated_info is not None:
                self.info[node] = updated_info
            updated_tag = self.tag[node].apply(value)
            if updated_tag is not None:
                self.tag[node] = updated_tag
        else:
            self.info[node] += value * (right - left + 1)
            self.tag[node] += value

    def _push(self, node, left, right):
        """Run the internal push step."""
        if left == right or self._tag_is_identity(self.tag[node]):
            return
        middle = (left + right) // 2
        self._apply(node * 2, left, middle, self.tag[node])
        self._apply(node * 2 + 1, middle + 1, right, self.tag[node])
        self.tag[node] = self._neutral_tag()

    def _clip(self, left, right):
        """Run the internal clip step."""
        return max(1, left), min(self.n, right)

    def modify(self, index, value):
        """Assign a new Info value to a 1-based position."""
        if not 1 <= index <= self.n:
            raise IndexError("index is out of range")
        value = self._info_factory(value)

        def update(node, left, right):
            """Run the update operation."""
            if left == right:
                self.info[node] = value
                self.tag[node] = self._neutral_tag()
                return
            self._push(node, left, right)
            middle = (left + right) // 2
            if index <= middle:
                update(node * 2, left, middle)
            else:
                update(node * 2 + 1, middle + 1, right)
            self._pull(node)

        update(1, 1, self.n)

    def range_query(self, left, right):
        """Query a 1-based closed interval."""
        left, right = self._clip(left, right)
        if self.n == 0 or left > right:
            return self._neutral_info()

        def query(node, node_left, node_right):
            """Run the query operation."""
            if right < node_left or node_right < left:
                return self._neutral_info()
            if left <= node_left and node_right <= right:
                return self.info[node]
            self._push(node, node_left, node_right)
            middle = (node_left + node_right) // 2
            return self._merge(
                query(node * 2, node_left, middle),
                query(node * 2 + 1, middle + 1, node_right),
            )

        return query(1, 1, self.n)

    def range_apply(self, left, right, value):
        """Apply a tag to a 1-based closed interval."""
        left, right = self._clip(left, right)
        if self.n == 0 or left > right:
            return

        def update(node, node_left, node_right):
            """Run the update operation."""
            if right < node_left or node_right < left:
                return
            if left <= node_left and node_right <= right:
                self._apply(node, node_left, node_right, value)
                return
            self._push(node, node_left, node_right)
            middle = (node_left + node_right) // 2
            update(node * 2, node_left, middle)
            update(node * 2 + 1, middle + 1, node_right)
            self._pull(node)

        update(1, 1, self.n)

    def find_first(self, left, right, predicate):
        """Run the find first operation."""
        left, right = self._clip(left, right)
        if self.n == 0 or left > right:
            return -1

        def search(node, node_left, node_right):
            """Run the search operation."""
            if right < node_left or node_right < left or not predicate(self.info[node]):
                return -1
            if node_left == node_right:
                return node_left
            self._push(node, node_left, node_right)
            middle = (node_left + node_right) // 2
            result = search(node * 2, node_left, middle)
            return result if result != -1 else search(node * 2 + 1, middle + 1, node_right)

        return search(1, 1, self.n)

    def find_last(self, left, right, predicate):
        """Run the find last operation."""
        left, right = self._clip(left, right)
        if self.n == 0 or left > right:
            return -1

        def search(node, node_left, node_right):
            """Run the search operation."""
            if right < node_left or node_right < left or not predicate(self.info[node]):
                return -1
            if node_left == node_right:
                return node_left
            self._push(node, node_left, node_right)
            middle = (node_left + node_right) // 2
            result = search(node * 2 + 1, middle + 1, node_right)
            return result if result != -1 else search(node * 2, node_left, middle)

        return search(1, 1, self.n)

    @staticmethod
    def _score(value):
        """Run the internal score step."""
        return getattr(value, "sum", value)

    def search(self, target):
        """Find the first position whose prefix aggregate reaches target."""
        if self.n == 0 or target <= 0 or self._score(self.info[1]) < target:
            return -1
        node, left, right = 1, 1, self.n
        while left != right:
            self._push(node, left, right)
            middle = (left + right) // 2
            left_score = self._score(self.info[node * 2])
            if left_score >= target:
                node, right = node * 2, middle
            else:
                target -= left_score
                node, left = node * 2 + 1, middle + 1
        return left

    # Numeric convenience API.
    def add(self, left, right, delta):
        """Add delta to a 1-based closed interval in scalar mode."""
        self.range_apply(left, right, delta)

    def query(self, left, right):
        """Query a 1-based closed interval in scalar mode."""
        return self.range_query(left, right)
