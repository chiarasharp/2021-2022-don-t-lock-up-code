from glob import glob
import os
import pandas as pd


def concat_csv(all_csv):
    all_df = (pd.read_csv(f) for f in all_csv)

    df = pd.concat(all_df, ignore_index=True)

    return df