def standard_euclidian(start, end):
    (x, y) = start
    (endx, endy) = end
    return ((x-endx)**2 + (y-endy)**2) ** 0.5 

def modified_euclidian(start, end):
    (x, y) = start
    (endx, endy) = end
    return ((x-endx)**2 + (y-endy)**2)

def standard_manhattan(start, end):
    (x, y) = start
    (endx, endy) = end
    return abs(x-endx) + abs(y-endy)

def standard_minkowski(start, end, p=3):
    '''
    With p = 1, it's the same as Manhattan distance.\n
    With p = 2, it's the same as Euclidian distance.\n
    With p = inf, it's the same as Chebyshev distance.\n
    '''
    (x, y) = start
    (endx, endy) = end
    return (abs(x-endx)**p + abs(y-endy)**p) ** (1/p)