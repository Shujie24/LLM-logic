import json
import os
import logging
import sys


def read_json(filename, start, end):
    with open(filename, "r") as f:
        return json.load(f)[start:end]


# def save_program(returned_program):
#     with open("toy_z3/file/program.json", "w") as f:
#          json.dump(returned_program, f, indent=2, ensure_ascii=False)


def save_program(new_data, filename):
    # Check if file exists and has content
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(new_data)

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def save_answer(returned_answer, file_path):
    with open(file_path, "w") as f:
        json.dump(returned_answer, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    file_path = "datasets/ProntoQA.json"
    logging.info(f"the current path is {os.getcwd()}")
    f1 = read_json(file_path)

    print(f1[0])
