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

def procedure(Px, Py, size):
    Lx, Rx, middle = addtoside(Px,size)
    Ly, Ry, middle = addtoside(Py,size)
    sigma = (solvesubproblems(Lx), solvesubproblems(Rx), solvesubproblems(Ly), solvesubproblems(Ry))
    sigma=min(sigma)
    Sy=thinset(Py, sigma, middle)
    abs_shortest=check_closest(Sy)
    if(abs_shortest<sigma):
        sigma=abs_shortest
    print(sigma)
    return sigma

def addtoside(P,size):
    Pleft=P[math.floor(size/2):]
    Pright=P[:math.floor(size/2)]
    middle=math.floor(size/2)
    return Pleft, Pright, middle

def thinset(Py, sigma, middle):
    Sy=[]
    for element in Py:
        if(element[0]<(middle+sigma) or element[0]>(middle-sigma)):
            Sy.append(element)
    return Sy

def distance(first, second):
    distance=math.sqrt((first[0]-second[0])**2+(first[1]-second[1])**2)
    return distance

def solvesubproblems(P):
    mindist=10000

    for element1 in P:
        for element2 in P:
            tempdist=distance(element1, element2)
            if tempdist<mindist and tempdist>0:
                mindist=tempdist
    return mindist

def check_closest(Sy):
    mindist=10000;
    for primary in range(len(Sy)):
        max_range = len(Sy) - primary
        if (max_range) < 16:
            addon = max_range
        else:
            addon=15
        for x in range(1,addon):
            tempdist = distance(Sy[primary-1], Sy[primary+x-1])
            if tempdist<mindist and tempdist>0:
                mindist=tempdist
    return mindist


def check_solution(P):
    min = solvesubproblems(P)
    numbers=[]
    numbers.append(min)
    numbers.sort()
    print(numbers)





if __name__ == '__main__':
    px, py, num_points = parse()
    procedure(px, py, num_points)
#points = open("data\\secret\\3large.in","r")
#Px, Py, size= parse(points)
#procedure(Px, Py, size)
#check_solution(Px)