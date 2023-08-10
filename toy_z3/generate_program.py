# from generator import Generator
from load_dataset import read_json
from prompt import PROMPT, INSTRUCTION_PROMPT
import openai
import logging
import os
import json
import re

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
        {"role": "system", "content": "Then execute this python z3 script. The answer printing in the result should be either A for True or B for False"}],
        temperature = 0)
        return_dict = {}
        return_dict["id"] = id_
        return_dict["program"] = response["choices"][0]["message"]["content"]
        return_dict["answer"] = answer
        response_list.append(return_dict)
    return response_list

def parse_and_execute_program(program_list) -> list:
    answer_list = []
    for i in range(len(program_list)):
        prompt = f"""Execute this z3 python script, and give answer A for True, and B for False: {program_list[i]["program"]}"""
        response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}])
        return_dict = {}
        return_dict["number"] = program_list[i]["id"]
        return_dict["prediction"] = refine_answer(response["choices"][0]["message"]["content"])
        return_dict["answer"] = program_list[i]["answer"]
        print(response["choices"][0]["message"]["content"])
        answer_list.append(return_dict)
    return answer_list

def refine_answer(answer: str) -> str:
    A_pattern = r"[!@#%^&*()_+\-=[]{}|;':\",./<>?~`]*A[!@#%^&*()_+\-=[]{}|;':\",./<>?~`]*"
    B_pattern = r"[!@#%^&*()_+\-=[]{}|;':\",./<>?~`]*B[!@#%^&*()_+\-=[]{}|;':\",./<>?~`]*"
    if answer == "A" or ("A" in answer and "B" not in answer) or (re.search(answer, A_pattern) and not re.search(answer, B_pattern)):
        return "A"
    elif answer == "B" or"B" in answer and "A" not in answer or (re.search(answer, B_pattern) and not re.search(answer, A_pattern)):
        return "B"
    else:
        return "None"

def evaluation(answer_list: list) -> list:
    correct = 0
    total = len(program_list)
    for i in range(len(program_list)):
        if answer_list[i]["prediction"] == answer_list[i]["answer"]:
            correct += 1
    print(f"The accuracy of the dataset is {correct / total}")
    return correct / total
    


def save_program(parsed_program_list):
    with open("toy_z3/file/program.json", "w") as f:
         json.dump(parsed_program_list, f)

def save_answer(answer_list):
    with open("toy_z3/file/answer.json", "w") as f:
         json.dump(answer_list, f)

if __name__ == "__main__":
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
    

    # prompt_solve = f"""Solve this problem with z3 solver: {response_list[0]}"""
    # response = openai.ChatCompletion.create(
    #     model='gpt-3.5-turbo',
    #     messages=[{"role": "user", "content": prompt_solve}])
    # print(response["choices"][0]["message"]["content"])


        

        
        
