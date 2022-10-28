import pandas as pd
import os
from tqdm import tqdm
import pickle
from glob import glob
pd.options.mode.chained_assignment = None  # default='warn'

if __name__ == "__main__":

    path_zip_file = input(str("\nPath to citing or cited files\n\n > "))

    path_output = input(str("\nPath for output files\n\n > "))

    path_pickle_file = input(str("\nPath to pickle_file\n\n > "))

    print("\n")

    with open(path_pickle_file, 'rb') as pickle_file:
        data_json = pickle.load(pickle_file)

    all_zips = os.listdir(path_zip_file + f"/citing")
    all_file_already_created = os.listdir(path_output)
    for name_zip in tqdm(all_zips):

        if name_zip in all_file_already_created: continue
        df_citing = pd.read_csv(path_zip_file + f"/citing/{name_zip}",
                                dtype={'timespan': str,
                                       'journal_sc': str,
                                       'author_sc': str,
                                       'creation': str,
                                       'cited': str,
                                       "citing": str,
                                       "oci": str,
                                       "journal": str}
                                )

        df_citing = df_citing.drop("journal", axis=1)

        df_cited = pd.read_csv(path_zip_file + f"/cited/{name_zip}", on_bad_lines='skip',
                               dtype={'timespan': str,
                                      'journal_sc': str,
                                      'author_sc': str,
                                      'creation': str,
                                      'cited': str,
                                      "citing": str,
                                      "oci": str,
                                      "journal": str})

        df_cited = df_cited.drop("journal", axis=1)

        df_result = pd.merge(df_cited, df_citing, how="inner") \
            .rename(columns={'cited': 'ref_from_to_DOAJ', 'citing': 'cit_from_to_DOAJ'})
        print(len(df_cited), len(df_citing), len(df_result))
        if len(df_result) == 0: continue

        df_ref_from_to_DOAJ = df_result[
            ['timespan', 'journal_sc', 'author_sc', 'creation', 'ref_from_to_DOAJ', "oci"]]. \
            reset_index(drop=True).convert_dtypes().drop_duplicates()

        df_ref_from_to_DOAJ["journal"] = df_ref_from_to_DOAJ["ref_from_to_DOAJ"].apply(lambda x: data_json[x])

        if not os.path.exists(path_output + "/ref_from_to_DOAJ"):
            os.mkdir(path_output + "/ref_from_to_DOAJ")

        df_ref_from_to_DOAJ.to_csv(f"{path_output}/ref_from_to_DOAJ/{name_zip}")

        df_cit_from_to_DOAJ = df_result[
            ['timespan', 'journal_sc', 'author_sc', 'creation', 'cit_from_to_DOAJ', "oci"]]. \
            reset_index(drop=True).convert_dtypes().drop_duplicates()

        df_cit_from_to_DOAJ["journal"] = df_cit_from_to_DOAJ["cit_from_to_DOAJ"].apply(lambda x: data_json[x])

        if not os.path.exists(path_output + "/cit_from_to_DOAJ"):
            os.mkdir(path_output + "/cit_from_to_DOAJ")

        df_cit_from_to_DOAJ.to_csv(f"{path_output}/cit_from_to_DOAJ/{name_zip}")
