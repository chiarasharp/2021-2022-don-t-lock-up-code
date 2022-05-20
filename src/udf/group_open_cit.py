import os
import pandas as pd
from glob import glob

def main():
    # getting the json files with the citations
    all_files = glob(os.path.join("data/queried/OC/opencit", "*.json"))
    ind_df = (pd.read_json(f) for f in all_files)

    # converting them in a pandas dataframe
    df = pd.concat(ind_df, ignore_index=True)

    # grouping by year and then counting
    df['year'] = pd.DatetimeIndex(df['creation']).year
    df['citation_count'] = df.groupby('year')['year'].transform('count')
    df = df[['citation_count', 'year']].reset_index(drop=True).convert_dtypes().drop_duplicates()
    df = df.dropna().astype({"citation_count":"int","year":"int"}).reset_index(drop=True)

    # dumping in a json
    df.to_json('open_cit_in_years.json', orient="records")