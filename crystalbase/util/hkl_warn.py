import pandas as pd


def check_pattern(hkl_file, pattern, conf_level):
    hkl_data = HKLData(hkl_file)
    pairs = hkl_data.find_pairs_by_pattern(pattern)
    result = hkl_data.check_equal_pairs(pairs, conf_level)
    return pd.DataFrame(result)


def check_sequence(hkl_file, sequence):
    return 1, 1, 2


def _generate_hkl_by_pattern(hkl_tuple, pattern):
    h, k, l = hkl_tuple
    ph, pk, pl = pattern
    new_hkl_tuple = eval(ph), eval(pk), eval(pl)
    return new_hkl_tuple


def _match_pattern(hkl_tuple, pattern):
    new_hkl_tuple = _generate_hkl_by_pattern(hkl_tuple, pattern)
    return hkl_tuple == new_hkl_tuple


class HKLData:

    def __init__(self, hkl_file):
        df = pd.read_table(hkl_file, sep='\\s+', header=None, names=['h', 'k', 'l', 'Int', 'sInt', 'phase'])
        self.line_number = {}
        self.hkl_dict = {}
        for index, row in df.iterrows():
            hkl_tuple = (row['h'], row['k'], row['l'])
            self.line_number[hkl_tuple] = index + 1
            self.hkl_dict[hkl_tuple] = (row['Int'], row['sInt'], row['phase'])

    def find_pairs_by_pattern(self, pattern_pair):
        pairs = {}
        hklp1, hklp2 = pattern_pair
        for hkl_tuple in self.hkl_dict:
            if not _match_pattern(hkl_tuple, hklp1):
                continue
            pair_hkl_tuple = _generate_hkl_by_pattern(hkl_tuple, hklp2)
            if pair_hkl_tuple in self.hkl_dict:
                pairs[hkl_tuple] = pair_hkl_tuple
        return pairs

    def check_equal_pairs(self, pairs, conf_level):
        result = []
        dup_check = set()
        for k, v in pairs.items():
            if (v, k) in dup_check:  # 已经检验过
                continue
            dup_check.add((k, v))
            int1, sigma1, phase1 = self.hkl_dict[k]
            int2, sigma2, phase2 = self.hkl_dict[v]
            t_value = abs(int1 - int2) / pow((sigma1 ** 2 + sigma2 ** 2) / 2, 0.5)
            if t_value > conf_level:
                result.append({'k': k, 'v': v, 't_value': t_value,
                               'k_int': self.hkl_dict[k], 'v_int': self.hkl_dict[v]})
        return result
