import os
import zipfile
from glob import glob
from tqdm import tqdm
import time


class ZipIterator:

    def __init__(self, path, output_file):
        self.output_file = output_file
        self.list_zip = glob(os.path.join(path, '*.zip'))
        self.all_files = self.open_zip()
        self.total_number_file = len(self.all_files)

    def __iter__(self):

        return self

    def __next__(self):

        if len(self.all_files) > 0:
            self.file = self.all_files.pop(0)

            return self.file

        elif len(self.list_zip) > 0:
            # take a rest
            print(f'\ntaking 30 second of rest')
            time.sleep(30)
            self.all_files = self.open_zip()
            if len(self.all_files) == 0:
                raise StopIteration
            self.file = self.all_files.pop(0)

            return self.file

        else:
            raise StopIteration

    def open_zip(self):
        if len(self.list_zip) > 0:
            dir_zip_name = self.list_zip.pop(0)
            print(f'\nstarting with another zip dir: {dir_zip_name}...')
            print(f'\nExtract all zipped csv files in a temporary folder...')
            with zipfile.ZipFile(dir_zip_name, 'r') as zip_ref:
                zip_ref.extractall(self.output_file)
                zip_ref.close()
            os.remove(dir_zip_name)

        all_files = glob(os.path.join(self.output_file, '*.csv'))
        self.total_number_file = len(all_files)
        print(f'\nTotal file to process {self.total_number_file}')

        return all_files
