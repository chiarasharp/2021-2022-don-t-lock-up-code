from src.udf import concat_udf
import pandas as pd
import os
from glob import glob

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

    path_to_I_O_repo = os.path.join('..', os.getenv('output_directory'), 'OC', 'group_by_year')

    '''
    |--------------------------------------------------------------------------
    | LOAD
    |--------------------------------------------------------------------------
    '''

    # take all name files from one of two input directory
    all_csv_normal = glob(os.path.join(path_to_I_O_repo, 'normal', '*.csv'))
    all_csv_byJournal = glob(os.path.join(path_to_I_O_repo, 'by_journal', '*.csv'))
    all_csv_null = glob(os.path.join('..', os.getenv('output_directory'), 'errors', 'null', '*.csv'))
    all_csv_wrong = glob(os.path.join('..', os.getenv('output_directory'), 'errors', 'wrong', '*.csv'))

    '''
    |--------------------------------------------------------------------------
    | EXECUTION
    |--------------------------------------------------------------------------
    '''

    df_normal = concat_udf.concat_csv(all_csv_normal)

    df_normal.to_json(os.path.join(path_to_I_O_repo, 'normal.json'), orient="records")

    df_by_journal = concat_udf.concat_csv(all_csv_byJournal)

    df_by_journal.to_json(os.path.join(path_to_I_O_repo, 'by_journal.json'), orient="records")

    # add journal information

    # manage_errors
    df_normal = concat_udf.concat_csv(all_csv_null)

    df_normal.to_json(os.path.join('..', os.getenv('output_directory'), 'errors', 'null.json'), orient="records")

    df_normal = concat_udf.concat_csv(all_csv_wrong)

    df_normal.to_json(os.path.join('..', os.getenv('output_directory'), 'errors', 'wrong.json'), orient="records")



