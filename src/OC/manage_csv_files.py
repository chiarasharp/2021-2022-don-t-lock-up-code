import json
import zipfile
from io import BytesIO
import pandas as pd
from os import listdir


def main(data_json, input_path_zip_file, output_file_path_general_dict, output_file_path_open_cit_json):
    list_zip_file = [f for f in listdir(input_path_zip_file)]
    general_count_dict = dict()
    # iterate all over zip file
    for zip_file in list_zip_file:
        with zipfile.ZipFile(f"{input_path_zip_file}/{zip_file}", "r") as zfile:

            # iterate all over CSV inside zip file
            for name_file in zfile.namelist():
                print(f"---> {name_file}\n")
                # check if the file is listed in the latter files

                # convert the file from bytes
                zfiledata = BytesIO(zfile.read(name_file))

                # convert the readed file to a Pandas dataframe
                df = pd.read_csv(zfiledata)

                my_dfs = {"cited": df[df["cited"].isin(data_json.keys())],
                          "citing": df[df["citing"].isin(data_json.keys())],
                          "open_cit": df[(df["cited"].isin(data_json.keys())) & (df["citing"].isin(data_json.keys()))]}

                for name_df, df in my_dfs.items():
                    if name_df == 'cited':
                        # we create a new column "journal" in order to apply a groupBy operation for each journal.
                        # for each record we put a new value in the new column with the correspondent journal
                        # from DOAJ (the json in input).
                        df["journal"] = df["cited"].apply(lambda x: data_json[x])
                        # groupBy and count of the column cited
                        df_count = df.groupby(["journal"], as_index=False)["cited"].count()

                        # Then we transform our dataframe in a dict for adding its values to a general dict
                        general_count_dict = counter_function(df_count.to_dict(orient="records"), general_count_dict,
                                                              "cited")

                    elif name_df == 'citing':
                        # we create a new column "journal" in order to apply a groupBy operation for each journal.
                        # for each record we put a new value in the new column with the correspondent journal
                        # from DOAJ (the json in input).
                        df["journal"] = df["citing"].apply(lambda x: data_json[x])
                        # groupBy and count of the column citing
                        df_count = df.groupby(["journal"], as_index=False)["citing"].count()

                        # Then we transform our dataframe in a dict for adding its values to a general dict
                        general_count_dict = counter_function(df_count.to_dict(orient="records"), general_count_dict,
                                                              "citing")



                    elif name_df == "open_cit":
                        # we create a deep copy of the dataframe for using it for another computation
                        copy_df = df.copy()
                        # we create a new column "journal" in order to apply a groupBy operation for each journal.
                        # for each record we put a new value in the new column with the correspondent journal
                        # from DOAJ (the json in input). Then we rename the columns for creating a new field
                        # in the general dict
                        df["journal"] = df["cited"].apply(lambda x: data_json[x])
                        df = df.rename(columns={'journal': 'journal', 'cited':'open_cited', 'citing':'citing'})
                        # groupBy and count of the column open_cited
                        df_count = df.groupby(["journal"], as_index=False)["open_cited"].count()
                        # Then we transform our dataframe in a dict for adding its values to a general dict
                        general_count_dict = counter_function(df_count.to_dict(orient="records"), general_count_dict,
                                                              "open_cited")


                        # we create a new column "journal" in order to apply a groupBy operation for each journal.
                        # for each record we put a new value in the new column with the correspondent journal
                        # from DOAJ (the json in input). Then we rename the columns for creating a new field
                        # in the general dict
                        copy_df["journal"] = copy_df["citing"].apply(lambda x: data_json[x])
                        # groupBy and count of the column open_citing
                        copy_df = copy_df.rename(columns={'journal': 'journal', 'cited':'cited', 'citing':'open_citing'})
                        df_count = copy_df.groupby(["journal"], as_index=False)["open_citing"].count()
                        # Then we transform our dataframe in a dict for adding its values to a general dict
                        general_count_dict = counter_function(df_count.to_dict(orient="records"), general_count_dict,
                                                              "open_citing")

                        # we save for each iteration the df filtered by DOAJ dois on both columns (cited and citing)
                        # in a json format
                        result = df.to_dict(orient="records")
                        json_object = json.dumps(result)
                        with open(f"{output_file_path_open_cit_json}/{name_df}/{name_file.replace('.csv', '').replace(':', '_')}.json",
                                  "w") as outfile:
                            outfile.write(json_object)
                            outfile.close()

                    # we save for each iteration the the general dict
                    with open(f"{output_file_path_general_dict}/general_count_dict_prova.json",
                              "w") as outfile:
                        json_object = json.dumps(general_count_dict)
                        outfile.write(json_object)
                        outfile.close


def counter_function(group_by_dict, json_file, name):
    for record in group_by_dict:

        if record["journal"] not in json_file:
            json_file[record["journal"]] = dict()
            json_file[record["journal"]]["cited"] = 0
            json_file[record["journal"]]["citing"] = 0
            json_file[record["journal"]]["open_cited"] = 0
            json_file[record["journal"]]["open_citing"] = 0
        json_file[record["journal"]][name] += record[name]

    return json_file
