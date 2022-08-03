import os
import pandas as pd
import numpy as np
from glob import glob

def group_cit_by_years(path_to_cit_folder, output_path_cit_years_json, output_path_date_null_json, output_path_date_wrong_json):

    # getting the json files with the citations
    all_files = glob(os.path.join(path_to_cit_folder, "*.json"))
    ind_df = (pd.read_json(f) for f in all_files)

    # converting them in a pandas dataframe
    df = pd.concat(ind_df, ignore_index=True)

    print("concatenation done. number of citations: "+ str(len(df))+ ".")

    # adding the singular year column
    df['year'] = pd.DatetimeIndex(df['creation']).year
    
    # getting the citations with errors in dates 
    df2 = df[(df['year'].isnull())] # null dates
    df3 = df[(df['year'] > 2024)] # wrong dates

    # dump them in files
    df2.to_json(output_path_date_null_json, orient="records")
    df3.to_json(output_path_date_wrong_json, orient="records")

    print("number of citations with null dates: " + str(len(df2)) + ". citations with null dates file created.")
    print("number of citations with wrong dates: " + str(len(df3)) + ". citations with wrong dates file created.")

    # grouping the citations by year and then counting
    df['citation_count'] = df.groupby('year')['year'].transform('count')
    df = df[['year', 'citation_count']].reset_index(drop=True).convert_dtypes().drop_duplicates()
    df = df.dropna().astype({"citation_count":"int","year":"int"}).reset_index(drop=True)
    df = df.sort_values(by=['year']).reset_index(drop=True)

    # getting just the rows without errors in the dates
    df = df[df['year'] <= 2024].dropna().reset_index(drop=True)

    print("grouping and counting done.")

    # dumping in a json
    df.to_json(output_path_cit_years_json, orient="records")



def group_fromto_DOAJ_cit_by_years(path_to_fromto_DOAJ_cit_folder, path_cit_years_json, output_path_date_null_json, output_path_date_wrong_json):

    # getting the json files with the citations from and to DOAJ
    all_files = glob(os.path.join(path_to_fromto_DOAJ_cit_folder, "*.json"))
    ind_df = (pd.read_json(f) for f in all_files)

    # converting them in a pandas dataframe
    df = pd.concat(ind_df, ignore_index=True)

    print("concatenation done. number of citations: "+ str(len(df))+ ".")

    # adding the singular year column
    df['year'] = pd.DatetimeIndex(df['creation']).year

    # getting the citations with errors in dates 
    df2 = df[(df['year'].isnull())] # null dates
    df3 = df[(df['year'] > 2024)] # wrong dates

    # dump them in files
    df2.to_json(output_path_date_null_json, orient="records")
    df3.to_json(output_path_date_wrong_json, orient="records")

    print("number of citations to and from DOAJ with null dates: " + str(len(df2)) + ". citations to and from DOAJ with null dates file created.")
    print("number of citations to and from DOAJ with wrong dates: " + str(len(df3)) + ". citations to and from DOAJ with wrong dates file created.")

    # grouping the citations by year and then counting
    df['cit_count_tofrom_DOAJ'] = df.groupby('year')['year'].transform('count')
    df = df[['year', 'cit_count_tofrom_DOAJ']].reset_index(drop=True).convert_dtypes().drop_duplicates()
    df = df.dropna().astype({"cit_count_tofrom_DOAJ":"int","year":"int"}).reset_index(drop=True)
    df = df.sort_values(by=['year']).reset_index(drop=True)

    # getting just the rows without errors in the dates
    df = df[df['year'] <= 2100].dropna().reset_index(drop=True)

    print("grouping and counting done.")

    # getting the general citations data
    df_gen_cit = pd.read_json(path_cit_years_json)

    # creating the new columns: from/to DOAJ citations count and the percentage of it
    df_merge = df_gen_cit.merge(df, how='left',on='year').replace(np.nan, 0).convert_dtypes()
    df_merge['cit_tofrom_DOAJ_pcent'] = ((df_merge['cit_count_tofrom_DOAJ'])*100)/(df_merge['citation_count'])

    # updating the json
    df.to_json(path_cit_years_json, orient="records")