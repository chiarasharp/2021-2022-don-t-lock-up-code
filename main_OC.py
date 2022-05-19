from src.OC.manage_csv_files import main as manage_csv_files
import pickle

if __name__ == "__main__":

    with open('./data/queried/DOAJ/doi_articles_journals.pickle', 'rb') as pickle_file:
        data_json = pickle.load(pickle_file)

        manage_csv_files(data_json, "E:/6741422", "E:/6741422/data", "./data/queried/OC")


