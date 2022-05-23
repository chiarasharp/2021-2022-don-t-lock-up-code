import os
import unittest
import json

from src.DOAJ.create_json_dois import create_json_dois


class DOAJDataTestCase(unittest.TestCase):

    def setUp(self):
        self.DOAJ_test_journals = "test/DOAJ/sample.tar.gz"
        self.DOAJ_test_articles = "test/DOAJ/sample_art.tar.gz"
        self.doi_json_path = "data/queried/DOAJ/doi.json"
        self.art_wout_dois_path = "data/queried/DOAJ/articles_without_doi.json"
        self.num_of_art_wout_dois = 1
        self.num_of_journals = 4

    def test_create_json_dois(self):
        create_json_dois(self.DOAJ_test_journals, self.DOAJ_test_articles)
        self.assertTrue(os.path.isfile(self.doi_json_path))
        self.assertTrue(os.path.isfile(self.art_wout_dois_path))

        f = open(self.doi_json_path)
        dois = json.load(f)
        self.assertEqual(len(dois), self.num_of_journals)

        f = open(self.art_wout_dois_path)
        art_wout_dois = json.load(f)
        self.assertEqual(len(art_wout_dois), self.num_of_art_wout_dois)


if __name__ == '__main__':
    unittest.main()
