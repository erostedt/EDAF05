import sys
import math


def parse():
    """
    Reads the file of points and converts into list of tuples (list of points). Returns points sorted in ascending order
    with respect to the first variable (x).
    :return:
            1. List of points (tuples), sorted in ascending order with respect to first variable
            2. Number of points.
    """
    points = sys.stdin.readlines()
    # Convert list of strings which represent points into points represented as list of integer tuples.
    points = [tuple(map(int, point.strip().split())) for point in points]
    num_points = points.pop(0)
    points.sort(key=lambda x: x[0])
    return points, num_points[0]


def closest_points():
    """
    Finds the closest points on a plane. Calls for input parsing, and starts recursive divide and conquer method.
    Distances are measured as Euclidian norm.
    :return: Distance between closest points in a plane.
    """
    px, num_points = parse()
    if num_points < 2:
        print('Not enough points')
        return None
    dist = _closest_points(px, num_points)
    return format(dist, '.6f')  


def _closest_points(px, num_points):
    """
    Recursive function which calculates closest pair of points on a plane, based on a divide and conquer method.
    Time complexity: O(n logn)
    :param px: Points sorted in ascending order with respect to the first variable (x).
    :param num_points: Number of points.
    :return: Smallest distance.
    """
    middle = num_points // 2
    divisor = px[middle][0]

    if num_points < 4:
        return base_case(px)

    left_dist = _closest_points(px[:middle], middle)
    right_dist = _closest_points(px[middle:], num_points - middle)
    dist = min(left_dist, right_dist)
    return min(dist, closest_overlap(px, dist, divisor))


def distance(p1, p2):
    """
    Calculates the Euclidian distance between two points in a plane.
    :param p1: Point 1.
    :param p2: Point 2.
    :return: Euclidian distance between the points.
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def base_case(points):
    """
    Brute force method. Only gets called if there are two or three points to compare.
    :param points: List of points to be compared.
    :return d: Euclidian distance between the closest points.
    """
    dist = float('Inf')
    for point in points:
        for other_point in points:
            if point is not other_point:
                dist = min(dist, distance(point, other_point))
    return dist


def closest_overlap(points, dist, divisor):
    """
    Finds the Euclidian distance between the two closest point that are seperated by the divisor line.
    :param points: List of points.
    :param dist: distance of closest point on the same side of divisor line.
    :param divisor: Position of divisor line (with respect to first variable, x).
    :return overlap_dist:
        Euclidian distance between the two closest point that are seperated by the divisor line.
    """
    strip_points = [point for point in points if abs(point[0] - divisor) < dist]
    num_strip_points = len(strip_points)
    strip_points.sort(key=lambda x: x[1])

    overlap_dist = float('Inf')
    for point_idx, strip_point in enumerate(strip_points):
        feasible_points = strip_points[point_idx + 1: point_idx + min(15, num_strip_points - point_idx)]
        for feasible_point in feasible_points:
            overlap_dist = min(distance(strip_point, feasible_point), overlap_dist)

    return overlap_dist


if __name__ == '__main__':
    print(closest_points())
