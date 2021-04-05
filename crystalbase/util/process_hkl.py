import os
import subprocess
from shutil import copy


def solve_hkl(hkl_file: str, ins_file: str):
    shelxt = os.path.dirname(__file__) + '/../../.temp/'
    hkl_path, hkl_full_name = os.path.split(hkl_file)
    ins_path, ins_full_name = os.path.split(ins_file)
    hkl_name = hkl_full_name.split('.')[0]
    ins_name = ins_full_name.split('.')[0]
    new_name = '%s_%s' % (hkl_name, ins_name)
    output_path = shelxt + new_name
    copy(hkl_file, '%s.hkl' % output_path)
    copy(ins_file, '%s.ins' % output_path)
    old_res = set()
    for file in os.listdir(shelxt):
        if file.endswith('.res'):
            old_res.add(file)
    subprocess.Popen(['shelxt.exe', new_name], cwd=shelxt, shell=True).wait()
    os.remove('%s.hkl' % output_path)
    os.remove('%s.ins' % output_path)
    new_res = []
    for file in os.listdir(shelxt):
        if file.endswith('.res') and file not in old_res:
            new_res.append(file)
    return new_res


edit_hkl_methods = {0: 'exp', 1: 'undefined'}


def edit_hkl(hkl_file: str, method: int, params: list):
    hkl = open(hkl_file, 'r')
    hkl_lines = hkl.readlines()
    hkl.close()
    output_list = []
    for p in params:
        new_hkl_file = hkl_file.replace('.hkl', '_%s_%s.hkl' % (edit_hkl_methods[method], str(p)))
        new_hkl = open(new_hkl_file, 'w')
        for line in hkl_lines:
            sp = line.split()
            if len(sp) <= 3:
                continue
            intensity = float(sp[3])
            if intensity < 0:
                intensity = -round(pow(-intensity, p), 2)
            else:
                intensity = round(pow(intensity, p), 2)
            sp[3] = str(intensity)
            new_hkl.write('%s\n' % ' '.join(sp))
            if sp[0] == sp[1] == sp[2] == '0':
                break
        new_hkl.close()
        output_list.append(new_hkl_file)
    return output_list
