import os
import pandas as pd
from glob import glob


def concatenate_json_files(path_to_files_dir, output_path_json_file):
    # getting the json files with the citations
    all_files = glob(os.path.join(path_to_files_dir, "*.json"))

    ind_df = (pd.read_json(f) for f in all_files)

    # converting them in a pandas dataframe
    df = pd.concat(ind_df, ignore_index=True)

    df = df.groupby("year", as_index=False).sum()

    df = df.dropna().astype({"year": "int", "citing_count": "int", "cited_count": "int"}).reset_index(drop=True)

    df["ratio"] = df["citing_count"] / df["cited_count"]

    df["ratio"] = df["ratio"].round(3)

    # dumping in a json
    df.to_json(output_path_json_file + '/general_count_dict.json', orient="records")


if __name__ == "__main__":
    path_to_dir = input(str("\nPath to input files\n\n > "))

    path_output = input(str("\nPath for output files\n\n > "))

    concatenate_json_files(path_to_dir, path_output)