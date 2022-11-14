import pandas as pd
import pickle
from src.OC import zip_manager, csv_manager
import os
from src.udf import read_env


pd.options.mode.chained_assignment = None

'''
|--------------------------------------------------------------------------
| DESCRIPTION
|--------------------------------------------------------------------------

REQUIRED SCRIPT: /

The script iterates all over the files filtered from OpenCitations on both columns cited and citing, containing the 
DOAJ journals. The script create two different folder (cited and citing), on the specified output path.

'''

if __name__ == '__main__':

    '''
    |--------------------------------------------------------------------------
    | INPUT VARIABLES
    |--------------------------------------------------------------------------
    '''

    dict_variable = read_env.take_env_variables('../.env')

    path_zip_file = os.path.join('..', dict_variable['input_directory'])

    path_output = os.path.join('..', dict_variable['output_directory'])

    path_pickle_file = os.path.join(path_output, 'DOAJ/doi_articles_journals.pickle')

    '''
    |--------------------------------------------------------------------------
    | LOAD
    |--------------------------------------------------------------------------
    '''

    # open pickle file from previous run: it contains all the Dois divided by journals
    with open(path_pickle_file, 'rb') as pickle_file:
        data_json = pickle.load(pickle_file)

    # create a temporary folder
    if not os.path.exists(os.path.join(path_output, 'tmp')):
        os.mkdir(os.path.join(path_output, 'tmp'))

    '''
    |--------------------------------------------------------------------------
    | EXECUTION
    |--------------------------------------------------------------------------
    '''

    for csv in zip_manager.ZipIterator(path_zip_file, os.path.join(path_output, 'tmp')):
        name_file = csv.split('\\')[-1]

        # convert the read file to a Pandas dataframe
        df = pd.read_csv(csv, dtype={
            'timespan': str,
            'journal_sc': str,
            'author_sc': str,
            'creation': str,
            'cited': str,
            'citing': str,
            'oci': str
        })

        # filter the CSV records which contain the DOAJ journals on cited column
        df_cited = csv_manager.refine(df, ['oci', 'creation', 'cited'], 'cited', data_json)

        df_cited = csv_manager.add_journal(df_cited, "cited", data_json)

        # filter the CSV records which contain the DOAJ journals on citing column
        df_citing = csv_manager.refine(df, ['oci', 'creation', 'citing'], 'citing', data_json)

        df_citing = csv_manager.add_journal(df_citing, "citing", data_json)

        df_result = df_citing.merge(df_cited, how='outer').reset_index(drop=True).convert_dtypes().drop_duplicates()

        df_result.to_csv(os.path.join(path_output, f'OC/filtered/{name_file}'), index=False)

        # delete the csv file
        os.remove(csv)
