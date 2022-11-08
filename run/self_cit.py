import pandas as pd
import os
from tqdm import tqdm

pd.options.mode.chained_assignment = None  # default='warn'

"""
|--------------------------------------------------------------------------
| DESCRIPTION
|--------------------------------------------------------------------------

REQUIRED SCRIPT: filter_OC

The script iterates all over the files filtered from OpenCitations on both columns cited and citing, containing the 
DOAJ journals. The script finds the common records on both read dataframe in order to understand which journal cite itself.

"""

if __name__ == "__main__":

    """
    |--------------------------------------------------------------------------
    | INPUT VARIABLE
    |--------------------------------------------------------------------------
    """
    path_zip_file = input(str("\nPath to citing or cited files\n\n > "))

    path_output = input(str("\nPath for output files\n\n > "))

    print("\n")

    """
    |--------------------------------------------------------------------------
    | EXECUTION
    |--------------------------------------------------------------------------
    """

    # read all files from one of two repository inside citing_cited repository
    # (files filtered with jounrnal from DOAJ on both columns)
    all_zips = os.listdir(path_zip_file + f"/cit_from_to_DOAJ")
    for name_zip in tqdm(all_zips):

        # Read all files from citing directory
        df_cit_from_to_DOAJ = pd.read_csv(path_zip_file + f"/cit_from_to_DOAJ/{name_zip}",
                                          dtype={'timespan': str,
                                                 'journal_sc': str,
                                                 'author_sc': str,
                                                 'creation': str,
                                                 'cit_from_to_DOAJ': str,
                                                 "oci": str,
                                                 "journal": str}
                                          )
        # Read all files from cited directory
        df_ref_from_to_DOAJ = pd.read_csv(path_zip_file + f"/ref_from_to_DOAJ/{name_zip}", on_bad_lines='skip',
                                          dtype={'timespan': str,
                                                 'journal_sc': str,
                                                 'author_sc': str,
                                                 'creation': str,
                                                 'ref_from_to_DOAJ': str,
                                                 "oci": str,
                                                 "journal": str})
        # merge the two read dataframe in a single one
        df_result = pd.merge(df_cit_from_to_DOAJ[["creation", "journal"]].reset_index(drop=True),
                             df_ref_from_to_DOAJ[["creation", "journal"]].reset_index(drop=True),
                             on=["creation", "journal"], how="inner").drop_duplicates()

        if len(df_result) == 0: continue

        # if not exist: create the final repo inside the repo for the output specified above
        if not os.path.exists(path_output + "/self_cit"):
            os.mkdir(path_output + "/self_cit")

        # save
        df_result.to_csv(f"{path_output}/self_cit/{name_zip}")
