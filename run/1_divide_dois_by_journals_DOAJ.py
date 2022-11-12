from src.DOAJ.set_dois import set_dois
from src.DOAJ.create_json_dois import create_json_dois
import os

if __name__ == "__main__":
    '''
    |--------------------------------------------------------------------------
    | INPUT VARIABLES
    |--------------------------------------------------------------------------
    '''

    path_to_DOAJ_journals_dump = os.path.join('..', 'DOAJ', 'doaj_journal_data_2022-05-01.tar.gz')

    path_to_DOAJ_articles_dump = os.path.join('..', 'DOAJ', 'doaj_article_data_2022-05-01.tar.gz')

    path_output_files = os.path.join('..', os.getenv('output_directory'), 'DOAJ')

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

    dois_divided_by_journals = create_json_dois(path_to_DOAJ_journals_dump, path_to_DOAJ_articles_dump, path_output_files)

    set_dois(dois_divided_by_journals, path_output_files)
