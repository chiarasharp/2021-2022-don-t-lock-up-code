import sys

input_directory = sys.argv[1]
output_directory = sys.argv[2]


with open("../../.env", "w") as f:
    f.write(f"input_directory={input_directory}\n")
    f.write(f"output_directory={output_directory}")
