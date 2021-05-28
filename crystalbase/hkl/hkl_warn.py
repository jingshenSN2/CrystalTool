import numpy as np

from .hkl_base import HKLData
from .space_group import generate_pairs_by_laue


normal_format = '{:5d} {:3d} {:3d} {:3d} {:9.2f} {:9.2f} {:2d}\n'
issue_format = '{:5d} {:3d} {:3d} {:3d} {:9.2f} {:9.2f} {:2d} {:5.2f}\n'


def check_laue(hkl_file: str, laue: int, z_value: float, error_rate: float, recursive: bool, save_option: dict):
    hkl_data = HKLData(hkl_file)
    issue_count = 0
    issue_str = '#line  h    k    l     F2   sigma   p  Z/b\n'
    all_pairs_list = hkl_data.find_pairs_by_laue(laue)
    all_high_var_indexes = []
    all_outlier_indexes = []
    for pairs_list in all_pairs_list:
        pairs = pairs_list['hkl']
        index_of_pairs = []
        for p in pairs:  # 记录该组的所有行号
            index_of_pairs.extend(hkl_data.hkl_dict[p])
        high_var, normal_var = _find_high_var(hkl_data, index_of_pairs, z_value)  # 强度方差过大的指标
        outliers, normal = _find_outlier(hkl_data, normal_var, error_rate, recursive)  # 只在方差正常的指标里找离群值
        if len(high_var) + len(outliers) > 0:  # 发现异常，汇报
            issue_count += 1
            issue_str += '{}:\n'.format(issue_count)
            issue_str += _report_issue_str(hkl_data.hkl_df.iloc[normal, :],
                                           hkl_data.hkl_df.iloc[high_var, :],
                                           hkl_data.hkl_df.iloc[outliers, :])
            all_high_var_indexes.extend(high_var)
            all_outlier_indexes.extend(outliers)

    #  保存功能
    remove_indexes = []
    if save_option['remove_high_var']:
        remove_indexes.extend(all_high_var_indexes)
    if save_option['remove_outlier']:
        remove_indexes.extend(all_outlier_indexes)

    new_hkl_file = hkl_file.replace('.hkl', '_new.hkl')

    hkl_data.save_to_hkl(new_hkl_file, remove_indexes=remove_indexes)

    return issue_count, issue_str


def _report_issue_str(normal_df, high_var_df, outlier_df):
    issue_str = 'normal:\n'
    for idx, row in normal_df.iterrows():
        issue_str += normal_format.format(idx, int(row['h']), int(row['k']), int(row['l']), row['Int'], row['sInt'],
                                          int(row['phase']))

    if len(high_var_df) > 0:
        issue_str += 'high_var:\n'
        for idx, row in high_var_df.iterrows():
            issue_str += issue_format.format(idx, int(row['h']), int(row['k']), int(row['l']), row['Int'], row['sInt'],
                                             int(row['phase']), row['z'])

    if len(outlier_df) > 0:
        issue_str += 'outlier:\n'
        for idx, row in outlier_df.iterrows():
            issue_str += issue_format.format(idx, int(row['h']), int(row['k']), int(row['l']), row['Int'], row['sInt'],
                                             int(row['phase']), row['b'])
    issue_str += '\n'
    return issue_str


def _find_high_var(hkl_data, index_list, z_value):
    high_var = []
    normal_var = []
    for test_idx in index_list:
        sigma = hkl_data.sigma_df[test_idx]
        if sigma == 0:  # 对最后一行0 0 0 0.00 0.00不作处理
            continue
        z_exp = hkl_data.int_df[test_idx] / sigma
        if z_exp > z_value:
            normal_var.append(test_idx)  # 强度大于z_value倍的方差，正常值
        else:
            high_var.append(test_idx)  # 强度小于z_value倍的方差，不显著值
            hkl_data.hkl_df.loc[test_idx, 'z'] = z_exp
    return high_var, normal_var


def _find_outlier(hkl_data, index_list, error_rate, recursive=False):
    outlier = new_outlier = _find_outlier_recursive(hkl_data, index_list, error_rate)
    normal = [idx for idx in index_list if idx not in outlier]  # 一阶正常值和离群值
    if not recursive:  # 非迭代模式直接返回一阶值
        return outlier, normal
    while True:
        if len(new_outlier) == 0:
            return outlier, normal
        new_outlier = _find_outlier_recursive(hkl_data, normal, error_rate)  # 高阶离群值
        outlier.extend(new_outlier)
        normal = [idx for idx in normal if idx not in new_outlier]


def _find_outlier_recursive(hkl_data, index_list, error_rate):
    outlier = []
    if len(index_list) <= 1:  # 一个点，不需要计算离群值
        return outlier
    intensities = hkl_data.int_df[index_list]
    q75, q25 = np.percentile(intensities, [75, 25])  # 计算四分位数
    for test_idx in index_list:
        inst = hkl_data.int_df[test_idx]
        sigma = hkl_data.sigma_df[test_idx]
        b1 = (q25 - inst) / sigma  # 左侧b值
        b2 = (inst - q75) / sigma  # 右侧b值
        if b1 > error_rate:
            hkl_data.hkl_df.loc[test_idx, 'b'] = b1
            outlier.append(test_idx)
        elif b2 > error_rate:
            hkl_data.hkl_df.loc[test_idx, 'b'] = b2
            outlier.append(test_idx)
    return outlier


def check_seq(hkl_file, laue, error_rate, seq_pattern):
    hkl_data = HKLData(hkl_file)
    sequence = []
    sh, sk, sl = seq_pattern
    for i in range(1, 41):
        params = {'h': i, 'k': i, 'l': i, 'n': i}
        hkl_tuple = eval(sh, params), eval(sk, params), eval(sl, params)  # 按n计算hkl指标
        sequence.append(hkl_tuple)

    result_str_list = ['#line  h    k    l     F2   sigma   p  Z/b\n']
    last_exist = 0  # 记录最后一个存在的指标
    for i in range(len(sequence)):
        hkl_tuple = sequence[i]
        hkl_tuples = generate_pairs_by_laue(hkl_tuple, laue)
        exist_hkl_list = []
        for hkl in hkl_tuples:
            if hkl in hkl_data.hkl_dict:
                exist_hkl_list.extend(hkl_data.hkl_dict[hkl])  # 存在的指标
                last_exist = i
        temp_str = 'n={} {}\n'.format(i + 1, '' if len(exist_hkl_list) != 0 else 'not exists')
        for idx, row in hkl_data.hkl_df.iloc[exist_hkl_list, :].iterrows():
            temp_str += normal_format.format(idx, int(row['h']), int(row['k']), int(row['l']), row['Int'], row['sInt'],
                                             int(row['phase']))
        result_str_list.append(temp_str)

    result_str = ''.join(result_str_list[:last_exist + 1])

    return last_exist + 1, result_str
