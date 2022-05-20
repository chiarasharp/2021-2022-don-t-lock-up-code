from src.OC.manage_csv_files import main as manage_csv_files
from src.DOAJ.create_json_dois import main as create_json_dois
from src.udf.final_merge import final_merge
from src.DOAJ.set_dois import main as set_dois
import pickle
import json





if __name__ == "__main__":


    '''1.------------DOAJ------------'''

    path_to_DOAJ_zip = "./data/imported/doaj_journal_data_2022-05-07.tar.gz"

    create_json_dois(path_to_DOAJ_zip)

    path_to_dois_file = "data/queried/DOAJ/doi.json"

    set_dois(path_to_dois_file)

    '''2.------------OC part------------'''

    path_zip_file = "E:/6741422"
    path_output_open_cit_json = "E:/6741422/data"
    path_output_general_dict = "./data/queried/OC"
    with open('./data/queried/DOAJ/doi_articles_journals.pickle', 'rb') as pickle_file:
        data_json = pickle.load(pickle_file)

        manage_csv_files(data_json, path_zip_file, path_output_open_cit_json, path_output_general_dict)


    '''3.------------Merge part------------'''

    all_doi_path = "./data/queried/DOAJ/doi.json"
    general_count_dict = "./data/queried/OC/general_count_dict_second_version.json"

    all_doi = json.load(open(all_doi_path, encoding="utf-8"))
    general_count_dict = json.load(open(general_count_dict))

    data = final_merge(all_doi, general_count_dict)

    with open('data/doi_with_count_second_version.json', 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


