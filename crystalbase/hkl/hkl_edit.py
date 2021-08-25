import numpy as np

from .hkl_base import HKLData

edit_hkl_methods = {0: 'm1', 1: 'm2', 2: 'm3'}
edit_hkl_ranges = {0: 'f', 1: 's', 2: 'fs'}


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


def edit_hkl(hkl_file: str, method: int, edit_range: int, params_str: str, is_scale):
    hkl_data = HKLData(hkl_file)
    hkl_df = hkl_data.hkl_df

    output_list = []  # 输出文件的名称
    params = _parse_params(params_str)  # 解析参数范围
    for p in params:
        new_hkl_df = hkl_df.copy()

        def edit_one(num):
            new_num = np.abs(num)
            if method == 0:
                new_num = np.power(new_num, p)  # 方法1 I0 = I^p
            if method == 1:
                new_num = new_num * np.log(new_num * p)  # 方法2 I0 = I*log(I*p)
            if method == 2:
                new_num = new_num / p  # 方法3 I0 = I / p
            return new_num if num >= 0 else -new_num

        if edit_range in [0, 2]:  # 调整强度
            new_hkl_df['Int'] = new_hkl_df['Int'].apply(edit_one)
        if edit_range in [1, 2]:  # 调整方差
            new_hkl_df['sInt'] = new_hkl_df['sInt'].apply(edit_one)
        p_str = '{:.2f}'.format(p).replace('.', '_')
        # 新文件名
        new_hkl_file = hkl_file.replace('.hkl',
                                        '_%s_%s.hkl' % (edit_hkl_methods[method] + edit_hkl_ranges[edit_range], p_str))
        hkl_data.hkl_df = new_hkl_df
        hkl_data.save_to_hkl(new_hkl_file, norm=is_scale)  # 保存到新文件
        output_list.append(new_hkl_file)
    return output_list
