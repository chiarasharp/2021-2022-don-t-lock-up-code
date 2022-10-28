import os
import pandas as pd
import numpy as np
from glob import glob
from tqdm import tqdm
from datetime import datetime

def group_cit_by_years(path_to_cit_folder, output_path_cit_years_json, output_path_date_null_json,
                       output_path_date_wrong_json):
    # getting the json files with the citations
    all_files = glob(os.path.join(path_to_cit_folder, "*.json"))
    for json_file in tqdm(all_files):

        file_name = json_file.split("\\")[-1]
        df = pd.read_json(json_file)

        if len(df) == 0: continue

        # adding the singular year column
        df['year'] = pd.DatetimeIndex(df['creation']).year

        # getting the citations with errors in dates
        df2 = df[(df['year'].isnull())]  # null dates
        df3 = df[(df['year'] > 2024)]  # wrong dates

        # dump them in files
        if len(df2) != 0:
            df2.to_json(output_path_date_null_json + f"/{file_name}", orient="records")
        if len(df3) != 0:
            df3.to_json(output_path_date_wrong_json + f"/{file_name}", orient="records")

        # grouping the citations by year and then counting
        df['citation_count'] = df.groupby('year')['year'].transform('count')
        df = df[['year', 'citation_count']].reset_index(drop=True).convert_dtypes().drop_duplicates()
        df = df.dropna().astype({"citation_count": "int", "year": "int"}).reset_index(drop=True)
        df = df.sort_values(by=['year']).reset_index(drop=True)

        # getting just the rows without errors in the dates
        df = df[df['year'] <= 2024].dropna().reset_index(drop=True)

        # dumping in a json
        df.to_json(output_path_cit_years_json + f"/{file_name}", orient="records")


def group_cit_by_years_prova(path_to_cit_folder, output_path_cit_years_json, output_path_date_null_json,
                       output_path_date_wrong_json):
    # getting the json files with the citations
    all_files = glob(os.path.join(path_to_cit_folder, "*.csv"))
    for json_file in tqdm(all_files):

        file_name = json_file.split("\\")[-1]
        df = pd.read_csv(json_file)

        if len(df) == 0: continue

        # adding the singular year column
        df['year'] = pd.to_datetime(df['creation'], errors='coerce').dt.year

        # getting the citations with errors in dates
        df2 = df[(df['year'].isnull())]  # null dates
        df3 = df[(df['year'] > 2024)]  # wrong dates

        # dump them in files
        if len(df2) != 0:
            df2.to_json(output_path_date_null_json + f"/{file_name.replace('csv', 'json')}", orient="records")
        if len(df3) != 0:
            df3.to_json(output_path_date_wrong_json + f"/{file_name.replace('csv', 'json')}", orient="records")

        # grouping the citations by year and then counting
        df['citation_count'] = df.groupby('year')['year'].transform('count')
        df = df[['year', 'citation_count']].reset_index(drop=True).convert_dtypes().drop_duplicates()
        df = df.dropna().astype({"citation_count": "int"}).reset_index(drop=True)
        df = df.sort_values(by=['year']).reset_index(drop=True)

        # getting just the rows without errors in the dates
        df = df[df['year'] <= 2024].dropna().reset_index(drop=True)


        # dumping in a json
        df.to_json(output_path_cit_years_json + f"/{file_name.replace('csv', 'json')}", orient="records")


def concatenate_json_files(path_to_files_dir, output_path_json_file):
    # getting the json files with the citations
    all_files = glob(os.path.join(path_to_files_dir, "*.json"))

    ind_df = (pd.read_json(f) for f in all_files)

    # converting them in a pandas dataframe
    df = pd.concat(ind_df, ignore_index=True)

    df = df.groupby("year", as_index=False).sum()

    # dumping in a json
    df.to_json(output_path_json_file, orient="records")


def print_result(DOAJ_citingByYear, path_to_cit_null, path_to_cit_wrong, errors_folder):
    df = pd.read_json(DOAJ_citingByYear)

    print("Number of citations: " + str(sum(df.citation_count)) + ".")

    all_files = glob(os.path.join(path_to_cit_null, "*.json"))

    ind_df = (pd.read_json(f) for f in all_files)

    df = pd.concat(ind_df, ignore_index=True)

    df.to_json(errors_folder + f"/date_null.json", orient="records")

    print("Number of citations with null dates: " + str(len(df)) + ".")

    all_files = glob(os.path.join(path_to_cit_wrong, "*.json"))

    ind_df = (pd.read_json(f) for f in all_files)

    df = pd.concat(ind_df, ignore_index=True)

    df.to_json(errors_folder + f"/date_wrong.json", orient="records")

    print("Number of citations with wrong dates: " + str(len(df)) + ".")


