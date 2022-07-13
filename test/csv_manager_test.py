import os
import unittest
import pickle
import json
from src.OC.manage_csv_files import main as manage_csv_files


class CsvManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.open_cit_path = "OC/open_cit/testing_csv.json"
        self.general_count_dict_path = "OC/general_count_dict.json"
        self.expected_general_dict = {'0042-790X1338-4333': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '0100-29451806-9967': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1020-49891680-5348': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1027-56061607-7938': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1080-60401080-6059': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1319-24422320-3838': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1471-2350': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1471-2458': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1687-59151687-5923': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1750-1172': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1752-1947': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1817-17371998-3557': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1932-6203': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '1935-27271935-2735': {'cited': 2, 'citing': 0, 'open_cited': 2, 'open_citing': 0},
                                      '2073-4441': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '2075-163X': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '2195-32282251-7715': {'cited': 1, 'citing': 2, 'open_cited': 1, 'open_citing': 2},
                                      '2223-76902223-7704': {'cited': 1, 'citing': 2, 'open_cited': 1, 'open_citing': 2},
                                      '2405-65612405-5816': {'cited': 1, 'citing': 0, 'open_cited': 1, 'open_citing': 0},
                                      '0539-61151665-1146': {'cited': 0, 'citing': 11, 'open_cited': 0, 'open_citing': 11},
                                      '1672-51071995-8226': {'cited': 0, 'citing': 1, 'open_cited': 0, 'open_citing': 1},
                                      '2095-82932198-7823': {'cited': 0, 'citing': 1, 'open_cited': 0, 'open_citing': 1},
                                      '2190-05582190-0566': {'cited': 0, 'citing': 1, 'open_cited': 0, 'open_citing': 1},
                                      '2190-54872190-5495': {'cited': 0, 'citing': 2, 'open_cited': 0, 'open_citing': 2}}

    def test_group_open_cit(self):

        path_zip_file = "imported/"
        path_output_open_cit_json = "./OC"
        path_output_general_dict = "./OC"
        with open('../data/queried/DOAJ/doi_articles_journals.pickle', 'rb') as pickle_file:
            data_json = pickle.load(pickle_file)

            manage_csv_files(data_json, path_zip_file, path_output_open_cit_json, path_output_general_dict)

        with open("./OC/general_count_dict.json", "r") as json_file:
            data_dict = json.load(json_file)

        self.assertEqual(data_dict, self.expected_general_dict)

        total_number = 0
        for i in data_dict.values():
            total_number += len(i)
        self.assertTrue(total_number // len(data_dict) == 4)

        self.assertTrue(os.path.isfile(self.open_cit_path))
        self.assertTrue(os.path.isfile(self.general_count_dict_path))

        with open(self.open_cit_path, "r") as json_file:
            data_open_cit = json.load(json_file)

        self.assertTrue(len(data_open_cit) <= len(data_dict))


if __name__ == '__main__':
    unittest.main()