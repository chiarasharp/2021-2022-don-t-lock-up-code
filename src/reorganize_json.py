from os import listdir
from os.path import isfile, join
import json
import gc



def main(dois_by_journal):
    # take all json data from cited and citing repository

    files = {"citing": [f for f in listdir("data/queried/OC/citing") if f != ".gitignore"],
             "cited": [f for f in listdir("data/queried/OC/cited") if f != ".gitignore"]}

    for name_list, list_file in files.items():
        general_dict = dict()
        for i, json_file in enumerate(list_file):
            print(f"{i+1}/{len(list_file)}")
            with open(f"data/queried/OC/{name_list}/{json_file}", 'r') as j:
                contents = json.loads(j.read())

                j.close()

                for record in contents:

                    journal_id = dois_by_journal[record[name_list]]

                    if journal_id not in general_dict:
                        general_dict[journal_id] = []
                    general_dict[journal_id].append(record)
                with open(f'E:/data/{name_list}/{json_file}', 'w', encoding='utf8') as json_file:
                    json.dump(general_dict, json_file, ensure_ascii=False)
                    json_file.close()



def reorganize_json_doi_DOAJ(dois_by_journal):
    general_dict = dict()
    for i, (journal_id, value) in enumerate(dois_by_journal.items()):
        print(f"{i}/{len(dois_by_journal)}")

        for i in value["dois"]:
            general_dict[i] = journal_id

    with open('./data/queried/DOAJ/reorganize_doi.json', 'w', encoding='utf8') as json_file:
        json.dump(general_dict, json_file, ensure_ascii=False)
