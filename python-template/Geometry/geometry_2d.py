import bisect
import math
import random
from collections import deque
from fractions import Fraction
from functools import cmp_to_key


PI = math.pi
EPS = 1e-9
INF = float('inf')
Frac = Fraction


def sign(value, other=None):
    """Run the sign operation."""
    value = value if other is None else value - other
    return 0 if abs(value) <= EPS else (1 if value > 0 else -1)


class Point(object):
    """2D vector: +/-, scalar */ and /, dot *, cross ^."""

    __slots__ = ('x', 'y')

    def __init__(self, x=0.0, y=0.0):
        """Initialize the data structure."""
        self.x, self.y = x, y

    def __add__(self, other):
        """Implement the add operator."""
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Implement the sub operator."""
        return Point(self.x - other.x, self.y - other.y)

    def __neg__(self):
        """Implement the neg operator."""
        return Point(-self.x, -self.y)

    def __mul__(self, other):
        """Implement the mul operator."""
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        return Point(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        """Implement the truediv operator."""
        return Point(self.x / scalar, self.y / scalar)

    def __xor__(self, other):
        """Implement the xor operator."""
        return self.x * other.y - self.y * other.x

    def __eq__(self, other):
        """Implement the eq operator."""
        if not isinstance(other, Point):
            try:
                other = Point(other[0], other[1])
            except (TypeError, IndexError):
                return False
        return sign(self.x, other.x) == 0 and sign(self.y, other.y) == 0

    def __lt__(self, other):
        """Implement the lt operator."""
        return (self.x, self.y) < (other.x, other.y)

    def __iter__(self):
        """Implement the iter operator."""
        return iter((self.x, self.y))

    def __getitem__(self, index):
        """Implement the getitem operator."""
        return (self.x, self.y)[index]

    def __repr__(self):
        """Implement the repr operator."""
        return 'Point(%r, %r)' % (self.x, self.y)

    def square(self):
        """Run the square operation."""
        return self * self

    def length(self):
        """Run the length operation."""
        return math.sqrt(self.square())

    def polar_angle(self):
        """Run the polar angle operation."""
        angle = math.atan2(self.y, self.x)
        return angle + 2 * PI if angle < 0 else angle


Vector = Point


def _point(value):
    """Run the internal point step."""
    return value if isinstance(value, Point) else Point(value[0], value[1])


class Line(object):
    __slots__ = ('a', 'b', 's', 'v', 'deg')

    def __init__(self, a=(0.0, 0.0), b=(0.0, 0.0)):
        """Initialize the data structure."""
        self.a, self.b = _point(a), _point(b)
        self.s, self.v = self.a, self.b - self.a
        self.deg = math.atan2(self.v.y, self.v.x)


class Circle(object):
    __slots__ = ('O', 'r')

    def __init__(self, center=(0.0, 0.0), radius=0.0):
        """Initialize the data structure."""
        self.O, self.r = _point(center), radius

    def area(self):
        """Run the area operation."""
        return PI * self.r * self.r

    def point_at(self, angle):
        """Run the point at operation."""
        return Point(self.O.x + self.r * math.cos(angle), self.O.y + self.r * math.sin(angle))

    Point_at = point_at


def circle_point(circle, angle):
    """Run the circle point operation."""
    return circle.point_at(angle)


class Polygon(list):
    def __init__(self, points=()):
        """Initialize the data structure."""
        list.__init__(self, [_point(point) for point in points])

    def mid_point(self):
        """Run the mid point operation."""
        return Point(sum(point.x for point in self) / len(self),
                     sum(point.y for point in self) / len(self)) if self else Point()

    def perimeter(self):
        """Run the perimeter operation."""
        return sum(dist(self[i], self[(i + 1) % len(self)]) for i in range(len(self))) if self else 0

    def signed_area_x2(self):
        """Run the signed area x2 operation."""
        return sum(self[i] ^ self[(i + 1) % len(self)] for i in range(len(self))) if len(self) >= 3 else 0

    def signed_area(self):
        """Run the signed area operation."""
        return self.signed_area_x2() / 2.0

    def area(self):
        """Run the area operation."""
        return abs(self.signed_area_x2()) / 2.0

    def is_ccw(self):
        """Run the is ccw operation."""
        return sign(self.signed_area_x2()) > 0

    def make_ccw(self):
        """Run the make ccw operation."""
        if not self.is_ccw():
            self.reverse()
        return self

    def is_convex(self):
        """Run the is convex operation."""
        if len(self) < 3:
            return False
        turns = [sign((self[(i + 1) % len(self)] - self[i]) ^
                      (self[(i + 2) % len(self)] - self[(i + 1) % len(self)]))
                 for i in range(len(self))]
        turns = [turn for turn in turns if turn]
        return bool(turns) and all(turn == turns[0] for turn in turns)

    def in_polygon(self, point):
        """Run the in polygon operation."""
        point = _point(point)
        inside = False
        for i, a in enumerate(self):
            b = self[(i + 1) % len(self)]
            if point_on_segment(point, a, b):
                return 1
            if (a.y > point.y) != (b.y > point.y):
                x_at_y = a.x + (b.x - a.x) * (point.y - a.y) / (b.y - a.y)
                if x_at_y > point.x:
                    inside = not inside
        return 2 if inside else 0


def polar_sort(points, origin=(0.0, 0.0)):
    """Run the polar sort operation."""
    origin = _point(origin)
    points = [_point(point) for point in points]

    def compare(a, b):
        """Run the compare operation."""
        va, vb = a - origin, b - origin
        half_a = 0 if va.y > 0 or (sign(va.y) == 0 and va.x >= 0) else 1
        half_b = 0 if vb.y > 0 or (sign(vb.y) == 0 and vb.x >= 0) else 1
        if half_a != half_b:
            return -1 if half_a < half_b else 1
        cross = va ^ vb
        if sign(cross):
            return -1 if cross > 0 else 1
        return (va.square() > vb.square()) - (va.square() < vb.square())

    return sorted(points, key=cmp_to_key(compare))


def angle(first, second):
    """Run the angle operation."""
    first, second = _point(first), _point(second)
    denominator = first.length() * second.length()
    if denominator <= EPS:
        raise ValueError('zero vector has no angle')
    return math.acos(max(-1.0, min(1.0, (first * second) / denominator)))


def area(a, b, c):
    """Run the area operation."""
    return abs((_point(b) - _point(a)) ^ (_point(c) - _point(a))) / 2.0


def dist(a, b):
    """Run the dist operation."""
    return (_point(a) - _point(b)).length()


def dist_2(a, b):
    """Run the dist 2 operation."""
    return (_point(a) - _point(b)).square()


distance = dist
distance_squared = dist_2


def rotate(point, radians):
    """Run the rotate operation."""
    point = _point(point)
    cosine, sine = math.cos(radians), math.sin(radians)
    return Point(point.x * cosine - point.y * sine, point.x * sine + point.y * cosine)


def normal_vector(vector):
    """Run the normal vector operation."""
    vector = _point(vector)
    return Point(-vector.y, vector.x)


def point_on_line_left(point, line):
    """Run the point on line left operation."""
    return sign(line.v ^ (_point(point) - line.s)) > 0


left_test = point_on_line_left


def is_segment_intersect(first, second):
    """Run the is segment intersect operation."""
    return segment_intersection(first, second)[0] != 0


def point_on_segment(point, a, b):
    """Run the point on segment operation."""
    point, a, b = _point(point), _point(a), _point(b)
    vector = b - a
    return abs(vector ^ (point - a)) <= EPS and (point - a) * (point - b) <= EPS


def project(point, line):
    """Run the project operation."""
    point = _point(point)
    if line.v.square() <= EPS:
        return line.a
    return line.a + line.v * (((point - line.a) * line.v) / line.v.square())


foot_point = project


def reflection(point, line):
    """Run the reflection operation."""
    return project(point, line) * 2 - _point(point)


def line_intersection(line_a, line_b):
    """Run the line intersection operation."""
    denominator = line_a.v ^ line_b.v
    if abs(denominator) <= EPS:
        return None
    return line_a.s + line_a.v * (((line_b.s - line_a.s) ^ line_b.v) / denominator)


def _empty_intersection():
    """Run the internal empty intersection step."""
    return 0, Point(), Point()


def segment_intersection(line_a, line_b):
    """Return (0, -, -), (1, point, point), (2, left, right), or (3, point, point)."""
    va, vb = line_a.v, line_b.v
    if va.square() <= EPS:
        return (3, line_a.a, line_a.a) if point_on_segment(line_a.a, line_b.a, line_b.b) else _empty_intersection()
    if vb.square() <= EPS:
        return (3, line_b.a, line_b.a) if point_on_segment(line_b.a, line_a.a, line_a.b) else _empty_intersection()
    denominator = va ^ vb
    if abs(denominator) <= EPS:
        if abs(va ^ (line_b.a - line_a.a)) > EPS:
            return _empty_intersection()
        ta = ((line_b.a - line_a.a) * va) / va.square()
        tb = ((line_b.b - line_a.a) * va) / va.square()
        left, right = max(0.0, min(ta, tb)), min(1.0, max(ta, tb))
        if left > right + EPS:
            return _empty_intersection()
        first, second = line_a.a + va * left, line_a.a + va * right
        return (3, first, second) if first == second else (2, first, second)
    t = ((line_b.a - line_a.a) ^ vb) / denominator
    u = ((line_b.a - line_a.a) ^ va) / denominator
    if t < -EPS or t > 1 + EPS or u < -EPS or u > 1 + EPS:
        return _empty_intersection()
    point = line_a.a + va * t
    return (1 if EPS < t < 1 - EPS and EPS < u < 1 - EPS else 3, point, point)


def segment_intersection_points(a, b, c, d):
    """Run the segment intersection points operation."""
    kind, first, second = segment_intersection(Line(a, b), Line(c, d))
    return [] if kind == 0 else [first] if first == second else sorted((first, second))


def segments_intersect(a, b, c, d):
    """Run the segments intersect operation."""
    return segment_intersection(Line(a, b), Line(c, d))[0] != 0


def distance_point_to_line(point, line, end=None):
    """Run the distance point to line operation."""
    point = _point(point)
    line = Line(line, end) if end is not None else line
    if line.v.square() <= EPS:
        return dist(point, line.a)
    return abs(line.v ^ (point - line.a)) / line.v.length()


def distance_point_to_segment_2(point, a, b):
    """Run the distance point to segment 2 operation."""
    point, a, b = _point(point), _point(a), _point(b)
    vector, offset = b - a, point - a
    length_squared = vector.square()
    if length_squared <= EPS:
        return offset.square()
    projection = offset * vector
    if projection <= 0:
        return offset.square()
    if projection >= length_squared:
        return (point - b).square()
    return (vector ^ offset) ** 2 / length_squared


def distance_point_to_segment(point, a, b=None):
    """Run the distance point to segment operation."""
    if b is None:
        line = a
    else:
        line = Line(a, b)
    return math.sqrt(distance_point_to_segment_2(point, line.a, line.b))


def distance_segment_to_segment(first, second):
    """Run the distance segment to segment operation."""
    first, second = first if isinstance(first, Line) else Line(*first), second if isinstance(second, Line) else Line(*second)
    if segment_intersection(first, second)[0]:
        return 0.0
    return min(distance_point_to_segment(first.a, second), distance_point_to_segment(first.b, second),
               distance_point_to_segment(second.a, first), distance_point_to_segment(second.b, first))


def point_in_polygon(point, polygon):
    """Run the point in polygon operation."""
    result = Polygon(polygon).in_polygon(point)
    return 1 if result == 2 else 0 if result == 1 else -1


def convex_polygon_contains(polygon, point):
    """Return -1/0/1 for outside/boundary/inside a convex polygon."""
    polygon, point = Polygon(polygon), _point(point)
    n = len(polygon)
    if n == 0:
        return -1
    if n == 1:
        return 0 if polygon[0] == point else -1
    if n == 2:
        return 0 if point_on_segment(point, polygon[0], polygon[1]) else -1
    if polygon.signed_area_x2() < 0:
        polygon.reverse()
    first = (polygon[1] - polygon[0]) ^ (point - polygon[0])
    last = (polygon[-1] - polygon[0]) ^ (point - polygon[0])
    if first < -EPS or last > EPS:
        return -1
    left, right = 1, n - 1
    while right - left > 1:
        middle = (left + right) // 2
        if (polygon[middle] - polygon[0]) ^ (point - polygon[0]) >= -EPS:
            left = middle
        else:
            right = middle
    edge = (polygon[(left + 1) % n] - polygon[left]) ^ (point - polygon[left])
    if edge < -EPS:
        return -1
    return 0 if abs(first) <= EPS or abs(last) <= EPS or abs(edge) <= EPS else 1


def convex_hull(points, keep_collinear=False):
    """Run the convex hull operation."""
    points = sorted(_point(point) for point in points)
    unique = []
    for point in points:
        if not unique or point != unique[-1]:
            unique.append(point)
    if len(unique) <= 1:
        return Polygon(unique)

    def pop(last, point):
        """Run the pop operation."""
        turn = (last[-1] - last[-2]) ^ (point - last[-1])
        return turn < -EPS if keep_collinear else turn <= EPS

    lower = []
    for point in unique:
        while len(lower) >= 2 and pop(lower, point):
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(unique):
        while len(upper) >= 2 and pop(upper, point):
            upper.pop()
        upper.append(point)
    return Polygon(lower[:-1] + upper[:-1])


def segment_in_polygon(segment, polygon):
    """Run the segment in polygon operation."""
    line, polygon = segment if isinstance(segment, Line) else Line(*segment), Polygon(polygon)
    if point_in_polygon(line.a, polygon) < 0 or point_in_polygon(line.b, polygon) < 0:
        return False
    parameters = [0.0, 1.0]
    for i, point in enumerate(polygon):
        kind, first, second = segment_intersection(line, Line(point, polygon[(i + 1) % len(polygon)]))
        if kind in (1, 3):
            parameters.append(((first - line.a) * line.v) / line.v.square() if line.v.square() else 0.0)
        elif kind == 2:
            parameters.extend((((p - line.a) * line.v) / line.v.square() for p in (first, second)))
    parameters = sorted(set(max(0.0, min(1.0, value)) for value in parameters))
    return all(point_in_polygon(line.a + line.v * ((left + right) / 2.0), polygon) >= 0
               for left, right in zip(parameters, parameters[1:]))


def half_plane_intersection(lines):
    """Run the half plane intersection operation."""
    lines = [line if isinstance(line, Line) else Line(line[0], _point(line[0]) + _point(line[1])) for line in lines]
    ordered, filtered = sorted(lines, key=lambda line: line.deg), []
    for line in ordered:
        if filtered and abs(filtered[-1].v ^ line.v) <= EPS:
            if point_on_line_left(line.a, filtered[-1]):
                filtered[-1] = line
        else:
            filtered.append(line)
    active, intersections = deque(), deque()
    for line in filtered:
        while intersections and not point_on_line_left(intersections[-1], line):
            intersections.pop(); active.pop()
        while intersections and not point_on_line_left(intersections[0], line):
            intersections.popleft(); active.popleft()
        if active:
            point = line_intersection(active[-1], line)
            if point is None:
                return []
            intersections.append(point)
        active.append(line)
    while intersections and not point_on_line_left(intersections[-1], active[0]):
        intersections.pop(); active.pop()
    while intersections and not point_on_line_left(intersections[0], active[-1]):
        intersections.popleft(); active.popleft()
    if len(active) < 3:
        return []
    point = line_intersection(active[-1], active[0])
    return list(intersections) + ([] if point is None else [point])


half_plane = half_plane_intersection


def signed_area_twice(polygon):
    """Run the signed area twice operation."""
    polygon = Polygon(polygon)
    return polygon.signed_area_x2()


def polygon_area(polygon):
    """Run the polygon area operation."""
    return abs(signed_area_twice(polygon)) / 2.0


def polygon_centroid(polygon):
    """Run the polygon centroid operation."""
    polygon = Polygon(polygon)
    area_twice = polygon.signed_area_x2()
    if not area_twice:
        raise ValueError('degenerate polygon has no area centroid')
    return Point(sum((a.x + b.x) * (a ^ b) for a, b in zip(polygon, polygon[1:] + polygon[:1])) /
                 (3.0 * area_twice),
                 sum((a.y + b.y) * (a ^ b) for a, b in zip(polygon, polygon[1:] + polygon[:1])) /
                 (3.0 * area_twice))


def _circumcircle(a, b, c):
    """Run the internal circumcircle step."""
    denominator = 2.0 * ((a ^ b) + (b ^ c) + (c ^ a))
    if abs(denominator) <= EPS:
        return None
    aa, bb, cc = a.square(), b.square(), c.square()
    center = Point((aa * (b.y - c.y) + bb * (c.y - a.y) + cc * (a.y - b.y)) / denominator,
                   (aa * (c.x - b.x) + bb * (a.x - c.x) + cc * (b.x - a.x)) / denominator)
    return Circle(center, dist(center, a))


def circum_circle(a, b=None, c=None):
    """Run the circum circle operation."""
    if b is None:
        a, b, c = a[0], a[1], a[2]
    return _circumcircle(_point(a), _point(b), _point(c))


def triangle_circumcircle(a, b, c):
    """Run the triangle circumcircle operation."""
    circle = circum_circle(a, b, c)
    if circle is None:
        raise ValueError('degenerate triangle')
    return circle.O, circle.r


def in_circle(triangle):
    """Run the in circle operation."""
    a, b, c = map(_point, triangle)
    side_a, side_b, side_c = dist(b, c), dist(a, c), dist(a, b)
    perimeter = side_a + side_b + side_c
    area_twice = abs((b - a) ^ (c - a))
    if perimeter <= EPS or area_twice <= EPS:
        raise ValueError('degenerate triangle')
    return Circle((a * side_a + b * side_b + c * side_c) / perimeter, area_twice / perimeter)


def triangle_incircle(a, b, c):
    """Run the triangle incircle operation."""
    circle = in_circle((a, b, c))
    return circle.O, circle.r


def circle_line_intersections(circle, line_a, line_b=None):
    """Run the circle line intersections operation."""
    line = line_a if isinstance(line_a, Line) else Line(line_a, line_b)
    if line.v.square() <= EPS:
        return [line.a] if abs(dist(circle.O, line.a) - circle.r) <= EPS else []
    foot = project(circle.O, line)
    height_squared = circle.r * circle.r - (foot - circle.O).square()
    if height_squared < -EPS:
        return []
    if height_squared <= EPS:
        return [foot]
    direction = line.v / line.v.length()
    height = math.sqrt(height_squared)
    offset = normal_vector(direction) * height
    return [foot + offset, foot - offset]


def circle_line_intersect(circle, line_a, line_b=None):
    """Return whether a circle and a line have a common point."""
    return bool(circle_line_intersections(circle, line_a, line_b))


circle_line_intersect_points = circle_line_intersections


def circle_circle_intersections(first, radius_a=None, second=None, radius_b=None):
    """Run the circle circle intersections operation."""
    if isinstance(first, Circle):
        circle_a, circle_b = first, radius_a
    else:
        circle_a, circle_b = Circle(first, radius_a), Circle(second, radius_b)
    delta = circle_b.O - circle_a.O
    distance = delta.length()
    if distance <= EPS:
        return None if abs(circle_a.r - circle_b.r) <= EPS else []
    if distance > circle_a.r + circle_b.r + EPS or distance < abs(circle_a.r - circle_b.r) - EPS:
        return []
    along = (circle_a.r * circle_a.r - circle_b.r * circle_b.r + distance * distance) / (2.0 * distance)
    height_squared = max(0.0, circle_a.r * circle_a.r - along * along)
    base = circle_a.O + delta * (along / distance)
    if height_squared <= EPS:
        return [base]
    offset = normal_vector(delta / distance) * math.sqrt(height_squared)
    return [base + offset, base - offset]


def circle_circle_intersect_points(first, radius_a=None, second=None, radius_b=None):
    """Run the circle circle intersect points operation."""
    points = circle_circle_intersections(first, radius_a, second, radius_b)
    return (None, None) if points is None else (points[0], points[-1]) if points else (Point(), Point())


def circle_relationship(first, second):
    """Classify circles as coincident(-1), contained(0), tangent(1/3), crossing(2), or separate(4)."""
    if first.r < second.r:
        first, second = second, first
    distance = dist(first.O, second.O)
    if sign(distance) == 0 and sign(first.r, second.r) == 0:
        return -1
    if sign(distance, first.r + second.r) > 0:
        return 4
    if sign(distance, first.r + second.r) == 0:
        return 3
    if sign(distance, first.r - second.r) == 0:
        return 1
    return 2 if distance > first.r - second.r else 0


relationship_between_two_circle = circle_relationship


def circle_tangent_points(circle, point):
    """Run the circle tangent points operation."""
    point = _point(point)
    vector = point - circle.O
    distance_squared = vector.square()
    if sign(distance_squared, circle.r * circle.r) < 0:
        return []
    if sign(distance_squared, circle.r * circle.r) == 0:
        return [point]
    distance = math.sqrt(distance_squared)
    alpha = math.acos(circle.r / distance)
    base = vector.polar_angle()
    return [circle.point_at(base + alpha), circle.point_at(base - alpha)]


get_circle_point_tangent_points = circle_tangent_points


def common_tangents(center_a, radius_a, center_b, radius_b):
    """Run the common tangents operation."""
    center_a, center_b = _point(center_a), _point(center_b)
    delta = center_b - center_a
    distance_squared = delta.square()
    if distance_squared <= EPS and abs(radius_a - radius_b) <= EPS:
        return None
    result = []
    for radius_sign in (1, -1):
        signed_radius_b = radius_sign * radius_b
        difference = radius_a - signed_radius_b
        height_squared = distance_squared - difference * difference
        if height_squared < -EPS or distance_squared <= EPS:
            continue
        height = math.sqrt(max(0.0, height_squared))
        for side in ((1, -1) if height > EPS else (1,)):
            vector = Point((delta.x * difference - delta.y * height * side) / distance_squared,
                           (delta.y * difference + delta.x * height * side) / distance_squared)
            result.append((center_a + vector * radius_a, center_b + vector * signed_radius_b))
    return result


get_circle_circle_tangents = common_tangents


def middle(a, b):
    """Run the middle operation."""
    return (_point(a) + _point(b)) / 2.0


def angle_of_vec(vector):
    """Run the angle of vec operation."""
    return math.atan2(_point(vector).y, _point(vector).x)


def polar_vec(radius, radians):
    """Run the polar vec operation."""
    return Point(radius * math.cos(radians), radius * math.sin(radians))


def minimum_circle(points):
    """Run the minimum circle operation."""
    points = [_point(point) for point in points]
    if not points:
        return Circle()
    random.shuffle(points)
    circle = Circle(points[0], 0.0)
    for i, point in enumerate(points):
        if dist(circle.O, point) <= circle.r + EPS:
            continue
        circle = Circle(point, 0.0)
        for j in range(i):
            other = points[j]
            if dist(circle.O, other) <= circle.r + EPS:
                continue
            circle = Circle((point + other) / 2.0, dist(point, other) / 2.0)
            for k in range(j):
                third = points[k]
                if dist(circle.O, third) > circle.r + EPS:
                    candidate = _circumcircle(point, other, third)
                    if candidate is None:
                        circle = max((Circle((first + second) / 2.0, dist(first, second) / 2.0)
                                      for first, second in ((point, other), (point, third), (other, third))),
                                     key=lambda item: item.r)
                    else:
                        circle = candidate
    return circle


minimum_enclosing_circle = minimum_circle


def convex_polygon_diameter(polygon):
    """Run the convex polygon diameter operation."""
    polygon = Polygon(polygon)
    n = len(polygon)
    if n == 0:
        return 0, None
    if n == 1:
        return 0, (polygon[0], polygon[0])
    if n == 2:
        return dist_2(polygon[0], polygon[1]), (polygon[0], polygon[1])
    best, pair, j = -1, None, 1
    for i in range(n):
        next_i = (i + 1) % n
        while abs(((polygon[next_i] - polygon[i]) ^ (polygon[(j + 1) % n] - polygon[i]))) > \
                abs(((polygon[next_i] - polygon[i]) ^ (polygon[j] - polygon[i]))):
            j = (j + 1) % n
        for candidate in (j, (j + 1) % n):
            current = dist_2(polygon[i], polygon[candidate])
            if current > best:
                best, pair = current, (polygon[i], polygon[candidate])
    return best, pair


get_hull = convex_hull


def closest_pair(points):
    """Run the closest pair operation."""
    points = sorted(_point(point) for point in points)
    if len(points) < 2:
        return INF, None

    def solve(left, right):
        """Run the solve operation."""
        if right - left <= 3:
            candidates = [(dist_2(points[i], points[j]), (points[i], points[j]))
                          for i in range(left, right) for j in range(i + 1, right)]
            return min(candidates) if candidates else (INF, None)
        middle = (left + right) // 2
        best = min(solve(left, middle), solve(middle, right), key=lambda item: item[0])
        strip = sorted((p for p in points[left:right] if (p.x - points[middle].x) ** 2 < best[0]),
                       key=lambda p: p.y)
        for i in range(len(strip)):
            for j in range(i + 1, len(strip)):
                if (strip[j].y - strip[i].y) ** 2 >= best[0]:
                    break
                candidate = (dist_2(strip[i], strip[j]), (strip[i], strip[j]))
                if candidate[0] < best[0]:
                    best = candidate
        return best

    return solve(0, len(points))


def minkowski_sum(polygon_a, polygon_b):
    """Run the minkowski sum operation."""
    a, b = Polygon(polygon_a), Polygon(polygon_b)
    if not a or not b:
        return Polygon()
    a = _normalize_polygon(a)
    b = _normalize_polygon(b)
    edges_a = [a[(i + 1) % len(a)] - a[i] for i in range(len(a))]
    edges_b = [b[(i + 1) % len(b)] - b[i] for i in range(len(b))]
    point, result, i, j = a[0] + b[0], [], 0, 0
    while i < len(edges_a) or j < len(edges_b):
        cross = edges_a[i] ^ edges_b[j] if i < len(edges_a) and j < len(edges_b) else 1 if i < len(edges_a) else -1
        step = Point()
        if i < len(edges_a) and cross >= 0:
            step += edges_a[i]; i += 1
        if j < len(edges_b) and cross <= 0:
            step += edges_b[j]; j += 1
        result.append(point)
        point += step
    return Polygon(result)


def _normalize_polygon(polygon):
    """Run the internal normalize polygon step."""
    start = min(range(len(polygon)), key=lambda i: (polygon[i].y, polygon[i].x))
    return Polygon(polygon[start:] + polygon[:start])


def lattice_polygon_points(polygon):
    """Run the lattice polygon points operation."""
    polygon = Polygon(polygon)
    area_twice = sum(a ^ b for a, b in zip(polygon, polygon[1:] + polygon[:1]))
    boundary = sum(math.gcd(abs(a.x - b.x), abs(a.y - b.y))
                   for a, b in zip(polygon, polygon[1:] + polygon[:1]))
    return (abs(area_twice) - boundary + 2) // 2, boundary


def segment_union_length(segments):
    """Run the segment union length operation."""
    segments = sorted((min(left, right), max(left, right)) for left, right in segments)
    if not segments:
        return 0
    left, right, result = segments[0][0], segments[0][1], 0
    for current_left, current_right in segments[1:]:
        if current_left > right:
            result += right - left
            left, right = current_left, current_right
        else:
            right = max(right, current_right)
    return result + right - left


class ChebyshevDistanceSum(object):
    def __init__(self, points):
        """Initialize the data structure."""
        points = [_point(point) for point in points]
        self.u, self.v = sorted(point.x + point.y for point in points), sorted(point.x - point.y for point in points)
        self.prefix_u, self.prefix_v = self._prefix(self.u), self._prefix(self.v)

    @staticmethod
    def _prefix(values):
        """Run the internal prefix step."""
        prefix = [0]
        for value in values:
            prefix.append(prefix[-1] + value)
        return prefix

    @staticmethod
    def _absolute_sum(values, prefix, query):
        """Run the internal absolute sum step."""
        index = bisect.bisect_left(values, query)
        return query * index - prefix[index] + prefix[-1] - prefix[index] - query * (len(values) - index)

    def query(self, x, y):
        """Run the query operation."""
        total = self._absolute_sum(self.u, self.prefix_u, x + y) + self._absolute_sum(self.v, self.prefix_v, x - y)
        return total // 2 if isinstance(total, int) else total / 2.0


def maximum_manhattan_distance(points):
    """Run the maximum manhattan distance operation."""
    points = [tuple(point) for point in points]
    if len(points) < 2:
        return 0
    dimensions, answer = len(points[0]), 0
    for mask in range(1 << dimensions):
        values = [sum(-value if mask >> i & 1 else value for i, value in enumerate(point)) for point in points]
        answer = max(answer, max(values) - min(values))
    return answer


def adaptive_simpson(function, left, right, tolerance=1e-9, max_depth=20):
    """Integrate one smooth function with adaptive Simpson recursion."""
    def simpson(a, b, fa, fm, fb):
        """Approximate one interval with Simpson's rule."""
        return (b - a) * (fa + 4.0 * fm + fb) / 6.0

    def integrate(a, b, fa, fm, fb, whole, eps, depth):
        """Recursively split an interval until its estimate converges."""
        middle = (a + b) / 2.0
        flm, frm = function((a + middle) / 2.0), function((middle + b) / 2.0)
        left_part, right_part = simpson(a, middle, fa, flm, fm), simpson(middle, b, fm, frm, fb)
        error = left_part + right_part - whole
        if depth == 0 or abs(error) <= 15.0 * eps:
            return left_part + right_part + error / 15.0
        return integrate(a, middle, fa, flm, fm, left_part, eps / 2.0, depth - 1) + \
               integrate(middle, b, fm, frm, fb, right_part, eps / 2.0, depth - 1)

    middle = (left + right) / 2.0
    fa, fm, fb = function(left), function(middle), function(right)
    return integrate(left, right, fa, fm, fb, simpson(left, right, fa, fm, fb), tolerance, max_depth)


