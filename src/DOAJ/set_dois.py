import json
import pickle


# transform for further computation doi.json in doi: issn-pissn

def set_dois(path_to_dois_file, path_output_files):
    all_dois = {}

    with open(path_to_dois_file, 'r', encoding="utf-8") as json_file:

        p = json.load(json_file)

        for i in p:
            for doi in p[i]["dois"]:
                if doi in all_dois:
                    print(doi)
                all_dois[doi] = i

    with open(f'{path_output_files}', 'wb') as pickle_file:
        pickle.dump(all_dois, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)


