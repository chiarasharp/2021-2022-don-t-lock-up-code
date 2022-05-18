from src.create_json_dois import main as doaj_json
from src.manage_csv_files import main as csv_files
from src.set_dois import main as take_all_dois
from src.reorganize_json import main as reorganize_json, reorganize_json_doi_DOAJ
from src.set_dois import main as set_dois
import os
import pickle
import pandas as pd
import json


if __name__ == "__main__":

    # for path in ["./data/queried/DOAJ/articles_without_doi.json",
    #              "./data/queried/DOAJ/doi.json"]:
    #
    #     if not os.path.exists(path):
    #         doaj_json()
    #
    # if not os.path.exists("./data/queried/DOAJ/doi_articles.pickle"):
    #     take_all_dois()
    #
    #
    # with open('./data/queried/DOAJ/doi_articles.pickle', 'rb') as pickle_file:
    #     data_json = pickle.load(pickle_file)
    #
    #
    # csv_files(data_json)

    import json






with open('./data/queried/DOAJ/doi_articles_journals.pickle', 'rb') as pickle_file:
    data_json = pickle.load(pickle_file)

csv_files(data_json)



