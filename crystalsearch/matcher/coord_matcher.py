import numpy as np


def coordinate_error(match_pair: dict):
    """根据给定原子映射关系，计算旋转矩阵、平移向量和最小坐标误差"""
    set_a = []
    set_b = []
    for k, v in match_pair.items():
        set_a.append([k.x, k.y, k.z])
        set_b.append([v.x, v.y, v.z])
    mat_a = np.array(set_a)
    mat_b = np.array(set_b)

    mat_a -= np.mean(mat_a, 0)
    mat_b -= np.mean(mat_b, 0)

    mat_a /= np.linalg.norm(mat_a)
    mat_b /= np.linalg.norm(mat_b)

    u, w, vt = np.linalg.svd(mat_b.T.dot(mat_a).T)
    R = u.dot(vt)
    scale = w.sum()
    mat_b = np.dot(mat_b, R.T) * scale
    rmse = len(set_a) / np.sum(np.square(mat_a - mat_b)) / 10000.0  # 取倒数，使得rmse越大匹配越好
    return rmse, R
