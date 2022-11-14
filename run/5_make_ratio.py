from src.OC import csv_manager
import pandas as pd
import os
import json
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

    path_to_normal_json = os.path.join('..', dict_variable['output_directory'], 'OC', 'group_by_year', 'normal.json')
    path_to_by_journal_json = os.path.join('..', dict_variable['output_directory'], 'OC', 'group_by_year',
                                           'by_journal.json')

    '''
    |--------------------------------------------------------------------------
    | LOAD
    |--------------------------------------------------------------------------
    '''
    with open(path_to_normal_json, 'r', encoding='utf-8') as jsonfile:
        normal_json = json.load(jsonfile)

    with open(path_to_by_journal_json, 'r', encoding='utf-8') as jsonfile:
        by_journal_json = json.load(jsonfile)

    '''
    |--------------------------------------------------------------------------
    | EXECUTION
    |--------------------------------------------------------------------------
    '''
    print('start adding ratio to the result of previous step...')

    # normal (only year, no journal)

    normal_json = csv_manager.make_ratio(normal_json)

    # by_journal (both year and journal)

    by_journal_json = csv_manager.make_ratio_journal(by_journal_json)

    '''
    |--------------------------------------------------------------------------
    | SAVE
    |--------------------------------------------------------------------------
    '''

    with open(path_to_normal_json, "w") as outfile:
        json.dump(normal_json, outfile)

    with open(path_to_by_journal_json, "w") as outfile:
        json.dump(by_journal_json, outfile)
