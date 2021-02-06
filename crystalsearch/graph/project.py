import numpy as np


def project3d(points, direction):
    """投影函数，将三维点集投影到二维
    points: 三维点集
    direction: 投影平面的法向量(u,v,w)，投影平面通过原点(0,0,0)
    投影平面内的y方向为z轴投影(如果投影的法向量为z轴，则y方向为x轴投影)
    """
    d = direction / np.linalg.norm(direction)
    y0 = np.array([1, 0, 0]) if np.array([0, 0, 1]).dot(d) == 1 else np.array([0, 0, 1])
    y1 = y0 - np.dot(d, y0) * d
    norm_y = y1 / np.linalg.norm(y1)
    x0 = np.cross(norm_y, d)
    norm_x = x0 / np.linalg.norm(x0)
    pos = {}
    for k in points:
        p0 = np.array(points[k])
        p1 = p0 - np.dot(d, p0) * d
        pos[k] = (np.dot(norm_y, p1), np.dot(norm_x, p1))
    return pos