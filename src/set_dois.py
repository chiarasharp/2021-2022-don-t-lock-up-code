import json
import pickle


def main():
    all_dois=[]

    with open('./data/queried/DOAJ/doi.json', 'r', encoding="utf-8") as json_file:
        p = json.load(json_file)

        for i in p:
            all_dois.extend(p[i]["dois"])
    all_dois_set = set(all_dois)

    with open('./data/queried/DOAJ/doi_articles.pickle', 'wb') as pickle_file:
        pickle.dump(all_dois_set, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
