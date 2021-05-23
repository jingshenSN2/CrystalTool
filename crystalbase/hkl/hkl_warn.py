import numpy as np
import pandas as pd

from .space_group import generate_pairs_by_laue


def check_laue(hkl_file, laue, error_rate):
    hkl_data = HKLData(hkl_file)
    result = hkl_data.check_pairs_by_laue(laue, error_rate)
    result_len = len(result)
    result_str = ''
    for i in range(result_len):
        result_str += 'issue {}\n'.format(i + 1)
        for row in result[i]['hkl']:
            # 强度正常的指标
            result_str += '({}, {}, {}): ({}, {}, {})\n'.format(int(row[0]), int(row[1]), int(row[2]), row[3], row[4],
                                                                int(row[5]))
        result_str += ' outliers:\n'
        for row in result[i]['outliers']:
            # 强度异常的指标
            result_str += '({}, {}, {}): ({}, {}, {})\n'.format(int(row[0]), int(row[1]), int(row[2]), row[3], row[4],
                                                                int(row[5]))
        result_str += '\n'
    return result_len, result_str


def check_seq(hkl_file, laue, error_rate, seq_pattern):
    hkl_data = HKLData(hkl_file)
    result = hkl_data.check_seq_by_laue(laue, seq_pattern)
    result_len = len(result)
    result_str = ''
    for i in range(len(result)):
        result_str += '{}. {}:\n'.format(i + 1, result[i]['exist'])
        for row in result[i]['hkl_list']:
            result_str += '({}, {}, {}): ({}, {}, {})\n'.format(int(row[0]), int(row[1]), int(row[2]), row[3], row[4],
                                                                int(row[5]))
    return result_len, result_str


class HKLData:

    def __init__(self, hkl_file):
        self.hkl_df = pd.read_table(hkl_file, sep='\\s+', header=None,
                                    names=['h', 'k', 'l', 'Int', 'sInt', 'phase']).fillna(-1)
        self.int_df = self.hkl_df['Int']
        self.sigma_df = self.hkl_df['sInt']
        self.hkl_dict = {}
        for index, row in self.hkl_df.iterrows():
            hkl_tuple = tuple(map(int, [row['h'], row['k'], row['l']]))
            if hkl_tuple not in self.hkl_dict:
                self.hkl_dict[hkl_tuple] = []
            self.hkl_dict[hkl_tuple].append(index)  # 保存hkl指标行号

    def _find_outlier(self, index_list, error_rate):
        outlier = []
        if len(index_list) == 1:  # 一个点，不需要计算离群值
            return outlier
        intensity = self.int_df[index_list]
        q75, q25 = np.percentile(intensity, [75, 25])
        for test_idx in index_list:
            sigma = self.sigma_df[test_idx]
            if q25 - error_rate * sigma < self.int_df[test_idx] < q75 + error_rate * sigma:
                continue
            outlier.append(test_idx)
        # all_sd = np.std(self.int_df[index_list])  # 所有hkl的强度方差
        # for i in range(len(index_list)):
        #     test_idx = index_list[i]
        #     other_idx = index_list[:i] + index_list[i + 1:]
        #     other_sd = np.std(self.int_df[other_idx])  # 排除test_hkl之后的强度方差
        #     t_value = (all_sd - other_sd) / self.sigma_df[test_idx]
        #     if t_value > error_rate:
        #         outlier.append(test_idx)
        return outlier

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

    def check_pairs_by_laue(self, laue, error_rate):
        result = []
        all_pairs_list = self._find_pairs_by_laue(laue)
        for pairs_list in all_pairs_list:
            pairs = pairs_list['hkl']
            index_of_pairs = []
            for p in pairs:  # 记录该组的所有行号
                index_of_pairs.extend(self.hkl_dict[p])
            outliers = self._find_outlier(index_of_pairs, error_rate)
            if len(outliers) != 0:
                # 发现异常，汇报
                normal = [idx for idx in index_of_pairs if idx not in outliers]
                result.append({'hkl': self.hkl_df.values[normal], 'outliers': self.hkl_df.values[outliers]})
        return result

    def check_seq_by_laue(self, laue, seq_pattern, n_limit=20):
        result = []
        sequence = []
        sh, sk, sl = seq_pattern
        for i in range(1, n_limit + 1):
            params = {'h': i, 'k': i, 'l': i, 'n': i}
            hkl_tuple = eval(sh, params), eval(sk, params), eval(sl, params)  # 按n计算hkl指标
            sequence.append(hkl_tuple)
        for hkl_tuple in sequence:
            hkl_tuples = generate_pairs_by_laue(hkl_tuple, laue)
            exist_hkl_list = [hkl for hkl in hkl_tuples if hkl in self.hkl_dict]  # 存在的指标
            result.append({'hkl': hkl_tuple,
                           'hkl_list': self.hkl_df.values[exist_hkl_list],
                           'exist': len(exist_hkl_list) != 0})
        return result
