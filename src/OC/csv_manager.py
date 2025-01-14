import json
import pandas as pd

'''
|--------------------------------------------------------------------------
| MAKE NUMERICAL OPERATION 
|--------------------------------------------------------------------------
'''


def pcent_division(a, b):
    if b > 0:
        return round((a / b) * 100, 2)
    return 0


def division(a, b):
    if b > 0:
        return round((a / b), 2)
    return 0


def make_ratio_journal(json_file: json):
    for journal in json_file:
        journal.update({'citing_cited_pcent': pcent_division(journal['citing'], journal['cited'])})
        journal.update({'citations_to_DOAJ_pcent': pcent_division(journal['citations_to_DOAJ'], journal['citing'])})
        journal.update({'cited_by_DOAJ_pcent': pcent_division(journal['cited_by_DOAJ'], journal['cited'])})
        journal.update({'self_citation_pcent': pcent_division(journal['self_citation'],
                                                              (journal['cited'] + journal['citing']))})
        journal.update({'citing_cited_ratio': division(journal['citing'], journal['cited'])})
        journal.update({'citations_to_DOAJ_ratio': division(journal['citations_to_DOAJ'], journal['citing'])})
        journal.update({'cited_by_DOAJ_ratio': division(journal['cited_by_DOAJ'], journal['cited'])})
        journal.update({'self_citation_ratio': division(journal['self_citation'],
                                                        (journal['cited'] + journal['citing']))})

    return json_file


def make_ratio(json_file: json):
    for year in json_file:
        year.update({'citing_cited_pcent': pcent_division(year['citing'], year['cited'])})
        year.update({'self_citation_pcent': pcent_division(year['self_citation'], (year['citing'] + year['cited']))})
        year.update({'citing_cited_ratio': division(year['citing'], year['cited'])})
        year.update({'self_citation_ratio': division(year['self_citation'], (year['citing'] + year['cited']))})

    return json_file


'''
|--------------------------------------------------------------------------
| FILTER COLUMNS
|--------------------------------------------------------------------------
'''


def delete_null_values(df, filtering_column):
    df_null_values = df[df[filtering_column].isnull()]

    df = df[df[filtering_column].notnull()]

    return df, df_null_values


def refine(df, selected_columns, filtering_column, filtering_data):
    # select columns
    df = df[selected_columns]

    # filter on data imported
    df = df[df[filtering_column].isin(filtering_data.keys())]

    # reset index and drop duplicates
    df = df.reset_index(drop=True).convert_dtypes().drop_duplicates()

    return df


'''
|--------------------------------------------------------------------------
| ADD COLUMNS
|--------------------------------------------------------------------------
'''


def add_journal(df, column_selected, journal_data):
    # we create a new column 'journal' in order to apply a groupBy operation for each journal.
    # for each record we put a new value in the new column with the correspondent journal
    # from DOAJ (the json in input).
    df[f'{column_selected}_journal'] = df[column_selected].apply(lambda x: journal_data[x])
    df[f'isDOAJ_{column_selected}'] = 'yes'

    return df


def add_year(df, name_column):
    df['year'] = pd.to_datetime(df[name_column], errors='coerce').dt.year

    return df


def add_isDOAJ(df):
    df['isDOAJ_citing'] = df.apply(lambda x: 'no' if pd.isnull(x['isDOAJ_citing']) else x['isDOAJ_citing'], axis=1)
    df['isDOAJ_cited'] = df.apply(lambda x: 'no' if pd.isnull(x['isDOAJ_cited']) else x['isDOAJ_cited'], axis=1)

    return df


'''
|--------------------------------------------------------------------------
| MANAGE ERRORS
|--------------------------------------------------------------------------
'''


def save_errors(df, name_csv):
    df['year'] = df['year'].fillna(0)
    df = df.astype({'year': 'int32'})

    # null dates
    df_null = df[df['year'] == 0]

    df_null['file'] = name_csv

    # wrong dates
    df_wrong = df[(df['year'] != 0) & (df['year'] > 2024)]

    df_wrong['file'] = name_csv

    # discard errors from main dataframe
    df = discard_errors(df)

    # group by
    df_wrong = df_wrong[['oci', 'file']].groupby('file', as_index=False).count().reset_index(drop=True)

    df_null = df_null[['oci', 'file']].groupby('file', as_index=False).count().reset_index(drop=True)

    return df, df_null, df_wrong


def discard_errors(df):
    df = df[(df['year'] != 0) & (df['year'] <= 2024)]

    return df


