# from generator import Generator
from load_dataset import read_json
from prompt import PROMPT, INSTRUCTION_PROMPT
import openai
import logging
import os

FEW_SHOT_PROMPT = """
Solve above problems by writing a Python program and using the Z3 library:
"""

def generate_results(dataset_list) -> list:
    response_list = []
    for i in range(len(dataset_list)):
        data = dataset_list[i]
        context, question, options, answer = data["context"], data["question"], data["options"], data["answer"]
        full_prompt = PROMPT % (context, question)
        print(full_prompt)
        response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": full_prompt},
                {"role": "system", "content": INSTRUCTION_PROMPT}])
        response_list.append(response["choices"][0]["message"]["content"])
    return response_list

if __name__ == "__main__":
    file_path = "datasets/ProntoQA_small.json"
    openai.api_key = "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"
    logging.info(f"the current path is {os.getcwd()}")
    dataset_list = read_json(file_path)
    print(dataset_list[0])
    response_list = generate_results(dataset_list)
    print(response_list)

    prompt_solve = f"""Solve this problem with z3 solver: {response_list[0]}"""
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt_solve}])
    print(response["choices"][0]["message"]["content"])


        

        
        
