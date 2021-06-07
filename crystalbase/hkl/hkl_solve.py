import os
import subprocess


def _copy(src, dst):
    src_file = open(src, 'r')
    src_str = src_file.read()
    src_file.close()
    dst_file = open(dst, 'w')
    dst_file.write(src_str)
    dst_file.close()


def solve_hkl(hkl_file: str, ins_file: str, program='shelxs', params=''):
    # 打开求解工作目录
    temp_path = os.path.dirname(__file__) + '/../../.solve_workspace/'
    hkl_path, hkl_full_name = os.path.split(hkl_file)
    ins_path, ins_full_name = os.path.split(ins_file)
    hkl_name = hkl_full_name.split('.')[0]
    ins_name = ins_full_name.split('.')[0]
    new_name = '%s_%s' % (hkl_name, ins_name)
    output_path = temp_path + new_name
    # 重命名hkl和ins并复制到求解工作目录
    _copy(hkl_file, '%s.hkl' % output_path)
    _copy(ins_file, '%s.ins' % output_path)
    # 记录目录下已存在的RES文件
    old_res = set()
    for file in os.listdir(temp_path):
        if file.endswith('.res'):
            old_res.add(file)
    # 执行求解程序，阻塞式
    command = program + ' ' + new_name
    if params != '':
        command += command + ' ' + params
    do = subprocess.Popen(command, cwd=temp_path, shell=True, env={'PATH': temp_path})
    do.wait()
    # 删除临时hkl和ins
    try:
        if 'shelxt' in program:
            # shelxt会生成新的hkl，可以删掉旧的
            os.remove('%s.hkl' % output_path)
        os.remove('%s.ins' % output_path)
        os.remove('%s.lst' % output_path)
        os.remove('%s.lxt' % output_path)
    except FileNotFoundError:
        # xs生成lst，shelxt生成lxt
        pass
    # 筛选出新RES文件并返回
    new_res = []
    for file in os.listdir(temp_path):
        if file.endswith('.res') and file not in old_res:
            new_res.append(file)
    return new_res
