import os


def take_env_variables(path):
    dict_variable = dict()
    with open(path, "r") as f:
        for line in f.readlines():
            try:
                key, value = line.split('=')
                dict_variable[key] = value.strip()

            except ValueError:
                # syntax error
                pass

    return dict_variable

