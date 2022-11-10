from src.udf import groupBy_udf
import pandas as pd
import os
from glob import glob
from tqdm import tqdm

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

    path_to_csv = os.path.join('..', os.getenv('output_directory'), 'OC', 'filtered')

    path_to_output = os.path.join('..', os.getenv('output_directory'), 'OC', 'group_by_year')

    '''
    |--------------------------------------------------------------------------
    | LOAD
    |--------------------------------------------------------------------------
    '''

    # take all name files from one of two input directory
    all_csv = glob(os.path.join(path_to_csv, '*.csv'))

    '''
    |--------------------------------------------------------------------------
    | EXECUTION
    |--------------------------------------------------------------------------
    '''

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

        df = groupBy_udf.add_isDOAJ(df)

        df = groupBy_udf.add_year(df)

        df_null, df_wrong = groupBy_udf.discard_errors(df, name_file)

        df_null.to_csv(os.path.join('..', os.getenv('output_directory'), 'errors', 'null', name_file), index=False)

        df_wrong.to_csv(os.path.join('..', os.getenv('output_directory'), 'errors', 'wrong', name_file),  index=False)

        groupBy_udf.groupBy_year(df).to_csv(os.path.join(path_to_output, 'normal', name_file),  index=False)

        groupBy_udf.groupBy_year_and_journal(df).to_csv(os.path.join(path_to_output, 'by_journal', name_file), index=False)
