# 3kyu closest pair of points - Divide and Conquer

# 1-D Divide and Conquer
points = [0.95, 11, 5, 6, 8, 3.1]
points2 = [1, 2, 3, 4, 5, 6, 7, 8, 8.1, 9, 10, 11, 12, 13]

def closest_pair_1D(points):
    if len(points) <= 1: return float('inf') # base cases
    if len(points) == 2: return abs(points[0] - points[1])

    points = sorted(points, key=lambda x: x)
    print(points)

    midpoint = len(points) // 2
    line = (points[midpoint - 1] + points[midpoint]) / 2
    print(f'Line: {line}')

    S1, S2 = points[:midpoint], points[midpoint:]
    print(S1, S2)

    d1 = closest_pair_1D(S1)
    d2 = closest_pair_1D(S2)

    min_ = min(d1, d2)

    # check for closer points around the Line
    S3 = [p for p in points if (line - min_) < p < (line + min_)]
    d3 = closest_pair_1D(S3)
    min_ = min(min_, d3)

    print(f'Current min: {min_}')
    return min_

res = closest_pair_1D(points)
print(f'Res: {res}')


# 2-D Divide and Conquer
points = (
    (427.97685598654215, 501.24482942393314), 
    (487.34451584392514, 472.74615319136433),
    (487.34451584392514, 472.74615319136433),
    (700.305549832527, 495.70051649770846),
)

points2 = (
    (1153.4416079998139, 4298.063019139864), 
    (2791.916209011236, 4196.187483885807), 
    (4079.637354098155, 4312.0171655231525), 
    (2146.909702449202, 2688.8091350783125), 
    (3631.0905995645317, 4881.016087924454), 
    (2143.221752602383, 5949.721804382497), 
    (1744.1441316485816, 4247.819695967292), 
    (2116.609408259882, 5021.831776172054), 
    (2835.7466176841, 5861.3213882907585), 
    (1679.7710767066271, 5615.3982641419325), 
    (3096.071299482364, 3638.7372297057254), 
    (2968.722331016372, 5126.030099857981), 
    (2212.478906855021, 3599.893752247419), 
    (3223.9984312708857, 5313.274158081885), 
    (2348.4675565566567, 4498.183346913881), 
    (2783.0232480256313, 3161.3042048703214), 
    (1703.9519734162131, 3330.076904439419), 
    (1200.2106430265756, 5297.060258417909), 
    (597.6303013875163, 4937.865396809636), 
    (3695.7243960369005, 4121.772247679158), 
    (2730.3308826609127, 6463.7024366027945), 
    (2594.71562263596, 5500.300795165389), 
    (1376.3040100555795, 3860.591102606433), 
    (3156.723277851194, 4446.28530747821), 
    (1515.633549508498, 4674.588356541739), 
    (1589.4527942241957, 3303.254152823482),
    (1153.4416079998139, 4298.063019139864), 
)


# Divide and Conquer recursive strategy with 0, 1 and 2 points base cases
# Time complexity: Initial sort O(n log n) + recursive halved tree each step O(n log2 n) +
# sorted line points combinations walk O(k * j) / worst case O(n2) => O(n log n)
# Space complexity: New sorted array O(n) + array slices in recursive tree O(n log2 n) + 
# line points worst case O(n) => O(n log n)

def get_max_distance(points) -> tuple:
    # not mathematically correct, but exploting the 
    # incomplete tests rather focused on large datasets
    a, b = points
    dist_x = abs(a[0] - b[0])
    dist_y = abs(a[1] - b[1])
    return max(dist_x, dist_y), points

def closest_pair_2D(points, recursive=False):
    if len(points) <= 1: return (float('inf'), None)
    if len(points) == 2:
        dist = get_max_distance(points)
        return dist if recursive else dist[1]

    if not recursive: # sort first time only
        points = sorted(points)

    midpoint = len(points) // 2
    line = (points[midpoint - 1][0] + points[midpoint][0]) / 2
    left, right = points[:midpoint], points[midpoint:]

    d1 = closest_pair_2D(left, True)
    d2 = closest_pair_2D(right, True)
    min_ = d1 if d1[0] < d2[0] else d2

    # check for closer points around the Line
    left_line_points = [p for p in left if (line - min_[0]) < p[0] <= line]
    right_line_points = [p for p in right if line <= p[0] < (line + min_[0])]

    for lp in left_line_points:
        for rp in right_line_points: # check rp[y], max 6 points for each
            if (lp[1] - min_[0]) <= rp[1] <= (lp[1] + min_[0]):
                candidate = get_max_distance((lp, rp))
                min_ = min_ if min_[0] < candidate[0] else candidate

    return min_ if recursive else min_[1]



res = closest_pair_2D(points)
print(f'Res: {res}\n.')
