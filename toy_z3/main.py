from input_output import read_json, save_program, save_answer
from generate_program import generate_program
from generate_answer import parse_and_execute_program
from evaluation import evaluation

import openai
import logging
import os

def main():
    file_path = "datasets/ProntoQA_small.json"
    openai.api_key = "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"
    logging.info(f"the current path is {os.getcwd()}")
    dataset_list = read_json(file_path)
    program_list = generate_program(dataset_list)
    save_program(program_list)
    # print(program_list)
    answer_list = parse_and_execute_program(program_list)
    save_answer(answer_list)
    evaluation(answer_list)


if __name__ == "__main__":
    main()