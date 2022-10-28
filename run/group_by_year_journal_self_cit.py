import os
import pandas as pd
import numpy as np
from glob import glob
from tqdm import tqdm
from datetime import datetime
import shutil
import time


def group_self_citation(path_to_cit_folder, output_path_cit_years_json, output_path_date_null_json,
                        output_path_date_wrong_json, name_column):
    # getting the json files with the citations from and to DOAJ
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
        df[f'{name_column}_count'] = df.groupby(['year', 'journal'])['journal'].transform("count")
        df = df[['year', f'{name_column}_count', 'journal']].reset_index(drop=True).convert_dtypes().drop_duplicates()
        df = df.dropna().astype({f'{name_column}_count': "int", "year": "int", "journal": "string"}).reset_index(
            drop=True)
        df = df.sort_values(by=['year']).reset_index(drop=True)

        # getting just the rows without errors in the dates
        df = df[df['year'] <= 2024].dropna().reset_index(drop=True)

        # dumping in a json
        df.to_json(output_path_cit_years_json + f"/{file_name.replace('csv', 'json')}", orient="records")


def concatenate_json_files_self(path_to_files_dir, output_path_json_file):
    print(path_to_files_dir)
    # getting the json files with the citations
    time.sleep(2)
    all_files = glob(os.path.join(path_to_files_dir, "*.json"))

    ind_df = (pd.read_json(f) for f in all_files)

    # converting them in a pandas dataframe
    df = pd.concat(ind_df, ignore_index=True)

    df = df.groupby(["year", 'journal'], as_index=False).sum()

    # dumping in a json
    df.to_json(output_path_json_file, orient="records")


if __name__ == "__main__":

    path_to_dir = input(str("\nPath to input files\n\n > "))

    path_errors = input(str("\nPath for output errors\n\n > "))

    path_output = input(str("\nPath for output files\n\n > "))

    name_column = input(str("\nName of column to be analyzed\n\n > "))

    print("\n")

    if not os.path.exists(path_output + "/tmp"):
        os.mkdir(path_output + "/tmp")
    if not os.path.exists(path_errors + f"/date_null/self_cit" + "_journal"):
        os.mkdir(path_errors + f"/date_null/self_cit" + "_journal")
    if not os.path.exists(path_errors + f"/date_wrong/self_cit" + "_journal"):
        os.mkdir(path_errors + f"/date_wrong/self_cit" + "_journal")

    group_self_citation(path_to_dir, path_output + "/tmp", path_errors + f"/date_null/self_cit" + "_journal",
                        path_errors + f"/date_wrong/self_cit" + "_journal", name_column)

    if not os.path.exists(path_output + "/by_journal"):
        os.mkdir(path_output + "/by_journal")

    concatenate_json_files_self(path_output + "/tmp", path_output + "/by_journal" + f"/{name_column}.json")

    shutil.rmtree(path_output + "/tmp", ignore_errors=True)
