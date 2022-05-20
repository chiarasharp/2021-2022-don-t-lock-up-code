"""
take in input two json file:
doi.json ---> {Journal: {all other information},
                ...}

general_count_dict.json ---> {Journal: {
                                "citing": 0,
                                "cited": 0,
                                "open_citing": 0,
                                open_cited": 0},
                                ...
                                }


"""


def final_merge(all_doi, count):
    new_dict = dict()
    list_dict = [all_doi, count]
    # Iterate over the two dict in input
    for listed_dict in list_dict:

        for journal_id, value in listed_dict.items():
            # if the key of the journal don't exist, add the key with as value a dict
            if journal_id not in new_dict:
                new_dict[journal_id] = dict()
            # if the key of the journal exist or after creating the new key, add inside this latter key
            # a new key of the other dict with the correspondent value
            for name_field, value_field in value.items():
                new_dict[journal_id][name_field] = value_field
    return new_dict
