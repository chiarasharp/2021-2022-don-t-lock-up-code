from src.OC.manage_csv_files import main as manage_csv_files
from src.DOAJ.create_json_dois import create_json_dois
from src.udf.final_merge import final_merge
from src.udf.group_open_cit import group_open_cit
from src.DOAJ.set_dois import main as set_dois
import pickle
import json


if __name__ == "__main__":


    '''1.------------DOAJ------------'''

    path_to_DOAJ_journ_zip = "./data/imported/doaj_journal_data_2022-05-07.tar.gz"
    path_to_DOAJ_art_zip = " " # to add where your dump is

    create_json_dois(path_to_DOAJ_journ_zip, path_to_DOAJ_art_zip)

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
    general_count_dict = "./data/queried/OC/general_count_dict.json"

    all_doi = json.load(open(all_doi_path, encoding="utf-8"))
    general_count_dict = json.load(open(general_count_dict))

    data = final_merge(all_doi, general_count_dict)



    with open('data/doi_with_count.json', 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False)


    '''4.------------Grouping and counting open cit part------------'''

    path_to_open_cit_folder = ".data/queried/OC/open_cit"
    output_path_open_cit_years_json = ".data/final_data/open_cit_in_years.json"
    output_path_open_cit_err_json = ".data/final_data/open_cit_w_date_err.json"
    group_open_cit(path_to_open_cit_folder, output_path_open_cit_years_json, output_path_open_cit_err_json)
