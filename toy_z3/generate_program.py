from prompt import PROMPT, INSTRUCTION_PROMPT
import openai
import logging
import json
from util import *
from generate_answer import parse_and_execute_program
from input_output import save_program, save_answer
from input_output import read_json
from io import StringIO
from contextlib import redirect_stdout
from evaluation import evaluation

FEW_SHOT_PROMPT = """
Solve above problems by writing a Python program and using the Z3 library and the answer printing in the result should be either A for True or B for False
"""

def generate_program(data: dict, num_iteration) -> str:
    """Given the dataset, generate an executable z3 program by calling OpenAI API. Includes iterative process of error handling. """
    # step:
    # for num of iteration:
    # 1. prepare all prompts
    # 2. call openai api and generate the program
    # 3. check, if pass the check, this is the return value, break
    # 4. if not, add execute error message? requirement not satisfy message? as assistant and in the loop again
    # 5. return the final program
    conversation = []
    for j in range(num_iteration):
        context, question, options, answer, id_ = data["context"], data["question"], data["options"], data["answer"], data["id"]
        user_prompt = PROMPT % (context, question)
        conversation.append(user_prompt)
        prompt = prepare_prompt(INSTRUCTION_PROMPT, conversation)
        try:
            response = call_openai_api(prompt)
        except Exception as e:
            if "Please reduce the length of the messages." in str(e):
                conversation = conversation[2:]
                response = call_openai_api(prompt)
            else:
                print(str(e))
        print(response)
        program_dict = {"id": id_, "context": context, "question": question, "program": response, "answer": answer}
        save_program(program_dict)
        response = parse_response(response)
        executable, prediction = check_execution(response)
        if executable:
            return prediction
        else:
            conversation.append(f"There is error when using code: {response}, and the error message: {prediction}")
    return 
    

def parse_response(response: str) -> str:
    """parse the response to an executable program"""
    code_begin = "```python"
    code_end = "```"
    res = response.split(code_begin)
    if len(res) > 1:
        return res[1].split(code_end)[0]
    return None


def check_execution(code: str):
    f = StringIO()
    global_vars = {}
    try:
        with redirect_stdout(f):
            exec(code, global_vars)
    except Exception as e:
        outputs = str(e)
        return False, outputs
    outputs = "".join(f.getvalue().split()) # get rid of "\n"
    if outputs != "A" and outputs != "B":
        return False, "Output format is not A or B: " + outputs
    else:
        return True, outputs


if __name__ == "__main__":
    file_path = "datasets/ProntoQA_small.json"
    openai.api_key = "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"
    # logging.info(f"the current path is {os.getcwd()}")
    dataset_list = read_json(file_path)
    answer_list = []
    for i, data in enumerate(dataset_list):
        prediction = generate_program(data, 4)
        print(prediction)
        return_dict = {}
        return_dict["id"] = data["id"]
        return_dict["prediction"] = prediction
        return_dict["answer"] = data["answer"]
        answer_list.append(return_dict)
    save_answer(answer_list)
    evaluation(answer_list)
    # program_list = generate_program(dataset_list)
    # save_program(program_list)
    # # print(program_list)
    # answer_list = parse_and_execute_program(program_list)
    # save_answer(answer_list)
    # evaluation(answer_list)



        

        
        
