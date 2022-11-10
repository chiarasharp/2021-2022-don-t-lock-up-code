import pandas as pd


def add_year(df):
    df['year'] = pd.to_datetime(df['creation'], errors='coerce').dt.year

    return df


def add_isDOAJ(df):
    
    df['isDOAJ_citing'] = df.apply(lambda x: 'no' if pd.isnull(x['isDOAJ_citing']) else x['isDOAJ_citing'], axis=1)
    df['isDOAJ_cited'] = df.apply(lambda x: 'no' if pd.isnull(x['isDOAJ_cited']) else x['isDOAJ_cited'], axis=1)

    return df


def discard_errors(df, name_csv):
    df_null = df[(df['year'].isnull())]  # null dates

    df_null['file'] = name_csv

    df_null = df_null[['oci', 'file']].groupby('file', as_index=False).count().reset_index(drop=True)

    df_wrong = df[(df['year'] > 2024)]  # wrong dates

    df_wrong['file'] = name_csv

    df_wrong = df_wrong[['oci', 'file']].groupby('file', as_index=False).count().reset_index(drop=True)

    return df_null, df_wrong


def groupBy_year(df):
    df_citing = df[['year', 'citing']][df['isDOAJ_citing'] == 'yes'].groupby('year', as_index=False).count().reset_index(
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

    df_citations_to_DOAJ = df[['year', 'citing', 'citing_journal']][(df['isDOAJ_cited'] == 'yes') & (df['isDOAJ_citing'] == 'yes')].groupby('year', as_index=False).count().reset_index(drop=True) \
        .convert_dtypes().drop_duplicates().rename(columns={'citing': 'citations_to_DOAJ', 'citing_journal': 'journal'})

    df_cited_to_DOAJ = df[['year', 'cited', 'cited_journal']][(df['isDOAJ_cited'] == 'yes') & (df['isDOAJ_citing'] == 'yes')].groupby('year', as_index=False).count().reset_index(drop=True) \
        .convert_dtypes().drop_duplicates().rename(columns={'cited': 'cited_by_DOAJ', 'cited_journal': 'journal'})

    dfs = [df.set_index(['year', 'journal']) for df in [df_cited, df_citing, df_self_cit, df_citations_to_DOAJ, df_cited_to_DOAJ]]
    df_result = pd.concat(dfs, axis=1).fillna(0)

    return df_result
