import sys
import math
import time
def parse(points):

    """
    Reads the file of points and converts into list of tuples (list of points). Returns points sorted in ascending order
    with respect the different variables.
    :return:
            1. List of points (tuples), sorted in ascending order with respect to first variable
            2. List of points (tuples), sorted in ascending order with respect to second variable
            3. Number of points.
    """

    #points = sys.stdin.readlines()
    # Convert list of strings which represent points into points represented as list of integer tuples.
    points = [tuple(map(int, point.strip().split())) for point in points]
    num_points = points.pop(0)
    return sorted(points, key=lambda x: x[0]), sorted(points, key=lambda x: x[1]), num_points[0]

def main_method(Px, Py, size):
    """
    Starts the recursion.
    :param Px: List of points sorted by x
    :param Py: List of points sorted by y
    :param size: Number of points in the lists
    :return: shortest distance
    """
    print(round(procedure(Px, Py, size),6))

def procedure(Px, Py, size):
    """
    Recursion function
    :param Px: List of points sorted by x
    :param Py: List of points sorted by y
    :param size: Number of points in the lists
    :return: shortest distance
    """

    Ly=[]
    Ry=[]
    if size<4:
        return solvesubproblems(Px)

    Lx, Rx, middle = addtoside(Px, size)

    left_set = set(Lx)

    for element in Py:
        if element in left_set:
            Ly.append(element)
        else:
            Ry.append(element)

    sigmaL=procedure(Lx, Ly, size//2)
    sigmaR=procedure(Rx, Ry, size-(size//2))

    sigma=min(sigmaL, sigmaR)
    Sy = thinset(Py, sigma, middle)
    abs_shortest = check_closest(Sy)
    if abs_shortest < sigma:
        sigma = abs_shortest
    return sigma

def addtoside(P, size):
    """
    Splits P into two equally long lists
    :param P: List to split
    :param size: Number of points in the lists
    :return 1: left side of array
    :return 2: Right side of array
    :return 3: Middle element
    """
    Pleft=P[:math.floor(size/2)]
    Pright=P[math.floor(size/2):]
    return Pleft, Pright, Pright[0][0]

def thinset(Py, sigma, middle):
    """
    Returns elements within a distance sigma from the middle
    :param Py: array sorted by Y
    :param sigma: Distance from middle to be covered
    :param middle: x-value from which the sigma should be used.
    :return: shortest distance
    """
    Sy=[]
    print("Py: ", len(Py))
    for element in Py:
        if(element[0]<(middle+sigma) and element[0]>(middle-sigma)):
            Sy.append(element)
    print("Sy: ", len(Sy))
    return Sy

def distance(first, second):
    """
    Returns distance between two points
    :param first: first point
    :param second: second point
    :return: distance between the input points using the distance formula.
    """
    distance=math.sqrt((first[0]-second[0])**2+(first[1]-second[1])**2)
    return distance

def solvesubproblems(P):
    """
    Returns shortest distance between points in a set
    :param P: set of points
    :return: shortest distance between any two points in the set P
    """
    mindist=distance(P[0], P[1])
    for element1 in P:
        for element2 in P:
            tempdist=distance(element1, element2)
            if tempdist<mindist and tempdist>0:
                mindist=tempdist
    return mindist

def check_closest(Sy):
    """
    Returns shortest distance between two points on different side of the middle-line
    :param Sy: Set of points within sigma distance from the middle line
    :return: Smallest distance between two points in the set
    """
    mindist=5000000
    for primary in range(len(Sy)):
        max_range = len(Sy) - primary
        if (max_range) < 9:
            addon = max_range
        else:
            addon=8
        for x in range(1, addon):
            tempdist = distance(Sy[primary-1], Sy[primary+x-1])
            if tempdist<mindist and tempdist>0:
                mindist=tempdist
    return mindist


if __name__ == '__main__':
    start = time.time()
    points = open("data\\secret\\6huger.in","r")
    Px, Py, size= parse(points)
    main_method(Px, Py, size)
    end = time.time()
    print("finished in ", round(end - start,2), " seconds")