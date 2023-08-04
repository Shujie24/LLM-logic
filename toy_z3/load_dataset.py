import json
import os
import logging
import sys

def read_json(filename):
    with open(filename, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    file_path = "datasets/ProntoQA.json"
    logging.info(f"the current path is {os.getcwd()}")
    f1 = read_json(file_path)

    print(f1[0])