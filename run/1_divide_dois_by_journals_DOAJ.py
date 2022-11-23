from src.DOAJ.set_dois import set_dois
from src.DOAJ.create_json_dois import create_json_dois
import os
from src.udf import read_env

if __name__ == "__main__":
    '''
    |--------------------------------------------------------------------------
    | INPUT VARIABLES
    |--------------------------------------------------------------------------
    '''

    dict_variable = read_env.take_env_variables('../.env')

    path_to_DOAJ_journals_dump = os.path.join('..', dict_variable['input_DOAJ_journals'])

    path_to_DOAJ_articles_dump = os.path.join('..', dict_variable['input_DOAJ_articles'])

    path_output_files = os.path.join('..', dict_variable['output_directory'], 'DOAJ')

    '''
    |--------------------------------------------------------------------------
    | LOAD
    |--------------------------------------------------------------------------
    '''

    # //

    '''
    |--------------------------------------------------------------------------
    | EXECUTION
    |--------------------------------------------------------------------------
    '''

    dois_divided_by_journals = create_json_dois(path_to_DOAJ_journals_dump,
                                                path_to_DOAJ_articles_dump,
                                                path_output_files)

    set_dois(dois_divided_by_journals, path_output_files)

    '''
    |--------------------------------------------------------------------------
    | SAVE
    |--------------------------------------------------------------------------
    '''

    # //
