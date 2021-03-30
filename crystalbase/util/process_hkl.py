import os
import subprocess
from shutil import copy


def processHkl(hkl_file: str, ins_file: str):
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
