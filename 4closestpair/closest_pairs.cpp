#include <iostream>
#include <cmath>
#include <iomanip>


struct Point{
/**
 * Point structure
 */
public:
    double x, y;
};

int cmp_x(const void* p1, const void* p2){
    /**
     * Compare function with respect to x-dimension
     */ 
    Point *point1 = (Point*)p1;
    Point *point2 = (Point*)p2;
    return point1->x - point2->x;
}

int cmp_y(const void* p1, const void* p2){
    /**
     * Compare function with respect to y-dimension
     */
    Point *point1 = (Point*)p1;
    Point *point2 = (Point*)p2;
    return point1->y - point2->y;
}

double sq_dist(Point p1, Point p2){
    /**
     * squared distance function, bad if numbers are to large, good since square root is slow.
     */
    return pow(p1.x - p2.x, 2) + pow(p1.y - p2.y, 2);
}

double base_case(Point* points, int num_points){
    /**
     * Brute force method, gets called when number of points are only 2 or 3. Finds points that are closest together.
     */
    double d = __DBL_MAX__;
    for(int i = 0; i < num_points; i++){
        for(int j = i + 1; j < num_points; j++){
            d = std::min(d, sq_dist(points[i], points[j]));
        }
    }
    return d;
}

double closest_overlap(Point* points, double dist, int num_points, double divisor){
    /**
     * Finds the squared Euclidian distance between the two closest point that are seperated by the divisor line.
     */
    Point* overlap = new Point[num_points];
    int iter = 0;
    double true_dist = sqrt(dist);
    for(int i = 0; i < num_points; i++){
        if(abs(points[i].x - divisor) < true_dist){
            overlap[iter] = points[i];
            iter++;
        }
    }
    qsort(overlap, iter, sizeof(Point), cmp_y);
    double overlap_min = __DBL_MAX__;
    for (int i = 0; i < iter; i++){
        int look_ahead = std::min(15, iter - i);
        for(int j = i+1; j < i + look_ahead; j++){
            overlap_min = std::min(overlap_min, sq_dist(overlap[i], overlap[j])); 
        }
    }
    delete[] overlap;
    return overlap_min;
}

double closest_points(Point* points, int num_points){
    /**
     * Recursive Divide and conquer method for calculating closest points in a plane
     */ 
    int middle = num_points / 2;
    double divisor = points[middle].x;

    if(num_points < 4){
        return base_case(points, num_points);
    }

    double left_dist = closest_points(points, middle);
    double right_dist = closest_points(points + middle, num_points - middle);
    double d = std::min(left_dist, right_dist);

    return std::min(d, closest_overlap(points, d, num_points, divisor));

}

int main(int argc, char* argv[]){
    /**
     * Main function, parses and calls solver method.
     */ 
    int num_points;
    std::cin >> num_points;

    Point* points = new Point[num_points];
    int i = 0;
    double x, y;
    for(int i = 0; i < num_points; i++){
        std::cin >> points[i].x;
        std::cin >> points[i].y;
    } 

    qsort(points, num_points, sizeof(Point), cmp_x); 
    std::cout << std::setprecision(6) << std::fixed << sqrt(closest_points(points, num_points)) << '\n';
    delete[] points;
}


