import json
import os
import logging
import sys

def read_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def save_program(returned_program):
    with open("toy_z3/file/program.json", "w") as f:
         json.dump(returned_program, f, indent=2, ensure_ascii=False)

def save_answer(returned_answer):
    with open("toy_z3/file/answer.json", "w") as f:
         json.dump(returned_answer, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    file_path = "datasets/ProntoQA.json"
    logging.info(f"the current path is {os.getcwd()}")
    f1 = read_json(file_path)

    print(f1[0])