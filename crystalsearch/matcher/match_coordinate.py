import numpy as np


def coordinate_error(match_pair):
    set_a = []
    set_b = []
    for k, v in match_pair.items():
        set_a.append([k.x, k.y, k.z])
        set_b.append([v.x, v.y, v.z])
    mat_a = np.array(set_a)
    mat_b = np.array(set_b)

    centroid_a = np.mean(mat_a, axis=1).reshape(-1, 1)
    centroid_b = np.mean(mat_b, axis=1).reshape(-1, 1)

    mat_am = mat_a - centroid_a
    mat_bm = mat_b - centroid_b

    H = mat_am @ np.transpose(mat_bm)
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = Vt.T @ U.T

    t = -R @ centroid_a + centroid_b

    mat_b2 = R @ mat_a + t
    mat_e = mat_b2 - mat_b
    mat_e = mat_e * mat_e
    err = np.sum(mat_e)
    rmse = np.sqrt(err / len(match_pair))
    return rmse
