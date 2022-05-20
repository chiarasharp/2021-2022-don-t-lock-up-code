import json
from glob import glob
import os
from datetime import datetime as dt

all_files = glob(os.path.join("E:/open_cit", "*.json"))
list_errors = list()
total_length = 0
for file in all_files:
    # print(list_errors)
    with open(file, "r") as json_file:
        print(file)
        data = json.load(json_file)
        total_length += len(data)

        for record in data:
            try:
                if dt.strptime(str(record["creation"]), '%Y-%m-%d') > dt.strptime("2022-06-01", '%Y-%m-%d'):
                    # print(record)
                    list_errors.append(record)
            except ValueError:
                try:
                    if dt.strptime(str(record["creation"]), '%Y-%m') > dt.strptime("2022-06", '%Y-%m'):
                        # print(record)
                        list_errors.append(record)
                except ValueError:
                    try:
                        if dt.strptime(str(record["creation"]), '%Y') > dt.strptime("2022", '%Y'):
                            # print(record)
                            list_errors.append(record)
                    except:
                        # print(record)
                        list_errors.append(record)
print(f"{len(list_errors)}/{total_length}")


