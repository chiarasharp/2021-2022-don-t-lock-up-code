import time
import pandas as pd
import pickle
from src.OC.OC_filter import manage_csv_files
import os
from glob import glob
from tqdm import tqdm
import zipfile

pd.options.mode.chained_assignment = None

"""
|--------------------------------------------------------------------------
| DESCRIPTION
|--------------------------------------------------------------------------

REQUIRED SCRIPT: /

The script iterates all over the files filtered from OpenCitations on both columns cited and citing, containing the 
DOAJ journals. The script create two different folder (cited and citing), on the specified output path.

"""

if __name__ == "__main__":

    """
    |--------------------------------------------------------------------------
    | INPUT VARIABLE
    |--------------------------------------------------------------------------
    """

    path_zip_file = input(str("\nPath to zip OpenCitations\n\n > "))

    path_pickle_file = input(str("\nPath to pickle_file\n\n > "))

    path_output = input(str("\nPath for output files\n\n > "))

    print("\n")

    """
    |--------------------------------------------------------------------------
    | EXECUTION
    |--------------------------------------------------------------------------
    """

    # open pickle file from previous run: it contains all the Dois divided by journals
    with open(path_pickle_file, 'rb') as pickle_file:
        data_json = pickle.load(pickle_file)
    all_zips = glob(os.path.join(path_zip_file, "*.zip"))

    # iterate all over the list with zip files until it is empty
    while len(all_zips) != 0:
        dir_zip_name = all_zips.pop(0)
        print(f"starting with another zip dir: {dir_zip_name}")
        # extrac all files from zip dir in another dir
        with zipfile.ZipFile(dir_zip_name, 'r') as zip_ref:
            zip_ref.extractall("../data/prova")
        zip_ref.close()

        # take all files from the repository created above
        all_files = glob(os.path.join("../data/prova", "*.csv"))
        # iterate all over the CSV files
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

            # filter the CSV records which contain the DOAJ journals on cited column
            df_cited = manage_csv_files(data_json, df, "cited")
            df_cited.to_csv(path_output + f"/cited/{name_file}")

            # filter the CSV records which contain the DOAJ journals on citing column
            df_citing = manage_csv_files(data_json, df, "citing")
            df_citing.to_csv(path_output + f"/citing/{name_file}")

            # delete the csv file
            os.remove(csv)

        # completed the iteration over the zip repo, delete it
        os.remove(dir_zip_name)

        # take a rest
        print(f"taking 200 second of rest")
        time.sleep(30)
