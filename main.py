from src.OC.manage_csv_files import main as manage_csv_files
from src.DOAJ.create_json_dois import create_json_dois
from src.udf.final_merge import final_merge
from udf.group_cit_by_years import group_fromto_DOAJ_cit_by_years, group_cit_by_years
from udf.manage_errors import manage_errors
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

    #TODO CHOOSE AND CORRECT THE PATHS

    path_to_cit_folder = "" 
    output_path_cit_years_json = ""
    output_path_date_null_gen_json = ".data/errors/null_date_gen_cit.json" #do not change this path
    output_path_date_wrong_gen_json = ".data/errors/wrong_date_gen_cit.json" #do not change this path
    group_cit_by_years(path_to_cit_folder, output_path_cit_years_json, output_path_date_null_gen_json, output_path_date_wrong_gen_json)

    path_to_fromto_DOAJ_cit_folder = ""
    path_cit_years_json = ""
    output_path_date_null_tofromDOAJ_json = ".data/errors/null_date_tofromDOAJ_cit.json" #do not change this path
    output_path_date_wrong_tofromDOAJ_json = ".data/errors/wrong_date_tofromDOAJ_cit.json" #do not change this path
    group_fromto_DOAJ_cit_by_years(path_to_fromto_DOAJ_cit_folder, output_path_cit_years_json, output_path_date_null_tofromDOAJ_json, output_path_date_wrong_tofromDOAJ_json)

    path_to_err_folder = ".data/errors" #do not change this path
    output_err_categories_json = ".data/final_data/errors.json"
    manage_errors(path_to_err_folder, output_err_categories_json)