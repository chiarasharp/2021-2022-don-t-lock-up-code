from src.OC import csv_manager
import pandas as pd
import os
from tqdm import tqdm
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

    path_to_csv = os.path.join('..', dict_variable['output_directory'], 'OC', 'filtered')

    path_to_output = os.path.join('..', dict_variable['output_directory'], 'OC', 'group_by_year')

    '''
    |--------------------------------------------------------------------------
    | LOAD
    |--------------------------------------------------------------------------
    '''

    # take all csv filtered by OpenCitations
    all_csv = os.listdir(os.path.join(path_to_csv))

    all_csv_already_groupBy = os.listdir(os.path.join(path_to_output, 'normal'))

    all_csv = list(set(all_csv).difference(set(all_csv_already_groupBy)))

    all_csv = [os.path.join(path_to_csv, path) for path in all_csv]

    '''
    |--------------------------------------------------------------------------
    | EXECUTION
    |--------------------------------------------------------------------------
    '''
    print('start with group by operation of filtered repository')
    for csv in tqdm(all_csv):
        name_file = csv.split('\\')[-1]

        df = pd.read_csv(csv, dtype={
            'oci': str,
            'creation': str,
            'citing': str,
            'citing_journal': str,
            'isDOAJ_citing': str,
            'cited': str,
            'cited_journal': str,
            'isDOAJ_cited': str
        })

        df = csv_manager.add_isDOAJ(df)

        df = csv_manager.add_year(df, 'creation')

        df, df_null, df_wrong = csv_manager.save_errors(df, name_file)

        df_normal = csv_manager.groupBy_year(df)

        df_by_journal = csv_manager.groupBy_year_and_journal(df)

        '''
        |--------------------------------------------------------------------------
        | SAVE
        |--------------------------------------------------------------------------
        '''

        df_normal.to_csv(os.path.join(path_to_output, 'normal', name_file))

        df_by_journal.to_csv(os.path.join(path_to_output, 'by_journal', name_file))

        df_null.to_csv(os.path.join('..', dict_variable['output_directory'], 'errors', 'null_dates', name_file))

        df_wrong.to_csv(os.path.join('..', dict_variable['output_directory'], 'errors', 'wrong_dates', name_file))
