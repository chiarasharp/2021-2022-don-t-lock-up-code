import os
import pandas as pd
from glob import glob

def main():
    # getting the json files with the citations
    all_files = glob(os.path.join("data/queried/OC/open_cit", "*.json"))
    ind_df = (pd.read_json(f) for f in all_files)

    # converting them in a pandas dataframe
    df = pd.concat(ind_df, ignore_index=True)

    print("concatenation done. number of citations: "+ str(len(df))+ ".")

    # adding the singular year column
    df['year'] = pd.DatetimeIndex(df['creation']).year

    # getting the citations with errors in dates and putting them in a file 
    df2 = df[(df['year'] > 2024) | (df['year'].isnull())]
    df2.to_json('open_cit_w_date_err.json', orient="records")

    print("number of citations with errors: " + str(len(df2)) + ". citations with errors file created.")

    # gruping the citations by year and then counting
    df['citation_count'] = df.groupby('year')['year'].transform('count')
    df = df[['citation_count', 'year']].reset_index(drop=True).convert_dtypes().drop_duplicates()
    df = df.dropna().astype({"citation_count":"int","year":"int"}).reset_index(drop=True)
    df = df.sort_values(by=['year']).reset_index(drop=True)
    df = df[df['year'] <= 2100].dropna().reset_index(drop=True) # getting just the rows without errors in the dates

    print("grouping and counting done.")

    # dumping in a json
    df.to_json('open_cit_in_years.json', orient="records")

main()