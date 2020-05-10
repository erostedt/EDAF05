import sys
import math


def parse():
    """
    Reads the file of points and converts into list of tuples (list of points). Returns points sorted in ascending order
    with respect the different variables.
    :return:
            1. List of points (tuples), sorted in ascending order with respect to first variable
            2. List of points (tuples), sorted in ascending order with respect to second variable
            3. Number of points.
    """
    points = sys.stdin.readlines()
    # Convert list of strings which represent points into points represented as list of integer tuples.
    points = [tuple(map(int, point.strip().split())) for point in points]
    num_points = points.pop(0)
    return sorted(points, key=lambda x: x[0]), sorted(points, key=lambda x: x[1]), num_points[0]


def closest_points():
    """
    Finds the closest points on a plane. Calls for input parsing, and starts recursive divide and conquer method.
    Distances are measured as squared Euclidian norm, squared since square root is a slow operation. But in the end
    when the distance shall be returned, the square root of the squared distance is returned.
    :return: Distance between closest points in a plane.
    """
    px, py, num_points = parse()
    sq_dist = _closest_points(px, py, num_points)
    return format(math.sqrt(sq_dist), '.6f')


def _closest_points(px, py, num_points):
    """
    Recursive function which calculates closest pair of points on a plane, based on a divide and conquer method.
    Time complexity: O(n logn)
    :param px: Points sorted in ascending order with respect to the first variable (x).
    :param py: Points sorted in ascending order with respect to the second variable (y).
    :param num_points: Number of points.
    :return: Smallest squared distance.
    """
    middle = num_points // 2
    divisor = px[middle][0]

    if num_points < 4:
        return brute_force(px)

    lpx = px[:middle]
    rpx = px[middle:]

    # Construct set for O(1) lookup.
    lp_set = set(lpx)

    lpy, rpy = [], []
    for point in py:
        if point in lp_set:
            lpy.append(point)
        else:
            rpy.append(point)

    left_dist = _closest_points(lpx, lpy, middle)
    right_dist = _closest_points(rpx, rpy, num_points - middle)
    sq_dist = min(left_dist, right_dist)
    return min(sq_dist, closest_overlap(py, sq_dist, divisor))


def sq_distance(p1, p2):
    """
    Calculates the squared Euclidian distance between two points in a plane.
    :param p1: Point 1.
    :param p2: Point 2.
    :return: Squared Euclidian distance between the points.
    """
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2


def brute_force(points):
    """
    Brute force method. Only gets called if there are two or three points to compare.
    :param points: List of points to be compared.
    :return sq_dist: Squared Euclidian distance between the closest points.
    """
    sq_dist = float('Inf')
    for point in points:
        for other_point in points:
            if point is not other_point:
                cmp_dist = sq_distance(point, other_point)
                if cmp_dist < sq_dist:
                    sq_dist = cmp_dist
    return sq_dist


def closest_overlap(points, sq_dist, divisor):
    """
    Finds the squared Euclidian distance between the two closest point that are seperated by the divisor line.
    :param points: List of points, sorted with respect to second variable (y).
    :param sq_dist: Squared distance of closest point on the same side of divisor line.
    :param divisor: Position of divisor line (with respect to first variable, x).
    :return overlap_sq_dist:
        squared Euclidian distance between the two closest point that are seperated by the divisor line.
    """
    dist = math.sqrt(sq_dist)

    feasible_points = [point for point in points if abs(point[0] - divisor) < dist]
    num_feasible_points = len(feasible_points)

    overlap_sq_dist = float('Inf')
    for point_idx, feasible_point in enumerate(feasible_points):
        cmp_points = feasible_points[point_idx + 1: point_idx + min(15, num_feasible_points - point_idx)]
        for cmp_point in cmp_points:
            overlap_sq_dist = min(sq_distance(feasible_point, cmp_point), overlap_sq_dist)
    return overlap_sq_dist


if __name__ == '__main__':
    print(closest_points())
