def refine(df, selected_columns, filtering_column, filtering_data):
    # select columns
    df = df[selected_columns]

    # filter on data imported
    df = df[df[filtering_column].isin(filtering_data.keys())]

    # reset index and drop duplicates
    df = df.reset_index(drop=True).convert_dtypes().drop_duplicates()

    return df


def add_journal(df, column_selected, journal_data):
    # we create a new column 'journal' in order to apply a groupBy operation for each journal.
    # for each record we put a new value in the new column with the correspondent journal
    # from DOAJ (the json in input).
    df[f"{column_selected}_journal"] = df[column_selected].apply(lambda x: journal_data[x])
    df[f"isDOAJ_{column_selected}"] = 'yes'

    return df