'''
|--------------------------------------------------------------------------
| GROUP BY OPERATION
|--------------------------------------------------------------------------
'''


def groupBy_year(df):
    df_citing = df[['year', 'citing']][df['isDOAJ_citing'] == 'yes'].groupby('year',
                                                                             as_index=False).count().reset_index(
        drop=True).convert_dtypes().drop_duplicates()
    df_cited = df[['year', 'cited']][df['isDOAJ_cited'] == 'yes'].groupby('year', as_index=False).count().reset_index(
        drop=True).convert_dtypes().drop_duplicates()

    df_self_cit = df[['year', 'cited']][(df['isDOAJ_cited'] == 'yes') & (df['isDOAJ_citing'] == 'yes')].groupby('year',
                                                                                                                as_index=False).count().reset_index(
        drop=True) \
        .convert_dtypes().drop_duplicates().rename(columns={'cited': 'self_citation'})

    dfs = [df.set_index('year') for df in [df_cited, df_citing, df_self_cit]]
    df_result = pd.concat(dfs, axis=1).fillna(0)

    return df_result


def groupBy_year_and_journal(df):
    df_citing = df[['year', 'citing', 'citing_journal']][df['isDOAJ_citing'] == 'yes'] \
        .groupby(['year', 'citing_journal'], as_index=False).count().reset_index(
        drop=True).convert_dtypes().drop_duplicates().rename(columns={'citing_journal': 'journal'})

    df_cited = df[['year', 'cited', 'cited_journal']][df['isDOAJ_cited'] == 'yes'] \
        .groupby(['year', 'cited_journal'], as_index=False).count().reset_index(
        drop=True).convert_dtypes().drop_duplicates().rename(columns={'cited_journal': 'journal'})

    df_self_cit = df[['year', 'cited', 'cited_journal']][df['cited_journal'] == df['citing_journal']] \
        .groupby(['year', 'cited_journal'], as_index=False).count().reset_index(drop=True) \
        .convert_dtypes().drop_duplicates().rename(columns={'cited': 'self_citation', 'cited_journal': 'journal'})

    df_citations_to_DOAJ = df[['year', 'citing', 'citing_journal']][
        (df['isDOAJ_cited'] == 'yes') & (df['isDOAJ_citing'] == 'yes')].groupby(['year', 'citing_journal'],
                                                                                as_index=False).count().reset_index(
        drop=True) \
        .convert_dtypes().drop_duplicates().rename(columns={'citing': 'citations_to_DOAJ', 'citing_journal': 'journal'})

    df_cited_to_DOAJ = df[['year', 'cited', 'cited_journal']][
        (df['isDOAJ_cited'] == 'yes') & (df['isDOAJ_citing'] == 'yes')].groupby(['year', 'cited_journal'],
                                                                                as_index=False).count().reset_index(
        drop=True) \
        .convert_dtypes().drop_duplicates().rename(columns={'cited': 'cited_by_DOAJ', 'cited_journal': 'journal'})

    dfs = [df.set_index(['year', 'journal']) for df in
           [df_cited, df_citing, df_self_cit, df_citations_to_DOAJ, df_cited_to_DOAJ]]
    df_result = pd.concat(dfs, axis=1).fillna(0)

    return df_result


'''
|--------------------------------------------------------------------------
| CONCAT OPERATION
|--------------------------------------------------------------------------
'''


def concat_csv(all_csv):
    all_df = [pd.read_csv(f) for f in all_csv]

    df = pd.concat(all_df)

    return df


def concat_csv_normal(all_csv):
    all_df = [pd.read_csv(f) for f in all_csv]

    df = pd.concat(all_df)

    df = df.groupby('year', as_index=False).sum().reset_index(
        drop=True).convert_dtypes()

    return df


def concat_csv_journal(all_csv):
    all_df = [pd.read_csv(f) for f in all_csv]

    df = pd.concat(all_df)

    df = df.groupby(['year', 'journal'], as_index=False).sum().reset_index(
        drop=True).convert_dtypes()

    return df


def add_to_journals_DOAJ_descriptions(df, df_journals_description):
    df_journals_description['journal'] = df_journals_description.index
    df_journals_description['dois'] = df_journals_description.apply(lambda x: len(x['dois']), axis=1)
    df_journals_description = df_journals_description.reset_index(level=0)
    df_journals_description = df_journals_description.drop('index', axis=1)
    df_journals_description = df_journals_description.rename({'dois': 'dois_count'}, axis=1)

    df_final = df_journals_description.merge(df, on='journal')

    return df_final
