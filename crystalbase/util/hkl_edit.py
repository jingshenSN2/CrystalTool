import re

import numpy as np

edit_hkl_methods = {0: 'undefined', 1: 'expFS', 2: 'expF', 3: 'expS', 4: 'scale'}
float_pat = re.compile('(-?\\d+\\.\\d*)\\s+(-?\\d+\\.\\d*)')


def _edit_line(line, method, param):
    new_line = line
    #  未选择修改方式 跳过
    if method == 0:
        print('undefined')
        return new_line
    # 正则匹配两个浮点数，分别是强度和强度方差
    result = re.search(float_pat, line).groups()
    if result is None:
        return new_line
    intensity, sigma = result[0], result[1]
    intensity_f, sigma_f = float(intensity), float(sigma)

    # 计算新强度
    def smart_exp(a):
        if a == 0:
            return a
        symbol = abs(a) / a
        return symbol * pow(symbol * a, param)

    new_intensity, new_sigma = intensity_f, sigma_f
    if method == 1:  # 强度幂（F+sigma）
        new_intensity, new_sigma = smart_exp(intensity_f), smart_exp(sigma_f)
    elif method == 2:  # 强度幂（F）
        new_intensity = smart_exp(intensity_f)
    elif method == 3:  # 强度幂（sigma）
        new_sigma = smart_exp(sigma_f)
    elif method == 4:  # 强度线性缩放（F+sigma）
        new_intensity, new_sigma = intensity_f / param, sigma_f / param

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


def edit_hkl(hkl_file: str, method: int, params_str: str):
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
            new_line = _edit_line(line, method, p)
            new_hkl.write(new_line)
        new_hkl.close()
        output_list.append(new_hkl_file)
    return output_list
