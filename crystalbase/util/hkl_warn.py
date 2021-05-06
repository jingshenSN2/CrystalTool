import pandas as pd


def check_pattern(hkl_file, pattern):
    pass


def check_sequence(hkl_file, sequence):
    return 1, 1, 2


class HKLData:

    def __init__(self, hkl_file):
        df = pd.read_table(hkl_file, sep='\\s+', header=None, names=['h', 'k', 'l', 'Int', 'sInt', 'phase'])
        self.line_number = {}
        self.hkl_dict = {}
        for index, row in df.iterrows():
            hkl_tuple = (row['h'], row['k'], row['l'])
            self.line_number[hkl_tuple] = index + 1
            self.hkl_dict[hkl_tuple] = (row['Int'], row['sInt'], row['phase'])

    def find_pairs_by_pattern(self, pattern):
        pairs = {}
        for hkl_tuple in self.hkl_dict:
            if not check_pattern(hkl_tuple, pattern):
                continue
            pair_hkl_tuple = generate_hkl_by_pattern(hkl_tuple, pattern)
            if pair_hkl_tuple in self.hkl_dict:
                pairs[hkl_tuple] = pair_hkl_tuple
        return pairs

    def check_equal_pair(self, pairs, threshold=3):
        for k, v in pairs.items():
            pass
