import json
import zipfile
from io import BytesIO
import pandas as pd
from os import listdir
from tqdm import tqdm
import pickle
import time


def add_citation_ratio(data):
    """
    take input data

    iterate all over the journals

    take citation and cited fields

    make ratio

    update dict with the result



    :param data: general_count_dict
    :return: dict
    """


def add_openCit_ratio(data):
    """
    take input data

    iterate all over the journals

    take citation, cited and open fields

    make ratio between citation and open, and cited and open

    update dict with the result



    :param data: general_count_dict
    :return: dict
    """


def collect_citation(data_json, input_path_zip_file):
    """
    take input data

    iterate all over the journals

    take all citation and cited with years and month

    make the sum of all citation and cited divided by year

    update dict with the result


    :param data: general_count_dict
    :return: dict
    """
    list_existing_file = [f for f in listdir("../../data/queried/OC/DOAJ_citing")]
    list_zip_file = [f for f in listdir(input_path_zip_file) if "gitignore" not in f]
    print(list_zip_file)
    # iterate all over zip file
    for zip_file in list_zip_file:
        with zipfile.ZipFile(f"{input_path_zip_file}/{zip_file}", "r") as zfile:

            # iterate all over CSV inside zip file
            general_df = None
            for i, name_file in enumerate(zfile.namelist()):
                print(name_file + "--->", end=" ")

                if name_file.replace('.csv', '.json').replace(':', '_') in list_existing_file:
                    print("skipped")
                    continue
                # print(f"---> {name_file}\n")
                # check if the file is listed in the latter files
                print("start working --->", end=" ")
                # convert the file from bytes
                zfiledata = BytesIO(zfile.read(name_file))

                # convert the readed file to a Pandas dataframe
                df = pd.read_csv(zfiledata)

                df = df[df["citing"].isin(data_json.keys())]

                if len(df) == 0:
                    print("skipped")
                    continue

                result = df.to_dict(orient="records")
                json_object = json.dumps(result)
                with open(
                        f"../../data/queried/OC/DOAJ_citing/{name_file.replace('.csv', '').replace(':', '_')}.json",
                        "w") as outfile:
                    outfile.write(json_object)
                    outfile.close()
                print("finished")
                zfiledata.close()



def collect_self_citation():
    pass


if __name__ == "__main__":
    path_zip_file = "../../data/imported/6741422"
    with open('../../data/queried/DOAJ/doi_articles_journals.pickle', 'rb') as pickle_file:
        data_json = pickle.load(pickle_file)

    collect_citation(data_json, path_zip_file)