def group_self_citation(path_to_cit_folder, output_path_cit_years_json, output_path_date_null_json,
                       output_path_date_wrong_json):
    # getting the json files with the citations from and to DOAJ
    all_files = glob(os.path.join(path_to_cit_folder, "*.json"))
    for json_file in tqdm(all_files):

        file_name = json_file.split("\\")[-1]
        df = pd.read_json(json_file)

        if len(df) == 0: continue

        df = df[df["citing"] == df["ref_from_to_DOAJ"]]

        # adding the singular year column
        df['year'] = pd.DatetimeIndex(df['creation']).year

        # getting the citations with errors in dates
        df2 = df[(df['year'].isnull())]  # null dates
        df3 = df[(df['year'] > 2024)]  # wrong dates

        # dump them in files
        df2.to_json(output_path_date_null_json + f"/{file_name}", orient="records")
        df3.to_json(output_path_date_wrong_json + f"/{file_name}", orient="records")

        # grouping the citations by year and then counting
        df["citation_count"] = df.groupby(['year', 'journal'])['journal'].transform("count")
        df = df[['year', 'citation_count', 'journal']].reset_index(drop=True).convert_dtypes().drop_duplicates()
        df = df.dropna().astype({"citation_count": "int", "year": "int", "journal": "string"}).reset_index(drop=True)
        df = df.sort_values(by=['year']).reset_index(drop=True)

        # getting just the rows without errors in the dates
        df = df[df['year'] <= 2024].dropna().reset_index(drop=True)

        # dumping in a json
        df.to_json(output_path_cit_years_json + f"/{file_name}", orient="records")


def concatenate_json_files_self(path_to_files_dir, output_path_json_file):
    # getting the json files with the citations
    all_files = glob(os.path.join(path_to_files_dir, "*.json"))

    ind_df = (pd.read_json(f) for f in all_files)

    # converting them in a pandas dataframe
    df = pd.concat(ind_df, ignore_index=True)

    df = df.groupby(["year", 'journal'], as_index=False).sum()

    # dumping in a json
    df.to_json(output_path_json_file, orient="records")


def group_fromto_DOAJ_cit_by_years(path_to_fromto_DOAJ_cit_folder, path_cit_years_json, output_path_date_null_json,
                                   output_path_date_wrong_json):
    # getting the json files with the citations from and to DOAJ
    all_files = glob(os.path.join(path_to_fromto_DOAJ_cit_folder, "*.json"))

    for json_file in tqdm(all_files):

        file_name = json_file.split("\\")[-1]

        df = pd.read_json(json_file)

        if len(df) == 0: continue

        # adding the singular year column
        df['year'] = pd.DatetimeIndex(df['creation']).year

        # getting the citations with errors in dates
        df2 = df[(df['year'].isnull())]  # null dates
        df3 = df[(df['year'] > 2024)]  # wrong dates

        # dump them in files
        if len(df2) > 0:
            df2.to_json(f"{output_path_date_null_json}/{file_name}", orient="records")
        if len(df3) > 0:
            df3.to_json(f"{output_path_date_wrong_json}/{file_name}", orient="records")

        # grouping the citations by year and then counting
        df['cit_count_tofrom_DOAJ'] = df.groupby('year')['year'].transform('count')
        df = df[['year', 'cit_count_tofrom_DOAJ']].reset_index(drop=True).convert_dtypes().drop_duplicates()
        df = df.dropna().astype({"cit_count_tofrom_DOAJ": "int", "year": "int"}).reset_index(drop=True)
        df = df.sort_values(by=['year']).reset_index(drop=True)

        # getting just the rows without errors in the dates
        df = df[df['year'] <= 2100].dropna().reset_index(drop=True)

        # # getting the general citations data
        # df_gen_cit = pd.read_json(path_cit_years_json)

        # creating the new columns: from/to DOAJ citations count and the percentage of it
        # df_merge = df_gen_cit.merge(df, how='left', on='year').replace(np.nan, 0).convert_dtypes()
        # df_merge['cit_tofrom_DOAJ_pcent'] = ((df_merge['cit_count_tofrom_DOAJ']) * 100) / (df_merge['citation_count'])

        # updating the json
        df.to_json(f"{path_cit_years_json}/{file_name}", orient="records")


def print_result_fromto(DOAJ_citingByYear, path_to_cit_null, path_to_cit_wrong, errors_folder):
    df = pd.read_json(DOAJ_citingByYear)

    print("Number of citations: " + str(sum(df.cit_count_tofrom_DOAJ)) + ".")

    all_files = glob(os.path.join(path_to_cit_null, "*.json"))

    ind_df = (pd.read_json(f) for f in all_files)

    df = pd.concat(ind_df, ignore_index=True)

    df.to_json(errors_folder + f"/date_null.json", orient="records")

    print("Number of citations with null dates: " + str(len(df)) + ".")

    all_files = glob(os.path.join(path_to_cit_wrong, "*.json"))

    ind_df = (pd.read_json(f) for f in all_files)

    df = pd.concat(ind_df, ignore_index=True)

    df.to_json(errors_folder + f"/date_wrong.json", orient="records")

    print("Number of citations with wrong dates: " + str(len(df)) + ".")