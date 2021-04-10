import os
import subprocess

import numpy as np


def _copy(src, dst):
    src_file = open(src, 'r')
    src_str = src_file.read()
    src_file.close()
    dst_file = open(dst, 'w')
    dst_file.write(src_str)
    dst_file.close()


def solve_hkl(hkl_file: str, ins_file: str, program='shelxt.exe'):
    # 打开shelxt计算临时路径
    temp_path = os.path.dirname(__file__) + '/../../.temp/'
    hkl_path, hkl_full_name = os.path.split(hkl_file)
    ins_path, ins_full_name = os.path.split(ins_file)
    hkl_name = hkl_full_name.split('.')[0]
    ins_name = ins_full_name.split('.')[0]
    new_name = '%s_%s' % (hkl_name, ins_name)
    output_path = temp_path + new_name
    # 重命名并复制到临时文件夹
    _copy(hkl_file, '%s.hkl' % output_path)
    _copy(ins_file, '%s.ins' % output_path)
    # 记录目录下已存在的RES文件
    old_res = set()
    for file in os.listdir(temp_path):
        if file.endswith('.res'):
            old_res.add(file)
    # 执行shelxt，阻塞式
    subprocess.Popen([program, new_name], cwd=temp_path, shell=True).wait()
    # 删除临时hkl和ins
    os.remove('%s.hkl' % output_path)
    os.remove('%s.ins' % output_path)
    # 筛选出新RES文件并返回
    new_res = []
    for file in os.listdir(temp_path):
        if file.endswith('.res') and file not in old_res:
            new_res.append(file)
    if len(new_res) == 0:
        # 求解失败则移除日志
        os.remove('%s.lxt' % output_path)
    return new_res


edit_hkl_methods = {0: 'undefined', 1: 'expFS', 2: 'expF', 3: 'expS', 4: 'scale'}


def _edit_line(line, method, param):
    new_line = line
    #  未选择修改方式 跳过
    if method == 0:
        print('undefined')
        return new_line, True
    sp = line.split()
    if len(sp) <= 3:
        # 跳过非关键行
        new_line = line
    else:
        h, k, l = map(int, sp[:3])  # 衍射指标
        F, sigma = map(float, sp[3:5])  # 强度和强度误差
        if h == k == l == 0:
            return new_line, True

        def smart_exp(a):  # 求幂函数，对于负数自动取绝对值求幂后补上符号
            if a == 0:
                return str(a)
            symbol = abs(a) / a
            return str(round(symbol * pow(symbol * a, param), 2))

        if method == 1:  # 强度幂（F+sigma）
            sp[3], sp[4] = smart_exp(F), smart_exp(sigma)
        elif method == 2:  # 强度幂（F）
            sp[3] = smart_exp(F)
        elif method == 3:  # 强度幂（sigma）
            sp[4] = smart_exp(sigma)
        elif method == 4:  # 强度缩放
            sp[3], sp[4] = str(round(F * param, 2)), str(round(sigma * param, 2))

        def indent(word, sep=' ', num=4):  # 保持hkl的格式
            return sep * (num - len(word)) + word

        new_line = indent(str(h)) + indent(str(k)) + indent(str(l)) + '  %s  %s  %s\n' % (sp[3], sp[4], sp[5])
    return new_line, False


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
            new_line, stop = _edit_line(line, method, p)
            new_hkl.write(new_line)
            if stop:
                break
        new_hkl.close()
        output_list.append(new_hkl_file)
    return output_list
