import os
import subprocess


def _copy(src, dst):
    src_file = open(src, 'r')
    src_str = src_file.read()
    src_file.close()
    dst_file = open(dst, 'w')
    dst_file.write(src_str)
    dst_file.close()


def solve_hkl(hkl_file: str, ins_file: str, program='xs.exe', params=''):
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
    command = [program, new_name]
    solve_params = params.split(' ')
    command.extend(solve_params)
    subprocess.Popen(command, cwd=temp_path, shell=True).wait()
    # 删除临时hkl和ins
    try:
        if program == 'shelxt.exe':
            os.remove('%s.hkl' % output_path)
        os.remove('%s.ins' % output_path)
        os.remove('%s.lst' % output_path)
        os.remove('%s.lxt' % output_path)
    except FileNotFoundError:
        pass
    # 筛选出新RES文件并返回
    new_res = []
    for file in os.listdir(temp_path):
        if file.endswith('.res') and file not in old_res:
            new_res.append(file)
    return new_res
