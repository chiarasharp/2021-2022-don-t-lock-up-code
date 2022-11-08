import os
import pandas as pd
from glob import glob
import numpy as np


def weird_division(n, m):
    return n / m if m else 0.0


def concatenate_json_files(path_to_files_dir, output_path_json_file):
    # getting the json files with the citations
    all_files = glob(os.path.join(path_to_files_dir, "*.json"))

    ind_df = (pd.read_json(f) for f in all_files)

    # converting them in a pandas dataframe
    df = pd.concat(ind_df, ignore_index=True)

    df = df.groupby(["year", "journal"], as_index=False).sum()

    df = df.dropna().astype({"year": "int",
                             "journal": "str",
                             "citing_count": "int",
                             "cited_count": "int",
                             "cit_from_to_DOAJ_count": "int",
                             "ref_from_to_DOAJ_count": "int"
                             }).reset_index(drop=True)

    df["citing_cited_ratio"] = df.apply(lambda row: weird_division(row['citing_count'], row['cited_count']), axis=1)

    df["citing_cited_ratio"] = df["citing_cited_ratio"].round(3)

    df["cit_from_to_DOAJ_pcent"] = df.apply(
        lambda row: weird_division(row['cit_from_to_DOAJ_count'], row['cited_count']), axis=1)

    df["cit_from_to_DOAJ_pcent"] = df["cit_from_to_DOAJ_pcent"].round(3)

    df["ref_from_to_DOAJ_pcent"] = df.apply(
        lambda row: weird_division(row['ref_from_to_DOAJ_count'], row['citing_count']), axis=1)

    df["ref_from_to_DOAJ_pcent"] = df["ref_from_to_DOAJ_pcent"].round(3)

    # dumping in a json
    df.to_json(output_path_json_file + '/general_count_dict.json', orient="records")


if __name__ == "__main__":
    path_to_dir = input(str("\nPath to input files\n\n > "))

    path_output = input(str("\nPath for output files\n\n > "))

    concatenate_json_files(path_to_dir, path_output)
