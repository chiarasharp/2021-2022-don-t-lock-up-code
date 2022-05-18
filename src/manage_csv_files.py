import json
import zipfile
from io import BytesIO
import pandas as pd
from os import listdir
import pickle

def main(data_json):
    with zipfile.ZipFile("./data/imported/2019-10-21T22_41_20_1-63.zip", "r") as zfile:
        files = {"citing": [f for f in listdir("./data/queried/OC/citing") if f != ".gitignore"],
                 "cited": [f for f in listdir("./data/queried/OC/cited") if f != ".gitignore"],
                 "open_cit": [f for f in listdir("./data/queried/OC/open_cit") if f != ".gitignore"]}

        for name_file in zfile.namelist():
            print(f"---> {name_file}\n")
            if f"{name_file.replace('.csv', '').replace(':', '_')}.json" not in files["cited"] \
                    and f"{name_file.replace('.csv', '').replace(':', '_')}.json" not in files["citing"]\
                    and f"{name_file.replace('.csv', '').replace(':', '_')}.json" not in files["open_cit"]:
                print("hello")
                zfiledata = BytesIO(zfile.read(name_file))

                df = pd.read_csv(zfiledata)

                my_dfs = {"cited": df[df["cited"].isin(data_json.keys())], "citing": df[df["citing"].isin(data_json.keys())], "open_cit": df[(df["cited"].isin(data_json.keys())) & (df["citing"].isin(data_json.keys()))]}

                for name_df, df in my_dfs.items():
                    if name_df == 'cited':
                        df["journal"] = df["cited"].apply(lambda x: data_json[x])
                    else:
                        df["journal"] = df["citing"].apply(lambda x: data_json[x])

                    
                    if f"{name_file.replace('.csv', '').replace(':', '_')}.json" not in files[name_df]:
                        result = df.to_dict(orient="records")
                        json_object = json.dumps(result)

                        with open(f"./data/queried/OC/{name_df}/{name_file.replace('.csv', '').replace(':', '_')}.json",
                                  "w") as outfile:
                            outfile.write(json_object)
            break

with open('./data/queried/DOAJ/doi_articles_journals.pickle', 'rb') as pickle_file:
    data_json = pickle.load(pickle_file)


main(data_json)
