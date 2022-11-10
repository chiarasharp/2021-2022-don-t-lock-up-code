import os
import sys

input_directory = sys.argv[1]

with open(sys.argv[1], "r") as f:
    for line in f.readlines():
        try:
            key, value = line.split('=')
            os.environ[key] = value
        except ValueError:
            # syntax error
            pass