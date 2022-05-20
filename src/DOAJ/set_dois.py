import json
import pickle


# transform for further computation doi.json in doi: issn-pissn

def main(path_to_dois_file):
    all_dois = {}

    with open(path_to_dois_file, 'r', encoding="utf-8") as json_file:

        p = json.load(json_file)

        for i in p:
            for doi in p[i]["dois"]:
                all_dois[doi] = i

    with open('./data/queried/DOAJ/doi_articles_journals.pickle', 'wb') as pickle_file:
        pickle.dump(all_dois, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
