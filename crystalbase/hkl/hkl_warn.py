import numpy as np
import pandas as pd

from .space_group import generate_pairs_by_laue


def check_laue(hkl_file, laue, error_rate):
    hkl_data = HKLData(hkl_file)
    pairs = hkl_data.find_pairs_by_laue(laue)
    result = hkl_data.check_pairs_by_laue(pairs, error_rate)
    df_result = pd.DataFrame(result)
    result_str = ''
    for i, row in df_result.iterrows():
        result_str += '{}:\n'.format(i + 1)
        for hkl in row['hkl']:
            result_str += '{}\n'.format(hkl)
        result_str += 'outliers: {}\n'.format(row['outliers'])
    return len(df_result), result_str


def check_seq(hkl_file, laue, error_rate, seq_pattern):
    hkl_data = HKLData(hkl_file)
    seq = hkl_data.find_seq_by_pattern(seq_pattern)
    result = hkl_data.check_seq_by_laue(laue, seq)
    df_result = pd.DataFrame(result)
    result_str = ''
    for i, row in df_result.iterrows():
        result_str += '{}. exist: {}\n'.format(i + 1, row['exist'])
        for hkl in row['hkl']:
            result_str += '{}\n'.format(hkl)
    return len(df_result), result_str


class HKLData:

    def __init__(self, hkl_file):
        df = pd.read_table(hkl_file, sep='\\s+', header=None, names=['h', 'k', 'l', 'Int', 'sInt', 'phase'])
        df['h'] = df['h'].astype(int)
        df['k'] = df['k'].astype(int)
        df['l'] = df['l'].astype(int)
        self.hkl_dict = {}
        for index, row in df.iterrows():
            hkl_tuple = tuple(map(int, [row['h'], row['k'], row['l']]))
            if hkl_tuple in self.hkl_dict:
                #  TODO 支持重复HKL指标
                print('发现重复的HKL指标{}，当前版本程序暂不支持，后出现的会覆盖前者'.format(hkl_tuple))
            self.hkl_dict[hkl_tuple] = (row['Int'], row['sInt'], row['phase'])

    def _find_outlier(self, int_list, error_rate):
        outlier = []
        if len(int_list) == 1:  # 只有一个点，不需要计算离群值
            return outlier
        all_mean = np.mean([self.hkl_dict[hkl][0] for hkl in int_list])  # 所有hkl的平均强度
        for test_hkl in int_list:
            other_mean = np.mean([self.hkl_dict[hkl][0] for hkl in int_list if hkl != test_hkl])  # 排除test_hkl之后的平均强度
            t_value = np.abs(all_mean - other_mean) / self.hkl_dict[test_hkl][1]  # 均值之差 / sigma
            if t_value > error_rate:
                outlier.append(test_hkl)
        return outlier

    def find_pairs_by_laue(self, laue):
        result = []
        dup_check = set()
        for hkl_tuple in self.hkl_dict:
            if hkl_tuple in dup_check:  # 已经包含在其他组里
                continue
            new_pair_list = generate_pairs_by_laue(hkl_tuple, laue)  # 按对称性分在同一组的hkl指标
            exist_pair_list = [hkl for hkl in new_pair_list if hkl in self.hkl_dict]
            dup_check = dup_check.union(exist_pair_list)
            result.append({'hkl': exist_pair_list})
        return result

    def check_pairs_by_laue(self, pair_list, error_rate):
        result = []
        for p in pair_list:
            pairs = p['hkl']
            outliers = self._find_outlier(pairs, error_rate)
            if len(outliers) != 0:
                result.append({'hkl': [(*p, *self.hkl_dict[p]) for p in pairs], 'outliers': outliers})
        return result

    def find_seq_by_pattern(self, pattern, n_limit=20):
        result = []
        sh, sk, sl = pattern
        for i in range(1, n_limit + 1):
            params = {'h': i, 'k': i, 'l': i, 'n': i}
            hkl_tuple = eval(sh, params), eval(sk, params), eval(sl, params)
            result.append({'hkl': hkl_tuple, 'exist': hkl_tuple in self.hkl_dict})
        return result

    def check_seq_by_laue(self, laue, sequence):
        result = []
        for hkl_seq in sequence:
            hkl_tuple = hkl_seq['hkl']
            if hkl_seq['exist']:
                hkl_tuples = generate_pairs_by_laue(hkl_tuple, laue)
                exist_hkl_list = [hkl for hkl in hkl_tuples if hkl in self.hkl_dict]
                exist_int_list = [(*p, *self.hkl_dict[p]) for p in exist_hkl_list]
                result.append({'hkl': exist_int_list, 'exist': True})
            else:
                result.append({'hkl': [hkl_tuple], 'exist': False})
        return result