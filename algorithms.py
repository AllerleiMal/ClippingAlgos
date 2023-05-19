from matplotlib.path import Path
import numpy as np
from shapely.geometry.polygon import Polygon
from shapely.geometry import LineString

def liang_barsky(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    dx = x2 - x1
    dy = y2 - y1
    p = [-dx, dx, -dy, dy]
    q = [x1 - xmin, xmax - x1, y1 - ymin, ymax - y1]

    u1 = 0
    u2 = 1

    for i in range(4):
        if p[i] == 0:
            if q[i] < 0:
                return None
        else:
            r = q[i] / p[i]
            if p[i] < 0:
                if r > u2:
                    return None
                elif r > u1:
                    u1 = r
            elif p[i] > 0:
                if r < u1:
                    return None
                elif r < u2:
                    u2 = r

    x1_clip = x1 + u1 * dx
    y1_clip = y1 + u1 * dy
    x2_clip = x1 + u2 * dx
    y2_clip = y1 + u2 * dy

    return x1_clip, y1_clip, x2_clip, y2_clip

# def sutherland_hodgman(subject_polygon, clip_polygon):
#     def inside(p, cp1, cp2):
#         return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) > (cp2[1] - cp1[1]) * (p[0] - cp1[0])

#     def intersection(cp1, cp2, s, e):
#         dc = (cp1[0] - cp2[0], cp1[1] - cp2[1])
#         dp = (s[0] - e[0], s[1] - e[1])
#         n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
#         n2 = s[0] * e[1] - s[1] * e[0]
#         n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
#         return ((n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3)

#     def clip(subject_polygon, clip_polygon):
#         output_list = subject_polygon
#         cp1 = clip_polygon[-1]
#         for clip_vertex in clip_polygon:
#             cp2 = clip_vertex
#             input_list = output_list
#             output_list = []
#             if len(input_list) == 0:
#                 return []
#             s = input_list[-1]
#             for subject_vertex in input_list:
#                 e = subject_vertex
#                 if inside(e, cp1, cp2):
#                     if not inside(s, cp1, cp2):
#                         output_list.append(intersection(cp1, cp2, s, e))
#                     output_list.append(e)
#                 elif inside(s, cp1, cp2):
#                     output_list.append(intersection(cp1, cp2, s, e))
#                 s = e
#             cp1 = cp2
#         return output_list

#     output = clip(subject_polygon, clip_polygon)
#     if len(output) > 0:
#         return output
#     else:
#         return None
    
def cyrus_beck_algorithm(x1, y1, x2, y2, polygon):
    def line_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
        # Находим точку пересечения двух отрезков
        # Используем формулу пересечения прямых
        den = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
        if den == 0:
            return None, None
        ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
        ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den
        if ua < 0 or ua > 1 or ub < 0 or ub > 1:
            return None, None
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)
        return x, y

    path = Path(polygon)

    # Проверяем, видим ли начальную и конечную точки отрезка
    inside1 = path.contains_point((x1, y1))
    inside2 = path.contains_point((x2, y2))

    vertices = np.array(polygon)
    intersections = []
    for i in range(len(vertices)):
        x3, y3 = vertices[i]
        x4, y4 = vertices[(i + 1) % len(vertices)]
        x, y = line_intersection(x1, y1, x2, y2, x3, y3, x4, y4)
        if x is not None and y is not None:
            intersections.append((x, y))

    if inside1 and inside2:
        return [x1, y1, x2, y2]
    elif not inside1 and not inside2:
        if len(intersections) == 0:
            return None
        result = []
        for intersection in intersections:
            result.append(intersection[0])
            result.append(intersection[1])

        return result
    else:
        if len(intersections) == 0:
            return None

        result = []
        if inside1 is True:
            result = [x1, y1]
        else:
            result = [x2, y2]

        for intersection in intersections:
            result.append(intersection[0])
            result.append(intersection[1])

        return result