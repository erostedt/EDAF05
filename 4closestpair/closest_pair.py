import sys


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


if __name__ == '__main__':
    px, py, num_points = parse()
    