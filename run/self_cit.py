import pandas as pd
import os
from tqdm import tqdm
import pickle
from glob import glob

pd.options.mode.chained_assignment = None  # default='warn'

if __name__ == "__main__":

    path_zip_file = input(str("\nPath to citing or cited files\n\n > "))

    path_output = input(str("\nPath for output files\n\n > "))

    print("\n")

    all_zips = os.listdir(path_zip_file + f"/cit_from_to_DOAJ")
    for name_zip in tqdm(all_zips):

        df_cit_from_to_DOAJ = pd.read_csv(path_zip_file + f"/cit_from_to_DOAJ/{name_zip}",
                                          dtype={'timespan': str,
                                                 'journal_sc': str,
                                                 'author_sc': str,
                                                 'creation': str,
                                                 'cit_from_to_DOAJ': str,
                                                 "oci": str,
                                                 "journal": str}
                                          )

        df_ref_from_to_DOAJ = pd.read_csv(path_zip_file + f"/ref_from_to_DOAJ/{name_zip}", on_bad_lines='skip',
                                          dtype={'timespan': str,
                                                 'journal_sc': str,
                                                 'author_sc': str,
                                                 'creation': str,
                                                 'ref_from_to_DOAJ': str,
                                                 "oci": str,
                                                 "journal": str})

        df_result = pd.merge(df_cit_from_to_DOAJ[["creation", "journal"]].reset_index(drop=True),
                             df_ref_from_to_DOAJ[["creation", "journal"]].reset_index(drop=True),
                             on=["creation", "journal"], how="inner").drop_duplicates()

        print(len(df_cit_from_to_DOAJ), len(df_ref_from_to_DOAJ), len(df_result))
        if len(df_result) == 0: continue

        if not os.path.exists(path_output + "/self_cit"):
            os.mkdir(path_output + "/self_cit")

        df_result.to_csv(f"{path_output}/self_cit/{name_zip}")
