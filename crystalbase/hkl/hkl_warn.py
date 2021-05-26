import numpy as np
import pandas as pd

from .space_group import generate_pairs_by_laue


def _print_table(table):
    table_str = ''
    hkl_format = '  ({}, {}, {}): ({}, {}, {})\n'  # 依次是h,k,l,F2,sigma(F2),phase
    for row in table:
        table_str += hkl_format.format(int(row[0]), int(row[1]), int(row[2]), row[3], row[4], int(row[5]))
    return table_str


def check_laue(hkl_file, laue, z_value, error_rate, recursive):
    hkl_data = HKLData(hkl_file)
    result = hkl_data.check_pairs_by_laue(laue, z_value, error_rate, recursive)
    result_len = len(result)
    result_str = ''
    for i in range(result_len):
        result_str += '{} normal:\n'.format(i + 1)
        result_str += _print_table(result[i]['normal'])  # 强度正常的指标
        if len(result[i]['high_var']) != 0:
            result_str += '  high_var:\n'
            result_str += _print_table(result[i]['high_var'])  # 强度方差过大的指标
        result_str += '  outliers:\n'
        result_str += _print_table(result[i]['outliers'])  # 强度离群的指标
        result_str += '\n'
    return result_len, result_str


def check_seq(hkl_file, laue, error_rate, seq_pattern):
    hkl_data = HKLData(hkl_file)
    result = hkl_data.check_seq_by_laue(laue, seq_pattern)
    result_len = len(result)
    result_str = ''
    for i in range(len(result)):
        result_str += 'n={} {}\n'.format(i + 1, '' if result[i]['exist'] else 'not exists')
        result_str += _print_table(result[i]['hkl_list'])
        result_str += '\n'
    return result_len, result_str


class HKLData:

    def __init__(self, hkl_file):
        self.hkl_df = pd.read_table(hkl_file, sep='\\s+', header=None,
                                    names=['h', 'k', 'l', 'Int', 'sInt', 'phase']).fillna(-1)
        self.int_df = self.hkl_df['Int'].apply(np.abs)
        self.sigma_df = self.hkl_df['sInt'].apply(np.abs)
        self.hkl_dict = {}
        for index, row in self.hkl_df.iterrows():
            hkl_tuple = tuple(map(int, [row['h'], row['k'], row['l']]))
            if hkl_tuple not in self.hkl_dict:
                self.hkl_dict[hkl_tuple] = []
            self.hkl_dict[hkl_tuple].append(index)  # 保存hkl指标行号

    def _find_outlier_recursive(self, index_list, error_rate):
        outlier = []
        if len(index_list) <= 1:  # 一个点，不需要计算离群值
            return outlier
        intensity = self.int_df[index_list]
        q75, q25 = np.percentile(intensity, [75, 25])
        for test_idx in index_list:
            sigma = self.sigma_df[test_idx]
            if q25 - error_rate * sigma < self.int_df[test_idx] < q75 + error_rate * sigma:
                continue
            outlier.append(test_idx)
        return outlier

    def _find_outlier(self, index_list, error_rate, recursive=False):
        outlier = new_outlier = self._find_outlier_recursive(index_list, error_rate)
        normal = [idx for idx in index_list if idx not in outlier]
        if not recursive:
            return outlier, normal
        while True:
            if len(new_outlier) == 0:
                return outlier, normal
            new_outlier = self._find_outlier_recursive(normal, error_rate)
            outlier.extend(new_outlier)
            normal = [idx for idx in normal if idx not in new_outlier]

    def _find_high_var(self, index_list, z_value):
        high_var = []
        normal_var = []
        for test_idx in index_list:
            if self.int_df[test_idx] > z_value * self.sigma_df[test_idx]:
                normal_var.append(test_idx)
            else:
                high_var.append(test_idx)  # 强度小于z_value倍的方差
        return high_var, normal_var

    def _find_pairs_by_laue(self, laue):
        result = []  # 按laue群分组后的所有hkl
        dup_check = set()
        for hkl_tuple in self.hkl_dict:
            if hkl_tuple in dup_check:  # 已经包含在其他组里
                continue
            new_pair_list = generate_pairs_by_laue(hkl_tuple, laue)  # 按对称性分在同一组的hkl指标
            exist_pair_list = [hkl for hkl in new_pair_list if hkl in self.hkl_dict]  # 存在的hkl指标
            dup_check = dup_check.union(exist_pair_list)
            result.append({'hkl': exist_pair_list})
        return result

    def check_pairs_by_laue(self, laue, z_value, error_rate, recursive):
        result = []
        all_pairs_list = self._find_pairs_by_laue(laue)
        for pairs_list in all_pairs_list:
            pairs = pairs_list['hkl']
            index_of_pairs = []
            for p in pairs:  # 记录该组的所有行号
                index_of_pairs.extend(self.hkl_dict[p])
            high_var, normal_var = self._find_high_var(index_of_pairs, z_value)  # 强度方差过大的指标
            outliers, normal = self._find_outlier(normal_var, error_rate, recursive)  # 只在方差正常的指标里找离群值
            if len(outliers) > 0:  # 发现异常，汇报
                result.append({'normal': self.hkl_df.values[normal],
                               'high_var': self.hkl_df.values[high_var],
                               'outliers': self.hkl_df.values[outliers]})
        return result

    def check_seq_by_laue(self, laue, seq_pattern, n_limit=30):
        result = []
        sequence = []
        sh, sk, sl = seq_pattern
        for i in range(1, n_limit + 1):
            params = {'h': i, 'k': i, 'l': i, 'n': i}
            hkl_tuple = eval(sh, params), eval(sk, params), eval(sl, params)  # 按n计算hkl指标
            sequence.append(hkl_tuple)

        last_exist = 0  # 记录最后一个存在的指标
        for i in range(len(sequence)):
            hkl_tuple = sequence[i]
            hkl_tuples = generate_pairs_by_laue(hkl_tuple, laue)
            exist_hkl_list = []
            for hkl in hkl_tuples:
                if hkl in self.hkl_dict:
                    exist_hkl_list.extend(self.hkl_dict[hkl])  # 存在的指标
                    last_exist = i
            result.append({'hkl': hkl_tuple,
                           'hkl_list': self.hkl_df.values[exist_hkl_list],
                           'exist': len(exist_hkl_list) != 0})
        return result[:last_exist + 1]  # 舍去后面不存在的指标
