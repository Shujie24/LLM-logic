from input_output import read_json, save_program, save_answer
from generate_program import AnswerGenerator
from evaluation import Evaluator

import openai
import logging
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Arguments for z3 model.")
    parser.add_argument("input_file_path",type=str,help="Input file path")
    parser.add_argument("api_key", type=str, help="Api key")
    parser.add_argument("--model_name", type=str, help="Model name of OpenAI API", default="gpt-3.5-turbo")
    parser.add_argument("--refinement_num_iteration", type=int, help="Number of iterations for self-refinement", default=4)
    args = parser.parse_args()
    file_path, openai.api_key, model_name, num_iteration = args.input_file_path, args.api_key, args.model_name, args.refinement_num_iteration
    print(file_path, openai.api_key, model_name, num_iteration)

    logging.info(f"the current path is {os.getcwd()}")
    dataset_list = read_json(file_path)
    answer_list = []
    for i, data in enumerate(dataset_list):
        answer_generator = AnswerGenerator(data, num_iteration, model_name)
        prediction = answer_generator.generate_answer()
        print(prediction)
        answer_dict = answer_generator.parse_answer_file(prediction)
        answer_list.append(answer_dict)
    save_answer(answer_list)
    evatuator = Evaluator(answer_list)
    evatuator.evaluation()


if __name__ == "__main__":
    main()


    # python toy_z3/main.py  "datasets/ProntoQA_small.json" "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"