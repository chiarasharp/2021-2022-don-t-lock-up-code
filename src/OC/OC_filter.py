

def manage_csv_files(data_json, df, column_selected):
    df = df[df[column_selected].isin(data_json.keys())]

    # we create a new column "journal" in order to apply a groupBy operation for each journal.
    # for each record we put a new value in the new column with the correspondent journal
    # from DOAJ (the json in input).
    df["journal"] = df[column_selected].apply(lambda x: data_json[x])

    return df
