import pandas as pd
import os
import json
from src.udf import read_env
import pickle

pd.options.mode.chained_assignment = None

'''
|--------------------------------------------------------------------------
| DESCRIPTION
|--------------------------------------------------------------------------

REQUIRED SCRIPT: /

'''

if __name__ == '__main__':
    '''
    |--------------------------------------------------------------------------
    | INPUT VARIABLES
    |--------------------------------------------------------------------------
    '''
    dict_variable = read_env.take_env_variables('../.env')

    path_to_DOAJ = os.path.join('..', dict_variable['output_directory'], 'DOAJ')
    path_to_DOAJ_metrics = os.path.join('..', dict_variable['output_directory'], 'DOAJ', 'metrics.json')
    path_to_DOAJ_total_dois = os.path.join('..', dict_variable['output_directory'], 'DOAJ',
                                           'doi_articles_journals.pickle')
    path_to_output_file = os.path.join('..', dict_variable['output_directory'], 'DOAJ', 'DOAJ_metrics')

    '''
    |--------------------------------------------------------------------------
    | LOAD
    |--------------------------------------------------------------------------
    '''

    with open(os.path.join('..', 'queried', 'DOAJ', 'doi.json'), 'r', encoding='utf-8') as json_file:
        total_with_repeated_dois = json.load(json_file)

    with open(path_to_DOAJ_metrics, 'r', encoding='utf-8') as jsonfile:
        DOAJ_metrics = json.load(jsonfile)

    with open(path_to_DOAJ_total_dois, 'rb') as pickle_file:
        total_no_repeated_dois = pickle.load(pickle_file)

    list_doi_from_dois_json = list()
    list_repeated_dois_count = dict()
    list_no_repeated_dois = total_no_repeated_dois.keys()
    '''
    |--------------------------------------------------------------------------
    | EXECUTION
    |--------------------------------------------------------------------------
    '''

    DOAJ_metrics['total_dois_used'] = len(total_no_repeated_dois)

    for article in total_with_repeated_dois.values():
        list_doi_from_dois_json += article['dois']

    for doi in list_doi_from_dois_json:
        if doi in list_no_repeated_dois and doi not in list_repeated_dois_count:
            list_repeated_dois_count[doi] = 0
        elif list_repeated_dois_count[doi] == 0:
            list_repeated_dois_count[doi] += 1
        else:
            pass

    DOAJ_metrics['total_dois_repeated'] = sum(list_repeated_dois_count.values())
    DOAJ_metrics['total_dois_accepted'] = len(list_doi_from_dois_json)

    print(DOAJ_metrics)

    '''
    |--------------------------------------------------------------------------
    | SAVE
    |--------------------------------------------------------------------------
    '''

    with open(path_to_output_file + '.json', "w") as outfile:
        json.dump(DOAJ_metrics, outfile)
