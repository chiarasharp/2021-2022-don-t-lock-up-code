import os


def crete_new_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


input_directory_OC = input('\nWhat is the path to OpenCitations directory?\n > ')
input_DOAJ_journals = input('\nWhat is the path to the DOAJ journals dump directory?\n > ')
input_DOAJ_articles = input('\nWhat is the path to the DOAJ articles dump directory?\n > ')
output_directory = input('\nWhat is the path to the directory for storing the transformed files?\n > ')
with open('.env', 'w') as f:
    f.write(f'input_directory={input_directory_OC}\n')
    f.write(f'output_directory={output_directory}\n')
    f.write(f'input_DOAJ_journals={input_DOAJ_journals}\n')
    f.write(f'input_DOAJ_articles={input_DOAJ_articles}\n')

crete_new_dir(output_directory)
crete_new_dir(os.path.join(output_directory, 'errors'))
crete_new_dir(os.path.join(output_directory, 'errors', 'null'))
crete_new_dir(os.path.join(output_directory, 'errors', 'wrong'))
crete_new_dir(os.path.join(output_directory, 'OC'))
crete_new_dir(os.path.join(output_directory, 'DOAJ'))
crete_new_dir(os.path.join(output_directory, 'OC', 'filtered'))
crete_new_dir(os.path.join(output_directory, 'OC', 'group_by_year'))
crete_new_dir(os.path.join(output_directory, 'OC', 'group_by_year', 'normal'))
crete_new_dir(os.path.join(output_directory, 'OC', 'group_by_year', 'by_journal'))
