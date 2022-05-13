import json
import pickle

all_dois=[]

with open('doi.json', 'r', encoding="utf-8") as json_file:
    p = json.load(json_file)

    for i in p:
        all_dois.extend(p[i]["dois"])
all_dois_set = set(all_dois)

with open('doi_articles.pickle', 'wb') as pickle_file:
    pickle.dump(all_dois_set, pickle_file, protocol=pickle.HIGHEST_PROTOCOL)
