import itertools
import math


PI = math.pi
EPS = 1e-9


def sign(value, other=None):
    """Run the sign operation."""
    value = value if other is None else value - other
    return 0 if abs(value) <= EPS else (1 if value > 0 else -1)


dcmp = sign


class Point(object):
    """3D vector: dot product is *, cross product is ^."""

    __slots__ = ('x', 'y', 'z')

    def __init__(self, x=0.0, y=0.0, z=0.0):
        """Initialize the data structure."""
        self.x, self.y, self.z = x, y, z

    def __add__(self, other):
        """Implement the add operator."""
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """Implement the sub operator."""
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self):
        """Implement the neg operator."""
        return Point(-self.x, -self.y, -self.z)

    def __mul__(self, other):
        """Implement the mul operator."""
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y + self.z * other.z
        return Point(self.x * other, self.y * other, self.z * other)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        """Implement the truediv operator."""
        return Point(self.x / scalar, self.y / scalar, self.z / scalar)

    def __xor__(self, other):
        """Implement the xor operator."""
        return Point(self.y * other.z - self.z * other.y,
                     self.z * other.x - self.x * other.z,
                     self.x * other.y - self.y * other.x)

    def __eq__(self, other):
        """Implement the eq operator."""
        return isinstance(other, Point) and sign(self.x, other.x) == 0 \
               and sign(self.y, other.y) == 0 and sign(self.z, other.z) == 0

    def __iter__(self):
        """Implement the iter operator."""
        return iter((self.x, self.y, self.z))

    def __getitem__(self, index):
        """Implement the getitem operator."""
        return (self.x, self.y, self.z)[index]

    def __repr__(self):
        """Implement the repr operator."""
        return 'Point(%r, %r, %r)' % (self.x, self.y, self.z)

    def square(self):
        """Run the square operation."""
        return self * self

    def length(self):
        """Run the length operation."""
        return math.sqrt(self.square())


Vector = Point
Point3 = Point


def _point(value):
    """Run the internal point step."""
    return value if isinstance(value, Point) else Point(*value)


class Line(object):
    __slots__ = ('a', 'b')

    def __init__(self, a=(0.0, 0.0, 0.0), b=(0.0, 0.0, 0.0)):
        """Initialize the data structure."""
        self.a, self.b = _point(a), _point(b)


class Plane(object):
    __slots__ = ('a', 'b', 'c')

    def __init__(self, a=(0.0, 0.0, 0.0), b=(0.0, 0.0, 0.0), c=(0.0, 0.0, 0.0)):
        """Initialize the data structure."""
        self.a, self.b, self.c = _point(a), _point(b), _point(c)

    def normal(self):
        """Return a normal vector using the stored point order."""
        return (self.b - self.a) ^ (self.c - self.a)

    normalVector = normal


def distance(a, b):
    """Run the distance operation."""
    return (_point(a) - _point(b)).length()


dist = distance


def distance_point_to_plane(point, plane_point, normal):
    """Run the distance point to plane operation."""
    normal = _point(normal)
    if normal.square() <= EPS:
        raise ValueError('normal vector must be nonzero')
    return abs((_point(point) - _point(plane_point)) * normal) / normal.length()


def signed_tetrahedron_volume_six(a, b, c, d):
    """Run the signed tetrahedron volume six operation."""
    return (_point(b) - _point(a)) * ((_point(c) - _point(a)) ^ (_point(d) - _point(a)))


def central_angle(first, second):
    """Run the central angle operation."""
    first, second = _point(first), _point(second)
    denominator = first.length() * second.length()
    if denominator <= EPS:
        raise ValueError('zero vector has no central angle')
    return math.acos(max(-1.0, min(1.0, (first * second) / denominator)))


def spherical_cap_area(angle, radius=1.0):
    """Run the spherical cap area operation."""
    return 2.0 * PI * radius * radius * (1.0 - math.cos(angle))


spherical_cap_Area = spherical_cap_area


def convex_hull_faces(points):
    """Return outward triangular faces for points in general position."""
    points = [_point(point) for point in points]
    if len(points) < 4:
        raise ValueError('at least four noncoplanar points are required')
    for i, point in enumerate(points):
        if any(point == previous for previous in points[:i]):
            raise ValueError('duplicate points are not supported')
    order = list(range(len(points)))
    initial = None
    for combination in itertools.combinations(order, 4):
        if abs(signed_tetrahedron_volume_six(*(points[index] for index in combination))) > EPS:
            initial = list(combination)
            break
    if initial is None:
        raise ValueError('points must not be coplanar')
    order = initial + [index for index in order if index not in initial]
    interior = sum((points[index] for index in initial), Point()) / 4.0

    def orient(face):
        """Run the orient operation."""
        a, b, c = face
        normal = (points[b] - points[a]) ^ (points[c] - points[a])
        return (a, c, b) if normal * (interior - points[a]) > 0 else face

    a, b, c, d = initial
    faces = [orient(face) for face in ((a, b, c), (a, d, b), (a, c, d), (b, d, c))]
    for point_id in order[4:]:
        visible = []
        for face in faces:
            a, b, c = face
            if ((points[b] - points[a]) ^ (points[c] - points[a])) * (points[point_id] - points[a]) > EPS:
                visible.append(face)
        if not visible:
            continue
        boundary = set()
        for a, b, c in visible:
            for edge in ((a, b), (b, c), (c, a)):
                reverse = (edge[1], edge[0])
                if reverse in boundary:
                    boundary.remove(reverse)
                else:
                    boundary.add(edge)
        faces = [face for face in faces if face not in visible]
        faces.extend(orient((edge[0], edge[1], point_id)) for edge in boundary)
    return faces


def convex_hull_area(points):
    """Return the surface area of a general-position 3D convex hull."""
    converted = [_point(point) for point in points]
    return sum(((converted[b] - converted[a]) ^ (converted[c] - converted[a])).length() / 2.0
               for a, b, c in convex_hull_faces(converted))
