import openai
from problem_definer import Problem, ProntoQA, FOLIO, ProofWriter, LogicalDeduction
from typing import Tuple


def create_problem(dataset_name: str) -> Problem:
    if dataset_name == "ProntoQA":
        return ProntoQA()
    elif dataset_name == "FOLIO":
        return FOLIO()
    elif dataset_name == "ProofWriter":
        return ProofWriter()
    elif dataset_name == "LogicalDeduction":
        return LogicalDeduction()
    else:
        raise Exception("Name is not defined")


def parse_dataset_str(dataset_name: str) -> Tuple[str, str, str, str]:
    problem = create_problem(dataset_name)
    dataset_path = problem.dataset_path
    few_shot_prompt = problem.prompt
    answer_save_path = problem.answer_save_path
    program_save_path = problem.program_save_path
    return dataset_path, few_shot_prompt, answer_save_path, program_save_path


def make_message(content, role):
    if role == "user":
        return {"role": "user", "content": content}
    if role == "system":
        return {"role": "system", "content": content}
    if role == "assistant":
        return {"role": "assistant", "content": content}
    if role == "":
        return


def prepare_prompt(sys_message, conversation):
    messages = [make_message(sys_message, "system")]
    for i, msg in enumerate(conversation):
        if i % 2 == 0:
            messages.append(make_message(msg, "user"))
        else:
            messages.append(make_message(msg, "assistant"))
    return messages


def call_openai_api(messages, model="gpt-3.5-turbo", temperature=0) -> str:
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=temperature
    )
    token_used = response["usage"]["total_tokens"]
    return response["choices"][0]["message"]["content"], token_used