def adaptive_simpson_2d(function, x_left, x_right, y_left, y_right,
                        tolerance=1e-8, max_depth=16):
    """Integrate function(x, y) over an axis-aligned rectangle."""
    return adaptive_simpson(
        lambda x: adaptive_simpson(lambda y: function(x, y), y_left, y_right,
                                   tolerance / 4.0, max_depth),
        x_left, x_right, tolerance, max_depth,
    )


def adaptive_simpson_3d(function, x_left, x_right, y_left, y_right,
                        z_left, z_right, tolerance=1e-7, max_depth=14):
    """Integrate function(x, y, z) over an axis-aligned box."""
    return adaptive_simpson(
        lambda x: adaptive_simpson_2d(lambda y, z: function(x, y, z),
                                      y_left, y_right, z_left, z_right,
                                      tolerance / 4.0, max_depth),
        x_left, x_right, tolerance, max_depth,
    )


def minimum_area_three_rectangles(sizes):
    """Minimum enclosing area for three axis-aligned rectangles."""
    if len(sizes) != 3:
        raise ValueError('exactly three rectangles are required')
    answer = min(sum(size[0] for size in sizes) * max(size[1] for size in sizes),
                 sum(size[1] for size in sizes) * max(size[0] for size in sizes))
    for order in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
        first, second, third = (sizes[index] for index in order)
        answer = min(answer, max(first[0] + second[0], third[0]) * (max(first[1], second[1]) + third[1]))
    return answer
