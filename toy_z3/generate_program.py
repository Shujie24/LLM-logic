# from generator import Generator
from load_dataset import read_json
from prompt import PROMPT, INSTRUCTION_PROMPT
import openai
import logging
import os
import json

FEW_SHOT_PROMPT = """
Solve above problems by writing a Python program and using the Z3 library and the answer printing in the result should be either A for True or B for False
"""

def generate_program(dataset_list) -> list:
    response_list = []
    for i in range(len(dataset_list)):
        data = dataset_list[i]
        context, question, options, answer, id_ = data["context"], data["question"], data["options"], data["answer"], data["id"]
        full_prompt = PROMPT % (context, question)
        # print(full_prompt)
        # response = openai.ChatCompletion.create(
        # model='gpt-3.5-turbo',
        # messages=[{"role": "user", "content": full_prompt},
        #         {"role": "system", "content": INSTRUCTION_PROMPT}])
        # response_list.append(response["choices"][0]["message"]["content"])
        response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": f"{FEW_SHOT_PROMPT} context: {context}, question: {question}"},
        {"role": "system", "content": "Then execute this python z3 script. The answer printing in the result should be either A for True or B for False"}])
        return_dict = {}
        return_dict["number"] = id_
        return_dict["program"] = response["choices"][0]["message"]["content"]
        return_dict["answer"] = answer
        response_list.append(return_dict)
    return response_list

def parse_and_execute_program(program_list) -> list:
    answer_list = []


def save_program(parsed_program_list):
    with open("program/toy.json", "w") as f:
         json.dump(parsed_program_list, f)

if __name__ == "__main__":
    file_path = "datasets/ProntoQA_small.json"
    openai.api_key = "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"
    logging.info(f"the current path is {os.getcwd()}")
    dataset_list = read_json(file_path)
    program_list = generate_program(dataset_list)
    print(program_list)
    save_program(program_list)

    # prompt_solve = f"""Solve this problem with z3 solver: {response_list[0]}"""
    # response = openai.ChatCompletion.create(
    #     model='gpt-3.5-turbo',
    #     messages=[{"role": "user", "content": prompt_solve}])
    # print(response["choices"][0]["message"]["content"])


        

        
        
