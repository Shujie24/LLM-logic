import openai
import re
ITERATION_NUM = 10

def parse_program(program_list) -> list:
    pass

def parse_and_execute_program(program: str) -> str:
    prompt = f"""Execute this z3 python script, and give answer A for True, and B for False: {program}"""
    response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[{"role": "user", "content": prompt}])
    # return_dict = {}
    # return_dict["number"] = program_list[i]["id"]
    return refine_answer(response["choices"][0]["message"]["content"])
    # return_dict["answer"] = program_list[i]["answer"]
    # print(response["choices"][0]["message"]["content"])
    # return return_dict

def refine_answer(answer: str) -> str:
    A_pattern = r"[!@#%^&*()_+\-=[]{}|;':\",./<>?~`]*A[!@#%^&*()_+\-=[]{}|;':\",./<>?~`]*"
    B_pattern = r"[!@#%^&*()_+\-=[]{}|;':\",./<>?~`]*B[!@#%^&*()_+\-=[]{}|;':\",./<>?~`]*"
    if answer == "A" or ("A" in answer and "B" not in answer) or (re.search(answer, A_pattern) and not re.search(answer, B_pattern)):
        return "A"
    elif answer == "B" or"B" in answer and "A" not in answer or (re.search(answer, B_pattern) and not re.search(answer, A_pattern)):
        return "B"
    else:
        return "None"