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
    parser.add_argument("start", type=int, help="starting index of data", default=0)
    parser.add_argument("end", type=int, help="ending index of data", default=10)
    args = parser.parse_args()
    file_path, openai.api_key, model_name, num_iteration, start, end = args.input_file_path, args.api_key, args.model_name, args.refinement_num_iteration, args.start, args.end
    print(file_path, openai.api_key, model_name, num_iteration)

    logging.info(f"the current path is {os.getcwd()}")
    dataset_list = read_json(file_path, start, end)
    answer_list = []
    total_token = 0
    for i, data in enumerate(dataset_list):
        answer_generator = AnswerGenerator(data, num_iteration, model_name)
        prediction, token_used = answer_generator.generate_answer()
        total_token += token_used
        print(prediction)
        answer_dict = answer_generator.parse_answer_file(prediction)
        answer_list.append(answer_dict)
    print(f"total tokens used is {total_token}")
    save_answer(answer_list)
    evatuator = Evaluator(answer_list)
    evatuator.evaluation()


if __name__ == "__main__":
    main()


    # python toy_z3/main.py  "datasets/ProntoQA.json" "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" 10