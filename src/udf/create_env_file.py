import sys

input_directory_OC = sys.argv[1]
output_directory = sys.argv[2]
input_DOAJ_journals = sys.argv[3]
input_DOAJ_articles = sys.argv[4]

with open(".env", "w") as f:
    f.write(f"input_directory={input_directory_OC}\n")
    f.write(f"output_directory={output_directory}\n")
    f.write(f"input_DOAJ_journals={input_DOAJ_journals}\n")
    f.write(f"input_DOAJ_articles={input_DOAJ_articles}\n")
