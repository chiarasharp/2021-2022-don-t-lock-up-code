import json
import zipfile
from io import BytesIO
import pandas as pd
from os import listdir


def main(data_json, input_path_zip_file, output_file_path_general_dict, output_file_path_open_cit_json):
    list_zip_file = [f for f in listdir(input_path_zip_file)]
    general_count_dict = dict()
    for zip_file in list_zip_file:
        with zipfile.ZipFile(f"{input_path_zip_file}/{zip_file}", "r") as zfile:

            # iterate all over CSV inside zip file
            for name_file in zfile.namelist():
                print(f"---> {name_file}\n")
                # check if the file is listed in the latter files

                # convert the file from bytes
                zfiledata = BytesIO(zfile.read(name_file))

                df = pd.read_csv(zfiledata)

                my_dfs = {"cited": df[df["cited"].isin(data_json.keys())],
                          "citing": df[df["citing"].isin(data_json.keys())],
                          "open_cit": df[(df["cited"].isin(data_json.keys())) & (df["citing"].isin(data_json.keys()))]}

                for name_df, df in my_dfs.items():
                    if name_df == 'cited':
                        # we create a new column journal in order to group by journal. We take dois from column and
                        # put the corrisponded value from json file
                        df["journal"] = df["cited"].apply(lambda x: data_json[x])
                        df_count = df.groupby(["journal"], as_index=False)["cited"].count()
                        general_count_dict = counter_function(df_count.to_dict(orient="records"), general_count_dict,
                                                              "cited")

                    elif name_df == 'citing':
                        df["journal"] = df["citing"].apply(lambda x: data_json[x])
                        df_count = df.groupby(["journal"], as_index=False)["citing"].count()
                        general_count_dict = counter_function(df_count.to_dict(orient="records"), general_count_dict,
                                                              "citing")



                    elif name_df == "open_cit":

                        df["journal"] = df["cited"].apply(lambda x: data_json[x])
                        df = df.rename(columns={'journal': 'journal', 'cited':'open_cit', 'citing':'citing'})
                        # here we need a renaming because we want to use cited column but on a different df, which
                        # have
                        df_count = df.groupby(["journal"], as_index=False)["open_cit"].count()
                        general_count_dict = counter_function(df_count.to_dict(orient="records"), general_count_dict,
                                                              "open_cit")

                    with open(f"{output_file_path_open_cit_json}/general_count_dict.json",
                              "w") as outfile:
                        json_object = json.dumps(general_count_dict)
                        outfile.write(json_object)
                        outfile.close


                        # result = df.to_dict(orient="records")
                        # json_object = json.dumps(result)
                        # with open(f"E:/{name_df}/{name_file.replace('.csv', '').replace(':', '_')}.json",
                        #           "w") as outfile:
                        #     outfile.write(json_object)
                        #     outfile.close()






def counter_function(group_by_dict, json_file, name):
    for record in group_by_dict:

        if record["journal"] not in json_file:
            json_file[record["journal"]] = dict()
            json_file[record["journal"]]["cited"] = 0
            json_file[record["journal"]]["citing"] = 0
            json_file[record["journal"]]["open_cit"] = 0
        json_file[record["journal"]][name] += record[name]

    return json_file
