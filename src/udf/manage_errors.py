from glob import glob
import os
import json


def manage_errors(path_to_err_folder, output_err_categories_json):
    titles = []
    count = []

    # getting the json files with the errors
    all_files = glob(os.path.join(path_to_err_folder, "*.json"))

    for f in all_files:
        # getting the titles of the files
        titles.append(f[7:-5])
        with open(f) as inf:
            j = json.load(inf)

            # counting the elements inside the files
            count.append(len(j))

    # creating a dictionary of the count of each category of errors and dumping it in a json
    dictionary = dict(zip(titles, count))
    with open(output_err_categories_json, "w") as outfile:
        json.dump(dictionary, outfile)