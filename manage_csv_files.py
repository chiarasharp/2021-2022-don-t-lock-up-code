import json
import zipfile
from io import BytesIO
import pandas as pd


with zipfile.ZipFile("data/imported/2019-10-21T22_41_20_1-63.zip", "r") as zfile:
    for name_file in zfile.namelist():
        print(f"---> {name_file}\n")
        zfiledata = BytesIO(zfile.read(name_file))

        df = pd.read_csv(zfiledata)

        my_dfs = {"cited": df[df["cited"].isin(data)], "citing": df[df["citing"].isin(data)]}

        for name_df, df in my_dfs.items():

            result = df.to_json(orient="records")
            json_object = json.dumps(result, indent=4)

            with open(f"./data/selected/{name_df}/{name_file.replace('.csv', '').replace(':', '_')}.json", "w") as outfile:
                outfile.write(json_object)