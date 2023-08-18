from input_output import read_json, save_program, save_answer
from generate_program import AnswerGenerator
from generate_answer import parse_and_execute_program
from evaluation import Evaluator

import openai
import logging
import os

def main():
    file_path = "datasets/ProntoQA_small.json"
    openai.api_key = "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"
    logging.info(f"the current path is {os.getcwd()}")
    dataset_list = read_json(file_path)
    answer_list = []
    for i, data in enumerate(dataset_list):
        answer_generator = AnswerGenerator(data, 4, "gpt-3.5-turbo")
        prediction = answer_generator.generate_answer()
        print(prediction)
        answer_dict = answer_generator.parse_answer_file(prediction)
        answer_list.append(answer_dict)
    save_answer(answer_list)
    evatuator = Evaluator(answer_list)
    evatuator.evaluation()


if __name__ == "__main__":
    main()