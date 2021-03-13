import os
from shutil import copy


def process_one_hkl(hkl_file: str, ins_file: str):
    shelxt = os.path.dirname(__file__)
    os.putenv('PATH', shelxt)
    hkl_full_name = hkl_file.split('/')[-1]
    ins_full_name = ins_file.split('/')[-1]
    hkl_name = hkl_full_name.split('.')[0]
    ins_name = ins_full_name.split('.')[0]
    if hkl_name != ins_name:
        # shelxt 只接受一个name参数，所以需要复制一份ins重命名并保存
        new_ins_file = hkl_file.replace('.hkl', '.ins')
        copy(ins_file, new_ins_file)
    name = hkl_file.rstrip('.hkl')
    os.system('shelxt %s' % name)
