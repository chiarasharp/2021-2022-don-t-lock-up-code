from src.DOAJ.set_dois import set_dois

if __name__ == "__main__":

    path_dois_by_journ = input(str("\nPath to dois divided by journals JSON\n\n > "))

    path_output_files = input(str("\nPath for output files\n\n > "))

    print("\n\n")

    set_dois(path_dois_by_journ, path_output_files)
