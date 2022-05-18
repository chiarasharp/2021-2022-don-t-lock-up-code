import json
import zipfile
from io import BytesIO
import pandas as pd


def main(data_json):
    # Take all existing files already created
    general_count_dict = dict()
    with zipfile.ZipFile("./data/imported/2019-10-21T22_41_20_1-63.zip", "r") as zfile:

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
                    result = df.to_dict(orient="records")
                    json_object = json.dumps(result)
                    with open(f"./data/queried/OC/{name_df}/{name_file.replace('.csv', '').replace(':', '_')}.json",
                              "w") as outfile:
                        outfile.write(json_object)
                        outfile.close()



        with open(f"./data/queried/OC/general_count_dict.json",
                  "w") as outfile:
            json_object = json.dumps(general_count_dict)
            outfile.write(json_object)
            outfile.close


def counter_function(group_by_dict, json_file, name):
    for record in group_by_dict:

        if record["journal"] not in json_file:
            json_file[record["journal"]] = dict()
            json_file[record["journal"]][name] = 0
        elif name not in json_file[record["journal"]]:
            json_file[record["journal"]][name] = 0
        json_file[record["journal"]][name] += record[name]

    return json_file

