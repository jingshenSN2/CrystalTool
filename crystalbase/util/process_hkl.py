import os
import re
import subprocess

import numpy as np


def _copy(src, dst):
    src_file = open(src, 'r')
    src_str = src_file.read()
    src_file.close()
    dst_file = open(dst, 'w')
    dst_file.write(src_str)
    dst_file.close()


def solve_hkl(hkl_file: str, ins_file: str, program='shelxt.exe', params=''):
    # ��shelxt������ʱ·��
    temp_path = os.path.dirname(__file__) + '/../../.temp/'
    hkl_path, hkl_full_name = os.path.split(hkl_file)
    ins_path, ins_full_name = os.path.split(ins_file)
    hkl_name = hkl_full_name.split('.')[0]
    ins_name = ins_full_name.split('.')[0]
    new_name = '%s_%s' % (hkl_name, ins_name)
    output_path = temp_path + new_name
    # �����������Ƶ���ʱ�ļ���
    _copy(hkl_file, '%s.hkl' % output_path)
    _copy(ins_file, '%s.ins' % output_path)
    # ��¼Ŀ¼���Ѵ��ڵ�RES�ļ�
    old_res = set()
    for file in os.listdir(temp_path):
        if file.endswith('.res'):
            old_res.add(file)
    # ִ��shelxt������ʽ
    command = [program, new_name]
    shelxt_params = params.split(' ')
    command.extend(shelxt_params)
    subprocess.Popen(command, cwd=temp_path, shell=True).wait()
    # ɾ����ʱhkl��ins
    os.remove('%s.hkl' % output_path)
    os.remove('%s.ins' % output_path)
    os.remove('%s.lxt' % output_path)
    # ɸѡ����RES�ļ�������
    new_res = []
    for file in os.listdir(temp_path):
        if file.endswith('.res') and file not in old_res:
            new_res.append(file)
    return new_res


edit_hkl_methods = {0: 'undefined', 1: 'expFS', 2: 'expF', 3: 'expS', 4: 'scale'}
float_pat = re.compile('(-?\\d+\\.\\d*)\\s+(-?\\d+\\.\\d*)')


def _edit_line(line, method, param):
    new_line = line
    #  δѡ���޸ķ�ʽ ����
    if method == 0:
        print('undefined')
        return new_line
    # ����ƥ���������������ֱ���ǿ�Ⱥ�ǿ�ȷ���
    result = re.search(float_pat, line).groups()
    if result is None:
        return new_line
    intensity, sigma = result[0], result[1]
    intensity_f, sigma_f = float(intensity), float(sigma)

    # ������ǿ��
    def smart_exp(a):
        if a == 0:
            return a
        symbol = abs(a) / a
        return symbol * pow(symbol * a, param)

    new_intensity, new_sigma = intensity_f, sigma_f
    if method == 1:  # ǿ���ݣ�F+sigma��
        new_intensity, new_sigma = smart_exp(intensity_f), smart_exp(sigma_f)
    elif method == 2:  # ǿ���ݣ�F��
        new_intensity = smart_exp(intensity_f)
    elif method == 3:  # ǿ���ݣ�sigma��
        new_sigma = smart_exp(sigma_f)
    elif method == 4:  # ǿ���������ţ�F+sigma��
        new_intensity, new_sigma = intensity_f / param, sigma_f / param

    # ǿ���滻���µ�
    new_line = new_line.replace(intensity, '%.2f' % new_intensity, 1)
    new_line = new_line.replace(sigma, '%.2f' % new_sigma, 1)

    return new_line


def _parse_params(params_str: str):
    sub_params_str = params_str.split(',')
    params = []
    for sub_str in sub_params_str:
        if ':' in sub_str:  # begin:step:endģʽ
            begin, step, end = map(float, sub_str.split(':'))
            params.extend(np.arange(start=begin, stop=end, step=step))
        else:  # ��������ģʽ
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
        # �������ļ�
        p_str = str(round(p, 2)).replace('.', '_')
        new_hkl_file = hkl_file.replace('.hkl', '_%s_%s.hkl' % (edit_hkl_methods[method], p_str))
        new_hkl = open(new_hkl_file, 'w')
        for line in hkl_lines:
            # ����ÿ�в�д�����ļ�
            new_line = _edit_line(line, method, p)
            new_hkl.write(new_line)
        new_hkl.close()
        output_list.append(new_hkl_file)
    return output_list
