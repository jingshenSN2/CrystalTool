import pandas as pd


def read_hkl(hkl_file):
    df = pd.read_table(hkl_file, sep='\\s+', header=None, names=['h', 'k', 'l', 'Int', 'sInt', 'phase'])
    return df


def to_hkl(df, hkl_file_name):
    df.to_csv(hkl_file_name, sep='\t', header=None, index=False)
