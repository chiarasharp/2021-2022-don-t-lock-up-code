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
    path_to_final_output_repo = os.path.join('..', dict_variable['output_directory'], 'final_output')


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
    print('\n start adding some useful metrics...')
    DOAJ_metrics['total_dois_used'] = {'value': len(total_no_repeated_dois), 'description':
                                        'All dois (with no repetition) which are used for the adding journal operation'
                                        'in the second pipeline step'}

    for article in total_with_repeated_dois.values():
        list_doi_from_dois_json += article['dois']

    for doi in list_doi_from_dois_json:
        if doi in list_no_repeated_dois and doi not in list_repeated_dois_count:
            list_repeated_dois_count[doi] = 0
        elif list_repeated_dois_count[doi] == 0:
            list_repeated_dois_count[doi] += 1
        else:
            pass

    DOAJ_metrics["j_with_dois"] = {'value': DOAJ_metrics["j_with_dois"], 'description': 'All journal which have '
                                                                                        'listed at least one doi'}
    DOAJ_metrics['total_dois_repeated'] = {'value': sum(list_repeated_dois_count.values()), 'description':
                                           'All dois which are repeated inside the same or in another journal'}
    DOAJ_metrics['total_dois_accepted'] = {'value': len(list_doi_from_dois_json), 'description':
                                           'All articles (with repetition) which have both a defined journal and a '
                                           'defined doi'}
    DOAJ_metrics["n_articles_no_dois"] = {'value': DOAJ_metrics["n_articles_no_dois"], 'description':
                                            'All articles which have no defined dois'}
    DOAJ_metrics["n_articles_processed"] = {'value': DOAJ_metrics["n_articles_processed"], 'description':
                                            'All articles which are been processed during the first pipeline step'}

    '''
    |--------------------------------------------------------------------------
    | SAVE
    |--------------------------------------------------------------------------
    '''

    with open(os.path.join(path_to_final_output_repo, 'DOAJ_metrics.json'), "w") as outfile:
        json.dump(DOAJ_metrics, outfile)
