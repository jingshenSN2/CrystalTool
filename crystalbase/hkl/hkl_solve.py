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
    solve_params = params.split(' ')
    command.extend(solve_params)
    subprocess.Popen(command, cwd=temp_path, shell=True).wait()
    # ɾ����ʱhkl��ins
    try:
        if program == 'shelxt.exe':
            os.remove('%s.hkl' % output_path)
        os.remove('%s.ins' % output_path)
        os.remove('%s.lst' % output_path)
        os.remove('%s.lxt' % output_path)
    except FileNotFoundError:
        pass
    # ɸѡ����RES�ļ�������
    new_res = []
    for file in os.listdir(temp_path):
        if file.endswith('.res') and file not in old_res:
            new_res.append(file)
    return new_res
