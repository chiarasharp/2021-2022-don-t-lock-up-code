from src.OC import csv_manager
import pandas as pd
import os
from glob import glob
from src.udf import read_env

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

    path_to_I_O_repo = os.path.join('..', dict_variable['output_directory'], 'OC', 'group_by_year')
    path_to_journals_description_file = os.path.join('..', dict_variable['output_directory'], 'DOAJ', 'doi.json')
    all_csv_normal = glob(os.path.join(path_to_I_O_repo, 'normal', '*.csv'))
    all_csv_byJournal = glob(os.path.join(path_to_I_O_repo, 'by_journal', '*.csv'))
    all_csv_null_dates = glob(os.path.join('..', dict_variable['output_directory'], 'errors', 'null_dates', '*.csv'))
    all_csv_wrong_dates = glob(os.path.join('..', dict_variable['output_directory'], 'errors', 'wrong_dates', '*.csv'))
    all_csv_null_citing = glob(os.path.join('..', dict_variable['output_directory'], 'errors', 'null_citing', '*.csv'))
    all_csv_null_cited = glob(os.path.join('..', dict_variable['output_directory'], 'errors', 'null_cited', '*.csv'))
    all_articles_without_dois = os.path.join('..', dict_variable['output_directory'], 'DOAJ',
                                             'articles_without_doi.json')

    '''
    |--------------------------------------------------------------------------
    | LOAD
    |--------------------------------------------------------------------------
    '''

    df_journals_description = pd.read_json(path_to_journals_description_file, orient="index")

    '''
    |--------------------------------------------------------------------------
    | EXECUTION
    |--------------------------------------------------------------------------
    '''
    print('\n> start concatenating all results of the previous step...')

    # concat normal csv
    df_normal = csv_manager.concat_csv_normal(all_csv_normal)
    # concat by_journal csv
    df_by_journal = csv_manager.concat_csv_journal(all_csv_byJournal)

    print('\n> add other metadata about journals extracted form DOAJ')
    # add journal information
    df_by_journal = csv_manager.add_to_journals_DOAJ_descriptions(df_by_journal, df_journals_description)

    # concat errors csv
    df_null_dates = csv_manager.concat_csv(all_csv_null_dates)

    df_wrong_dates = csv_manager.concat_csv(all_csv_wrong_dates)

    df_null_citing = csv_manager.concat_csv(all_csv_null_citing)

    df_null_cited = csv_manager.concat_csv(all_csv_null_cited)

    df_articles_without_dois = pd.read_json(all_articles_without_dois, orient='records')

    df_errors = pd.DataFrame({'type_of_error': ['null_dates', 'wrong_dates',
                                                'null_citing', 'null_cited', 'articles_without_dois'],
                              'count': [sum(df_null_dates['oci']), sum(df_wrong_dates['oci']),
                                        len(df_null_citing), len(df_null_cited),
                                        len(df_articles_without_dois)]})

    '''
    |--------------------------------------------------------------------------
    | SAVE
    |--------------------------------------------------------------------------
    '''

    df_normal = df_normal.to_json(os.path.join(path_to_I_O_repo, 'normal.json'), orient="records")

    df_by_journal.to_json(os.path.join(path_to_I_O_repo, 'by_journal.json'), orient="records")

    df_null_dates.to_json(os.path.join('..', dict_variable['output_directory'], 'errors', 'null.json'), orient="records")

    df_wrong_dates.to_json(os.path.join('..', dict_variable['output_directory'], 'errors', 'wrong.json'), orient="records")

    df_null_cited.to_json(os.path.join('..', dict_variable['output_directory'], 'errors', 'null_cited.json'), orient="records")

    df_null_citing.to_json(os.path.join('..', dict_variable['output_directory'], 'errors', 'null_citing.json'), orient="records")

    df_errors.to_json(os.path.join('..', dict_variable['output_directory'], 'errors', 'errors.json'), orient="records")
