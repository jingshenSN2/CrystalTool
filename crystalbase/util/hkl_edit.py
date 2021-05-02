import re

import numpy as np
import pandas as pd

edit_hkl_methods = {0: 'expFS', 1: 'expF', 2: 'expS'}
float_pat = re.compile('(-?\\d+\\.\\d*)\\s+(-?\\d+\\.\\d*)')


def _smart_exp(a, p):
    if a == 0:
        return a
    symbol = abs(a) / a
    return symbol * pow(symbol * a, p)


def _edit_line(line, method, param, is_scale, hkl_min, hkl_max, scaler_min, scaler_max):
    new_line = line
    # 正则匹配两个浮点数，分别是强度和强度方差
    result = re.search(float_pat, line).groups()
    if result is None:
        return new_line
    intensity, sigma = result[0], result[1]
    intensity_f, sigma_f = float(intensity), float(sigma)
    new_intensity, new_sigma = intensity_f, sigma_f
    if method in [0, 1]:  # 强度幂（F）
        new_intensity = _smart_exp(intensity_f, param)
        hkl_max = _smart_exp(hkl_max, param)
    elif method in [0, 2]:  # 强度幂（sigma）
        new_sigma = _smart_exp(sigma_f, param)

    if is_scale:
        new_intensity = scaler_min + (scaler_max - scaler_min) * (new_intensity - hkl_min) / (hkl_max - hkl_min)
        new_sigma = (scaler_max - scaler_min) * new_sigma / (hkl_max - hkl_min)

    # 强度替换成新的
    new_line = new_line.replace(intensity, '%.2f' % new_intensity, 1)
    new_line = new_line.replace(sigma, '%.2f' % new_sigma, 1)
    return new_line


def _parse_params(params_str: str):
    sub_params_str = params_str.split(',')
    params = []
    for sub_str in sub_params_str:
        if ':' in sub_str:  # begin:step:end模式
            begin, step, end = map(float, sub_str.split(':'))
            params.extend(np.arange(start=begin, stop=end, step=step))
        else:  # 单独数字模式
            p = float(sub_str)
            params.append(p)
    return params


def edit_hkl(hkl_file: str, method: int, params_str: str, is_scale, scaler_min, scaler_max):
    df = pd.read_table(hkl_file, sep='\\s+', header=None, names=['h', 'k', 'l', 'Int', 'sInt', 'phase'])
    hkl_min = df['Int'].min()
    hkl_max = df['Int'].max()

    hkl = open(hkl_file, 'r')
    hkl_lines = hkl.readlines()
    hkl.close()

    output_list = []
    params = _parse_params(params_str)
    for p in params:
        # 创建新文件
        p_str = str(round(p, 2)).replace('.', '_')
        new_hkl_file = hkl_file.replace('.hkl', '_%s_%s.hkl' % (edit_hkl_methods[method], p_str))
        new_hkl = open(new_hkl_file, 'w')
        for line in hkl_lines:
            # 处理每行并写入新文件
            new_line = _edit_line(line, method, p, is_scale, hkl_min, hkl_max, scaler_min, scaler_max)
            new_hkl.write(new_line)
        new_hkl.close()
        output_list.append(new_hkl_file)
    return output_list
