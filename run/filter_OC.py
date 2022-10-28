import time
import pandas as pd
import pickle
from src.OC.OC_filter import manage_csv_files
import os
from glob import glob
from tqdm import tqdm
import zipfile
pd.options.mode.chained_assignment = None  # default='warn'

if __name__ == "__main__":

    path_zip_file = input(str("\nPath to zip OpenCitations\n\n > "))

    path_pickle_file = input(str("\nPath to pickle_file\n\n > "))

    path_output = input(str("\nPath for output files\n\n > "))

    print("\n")

    with open(path_pickle_file, 'rb') as pickle_file:
        data_json = pickle.load(pickle_file)
    all_zips = glob(os.path.join(path_zip_file, "*.zip"))

    while len(all_zips) != 0:
        dir_zip_name = all_zips.pop(0)
        print(f"starting with another zip dir: {dir_zip_name}")
        with zipfile.ZipFile(dir_zip_name, 'r') as zip_ref:
            zip_ref.extractall("../data/prova")
        zip_ref.close()

        all_files = glob(os.path.join("../data/prova", "*.csv"))
        for csv in tqdm(all_files):
            name_file = csv.split("\\")[-1]

            # convert the read file to a Pandas dataframe
            df = pd.read_csv(csv,
                             dtype={'timespan': str,
                                    'journal_sc': str,
                                    'author_sc': str,
                                    'creation': str,
                                    'cited': str,
                                    "citing": str,
                                    "oci": str})

            df_cited = manage_csv_files(data_json, df, "cited")
            df_cited.to_csv(path_output + f"/cited/{name_file}")

            df_citing = manage_csv_files(data_json, df, "citing")
            df_citing.to_csv(path_output + f"/citing/{name_file}")

            os.remove(csv)
        os.remove(dir_zip_name)
        print(f"taking 200 second of rest")
        time.sleep(30)
