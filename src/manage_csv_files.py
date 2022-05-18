import json
import zipfile
from io import BytesIO
import pandas as pd
from os import listdir


def main(data_json):
    with zipfile.ZipFile("./data/imported/2019-10-21T22_41_20_1-63.zip", "r") as zfile:

        files = {"citing": [f for f in listdir("data/queried/OC/citing") if f != ".gitignore"],
                 "cited": [f for f in listdir("data/queried/OC/cited") if f != ".gitignore"]}

        for name_file in zfile.namelist():
            print(f"---> {name_file}\n")
            if f"{name_file.replace('.csv', '').replace(':', '_')}.json" not in files["cited"] \
                    and f"{name_file.replace('.csv', '').replace(':', '_')}.json" not in files["citing"]:

                zfiledata = BytesIO(zfile.read(name_file))

                df = pd.read_csv(zfiledata)

                my_dfs = {"cited": df[df["cited"].isin(data_json)], "citing": df[df["citing"].isin(data_json)]}

                for name_df, df in my_dfs.items():

                    if f"{name_file.replace('.csv', '').replace(':', '_')}.json" not in files[name_df]:
                        result = df.to_dict(orient="records")
                        json_object = json.dumps(result)

                        with open(f"./data/queried/OC/{name_df}/{name_file.replace('.csv', '').replace(':', '_')}.json",
                                  "w") as outfile:
                            outfile.write(json_object)
