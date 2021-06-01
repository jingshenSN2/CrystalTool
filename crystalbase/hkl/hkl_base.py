import numpy as np
import pandas as pd

from .space_group import generate_pairs_by_laue


class HKLData:

    def __init__(self, hkl_file):
        self.hkl_df = pd.read_table(hkl_file, sep='\\s+', header=None,
                                    names=['h', 'k', 'l', 'Int', 'sInt', 'phase', 'z', 'b']).fillna(1)

        self.int_df = self.hkl_df['Int'].apply(np.abs)
        self.sigma_df = self.hkl_df['sInt'].apply(np.abs)
        self.hkl_dict = {}
        for index, row in self.hkl_df.iterrows():
            hkl_tuple = tuple(map(int, [row['h'], row['k'], row['l']]))
            if hkl_tuple not in self.hkl_dict:
                self.hkl_dict[hkl_tuple] = []
            self.hkl_dict[hkl_tuple].append(index)  # 保存hkl指标行号

    def find_pairs_by_laue(self, laue):
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

    def save_to_hkl(self, filename='new.hkl', remove_indexes=None, save_phase=False):
        hkl_df_copy = self.hkl_df.copy()
        if remove_indexes is not None:
            hkl_df_copy.drop(remove_indexes, inplace=True)
        new_hkl_str = ''
        for _, row in hkl_df_copy.iterrows():
            new_hkl_str += ' {:3d} {:3d} {:3d} {:7.2f} {:7.2f}\n'.format(int(row['h']), int(row['k']),
                                                                         int(row['l']), row['Int'],
                                                                         row['sInt'])
        new_hkl = open(filename, 'w+')
        new_hkl.write(new_hkl_str)
        new_hkl.close()
