from src.DOAJ.create_json_dois import create_json_dois

if __name__ == "__main__":

    path_DOAJ_journ = input(str("\nPath to journals dump from DOAJ\n\n > "))

    path_DOAJ_art = input(str("\nPath to articles dump from DOAJ\n\n > "))

    path_output_files = input(str("\nPath for output files\n\n > "))

    print("\n\n")

    create_json_dois(path_DOAJ_journ, path_DOAJ_art, path_output_files)
