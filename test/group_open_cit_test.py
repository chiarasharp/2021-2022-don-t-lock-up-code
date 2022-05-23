import os
import unittest
import json

from src.udf.group_open_cit import group_open_cit


class GroupOpenCitTestCase(unittest.TestCase):

    def setUp(self):
        self.open_cit_test_files_path = "test/open_cit"
        self.open_cit_years_path = "open_cit_in_years.json"
        self.open_cit_err_path = "open_cit_w_date_err.json"
        self.num_of_open_cit_err = 6
        self.num_of_open_cit_years = 4
        self.num_cit_2019 = 3
    
    def test_group_open_cit(self):
        group_open_cit(self.open_cit_test_files_path, self.open_cit_years_path, self.open_cit_err_path)
        self.assertTrue(os.path.isfile(self.open_cit_years_path))
        self.assertTrue(os.path.isfile(self.open_cit_err_path))

        f = open(self.open_cit_years_path)
        open_cit_years = json.load(f)
        self.assertEqual(len(open_cit_years), self.num_of_open_cit_years)

        f = open(self.open_cit_err_path)
        open_cit_err = json.load(f)
        self.assertEqual(len(open_cit_err), self.num_of_open_cit_err)


if __name__ == '__main__':
    unittest.main()