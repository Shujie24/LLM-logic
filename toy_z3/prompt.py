# from generator import Generator
from load_dataset import read_json
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
        prompt = f"""
        You are given a problem: {context}. The question is {question}, and you are given these options: {options}.
        """
        print(prompt)
        response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt},
                {"role": "user", "content": f"{FEW_SHOT_PROMPT}. Don't give extra words, just give the python script."}])
        response_list.append(response)
    return response_list

if __name__ == "__main__":
    file_path = "datasets/ProntoQA_small.json"
    openai.api_key = "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"
    logging.info(f"the current path is {os.getcwd()}")
    dataset_list = read_json(file_path)
    print(dataset_list[1])
    response_list = generate_results(dataset_list)
    print(response_list)

        

        
        
