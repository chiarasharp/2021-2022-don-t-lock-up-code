import unittest
import os
import json
import pickle
from glob import glob


class DoisTest(unittest.TestCase):

    def setUp(self):
        with open(os.path.join('..', 'queried', 'DOAJ', 'doi.json'), 'r', encoding='utf-8') as json_file:
            self.all_dois = json.load(json_file)

        with open(os.path.join('..', 'queried', 'DOAJ', 'doi_articles_journals.pickle'), 'rb') as pickle_file:
            self.pickle_file = pickle.load(pickle_file)

        with open(os.path.join('..', 'queried', 'DOAJ', 'duplicated_dois.json'), 'r', encoding='utf-8') as json_file:
            self.duplicated_dois = json.load(json_file)

        with open(os.path.join('..', 'queried', 'DOAJ', 'articles_without_doi.json'), 'r', encoding='utf-8') as json_file:
            self.discarded_articles = json.load(json_file)

        self.all_articles = glob(os.path.join('..', 'queried', 'DOAJ', 'doaj_article_data_2022-05-01', '*json'))

        with open(os.path.join('..', 'queried', 'DOAJ', 'metrics.json'), 'r', encoding='utf-8') as json_file:
            self.metrics = json.load(json_file)

    def test_pickle_file_is_without_repeated_dois(self):

        list_doi_from_dois_json = list()
        list_repeated_dois_count = dict()
        list_no_repeated_dois = self.pickle_file.keys()

        for article in self.all_dois.values():
            list_doi_from_dois_json += article['dois']

        for doi in list_doi_from_dois_json:
            if doi in list_no_repeated_dois and doi not in list_repeated_dois_count:
                list_repeated_dois_count[doi] = 0
            else:
                list_repeated_dois_count[doi] += 1

        self.assertEqual(len(list_no_repeated_dois) + sum(list_repeated_dois_count.values()),
                         len(list_doi_from_dois_json))

    def test_processed_article_are_articles_with_and_without_dois(self):

        list_doi_from_dois_json = list()

        for article in self.all_dois.values():
            list_doi_from_dois_json += article['dois']

        number_accepted_dois = len(list_doi_from_dois_json)
        number_total_articles_no_dois = int(self.metrics['n_articles_no_dois'])
        number_total_dois_processed = int(self.metrics['n_articles_processed'])

        self.assertEqual(number_total_articles_no_dois + number_accepted_dois, number_total_dois_processed)


if __name__ == '__main__':
    unittest.main()
