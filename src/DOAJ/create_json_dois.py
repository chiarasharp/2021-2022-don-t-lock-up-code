import tarfile
import json


def create_json_dois(path_to_DOAJ_journ_zip, path_to_DOAJ_art_zip):
    # Initializing the set that will contain all of the journals 'issn+eissn'
    journals = set()

    # Extracting data from the DOAJ journals dump (May 7th, 2022)
    tar_journals = tarfile.open(path_to_DOAJ_journ_zip, "r:gz")
    for tarinfo in tar_journals:

        zip_file = tar_journals.extractfile(tarinfo)
        # Extracting the data in json format
        p = json.load(zip_file)

        for journal in p:
            # For every journal, extract only the info about issn and eissn. Through some tests, we verified that
            # there is always at least one of the two info for each record in the dump.
            try:
                if journal["bibjson"]["pissn"]:
                    journal_issn = journal["bibjson"]["pissn"]
            except KeyError:
                journal_issn = ""
            try:
                if journal["bibjson"]["eissn"]:
                    journal_eissn = journal["bibjson"]["eissn"]
            except KeyError:
                journal_eissn = ""

            # Creating our own unique identifier for each journal which is a concatenation of the issn and the eissn
            key_dict = f"{journal_issn}{journal_eissn}"

            journals.add(key_dict)

    print("number of journals: " + str(len(journals)))

    # Instantiating the data structure that will be stored in the JSON containing all of the dois of the articles for
    # each journal. It is of the form {"issnj1+eissnj1":{"title":title1, "issn":issnj1, "eissn":eissnj1,
    # "dois:["doi1", "doi2",...]"}, "issnj2+eissnj2":{"title":title2, "issn":issnj2, "eissn":eissnj2, "dois:["doi1",
    # "doi2",...]"}
    doi_json = {}

    # Storing the articles that don't have a doi and have been wrongly registered
    art_without_doi = []

    # Counting all of the articles
    num_art = 0
    # Extracting data from the DOAJ articles dump (May 1st, 2022)
    tar = tarfile.open(path_to_DOAJ_art_zip, "r:gz")
    for tarinfo in tar:

        z_file = tar.extractfile(tarinfo)
        # Extracting the data in json format
        p = json.load(z_file)
        for article in p:
            num_art += 1
            # Initializing the variables as empty strings for each iteration
            journal_issn = ""
            journal_eissn = ""
            art_doi = ""
            key_dict = ""
            journal_subject = ""

            # Collecting data for issn, eissn and doi for each article
            for el in article["bibjson"]["identifier"]:
                if el["type"] == "pissn":
                    journal_issn = el["id"]
                if el["type"] == "eissn":
                    journal_eissn = el["id"]
                if el["type"] == "doi" or el["type"] == "DOI":
                    try:
                        art_doi = el["id"]
                    # Some articles had an identifier of type doi registered without inserting the doi, which caused
                    # an error By setting the art_doi to an empty string, these articles will be added to the list of
                    # articles without dois.
                    except KeyError:
                        art_doi = ""

            # If the article doesn't have any doi registered, it is added to a list which will be later dumped to a
            # json "articles_without_doi.json"
            if art_doi == "":
                art_without_doi.append(article)
            else:

                # Collecting the title of the journal
                journal_title = article["bibjson"]["journal"]["title"]

                # Creating our own unique identifier for each journal
                key_dict = f"{journal_issn}{journal_eissn}"

                # Handling cases where the issn and/or eissn from the articles dump don't match the journals dump
                if key_dict not in journals:

                    # Aligning with the journals metadata if there is only the issn registered
                    if journal_issn in journals:
                        key_dict = journal_issn
                    # Aligning with the journals metadata if there is only the eissn registered
                    elif journal_eissn in journals:
                        key_dict = journal_eissn
                    else:
                        # In case the articles metadata has only one of the 2 identifiers, we check on all of the
                        # journals identifiers if the string contains the (e)issn held in the article metadata
                        for issn in journals:
                            if journal_issn != "" and journal_issn in issn:
                                key_dict = issn
                                break
                            elif journal_eissn != "" and journal_eissn in issn:
                                key_dict = issn
                                break

                journal_subject = article["bibjson"]["subject"]
                # Once all of the information are collected, we add them to our final json, adding a new key if it
                # doesn't exist or adding it to the list of dois for the journal
                if key_dict in doi_json:
                    doi_json[key_dict]["dois"].append(art_doi)
                else:
                    doi_json[key_dict] = {"title": journal_title, "pissn": journal_issn, "eissn": journal_eissn,
                                          "dois": [art_doi], "subject": journal_subject}

    print("number of journals that have articles with dois: " + str(len(doi_json)))
    print("number of articles that don't have a doi: " + str(len(art_without_doi)))
    print("total number of articles processed: " + str(num_art))

    # Save a json file with all journals and DOIs
    with open('./data/queried/DOAJ/doi.json', 'w', encoding='utf8') as json_file:
        json.dump(doi_json, json_file, ensure_ascii=False)

    # Save a json file with the articles that don't have a DOI
    with open('./data/queried/DOAJ/articles_without_doi.json', 'w', encoding='utf-8') as json_file2:
        json.dump(art_without_doi, json_file2, ensure_ascii=False)
