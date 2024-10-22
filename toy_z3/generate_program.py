import logging
import json
from util import *
from io import StringIO
from contextlib import redirect_stdout
from input_output import save_program


class AnswerGenerator:
    def __init__(
        self,
        data,
        num_iteration,
        model_name,
        few_shot_prompt,
        instruction_prompt,
        program_save_path,
        choice,
    ):
        self.data = data
        self.num_iteration = num_iteration
        self.model_name = model_name
        self.few_shot_prompt = few_shot_prompt
        self.instruction_prompt = instruction_prompt
        self.program_save_path = program_save_path
        self.choice = choice

    def generate_answer(self) -> str:
        """Given the dataset, generate an executable z3 program by calling OpenAI API. Includes iterative process of error handling."""
        # step:
        # for num of iteration:
        # 1. prepare all prompts
        # 2. call openai api and generate the program
        # 3. check if the program can be executed
        # 4.if does, execute the program and return the answer
        #   if not, add execute error message as assistant and in the loop again
        # 5. return the final answer(answer or null)
        conversation = []
        total_tokens = 0
        for j in range(self.num_iteration):
            context, question, options, answer, id_ = (
                self.data["context"],
                self.data["question"],
                self.data["options"],
                self.data["answer"],
                self.data["id"],
            )
            user_prompt = self.few_shot_prompt % (context, question, options)
            conversation.append(user_prompt)
            prompt = prepare_prompt(self.instruction_prompt, conversation)
            try:
                response, token_used = call_openai_api(prompt, self.model_name)
                total_tokens += token_used
            except Exception as e:
                if "Please reduce the length of the messages." in str(e):
                    return (f"None, max token used", total_tokens)
                else:
                    raise e
            print(response)
            program_dict = {
                "id": id_,
                "context": context,
                "question": question,
                "options": options,
                "program": response,
                "answer": answer,
            }
            save_program(program_dict, self.program_save_path)
            response = self.parse_response(response)
            executable, prediction = self.check_execution(response)
            if executable:
                return prediction, total_tokens
            else:
                output = f"There is error when using code: {response}, and the error message: {prediction}"
                print(output)
                conversation.append(output)
        return (f"None, {output}", total_tokens)

    def parse_response(self, response: str) -> str:
        """parse the response to an executable program"""
        code_begin = "```python"
        code_end = "```"
        res = response.split(code_begin)
        if len(res) > 1:
            return res[1].split(code_end)[0]
        return None

    def check_execution(self, code: str):
        f = StringIO()
        global_vars = {}
        try:
            with redirect_stdout(f):
                exec(code, global_vars)
        except Exception as e:
            outputs = str(e)
            return False, outputs
        outputs = "".join(f.getvalue().split())  # get rid of "\n"
        if outputs not in self.choice:
            return False, f"Output format is not choices: {self.choice} : " + outputs
        else:
            return True, outputs

    def parse_answer_file(self, prediction) -> dict:
        return_dict = {}
        return_dict["id"] = self.data["id"]
        return_dict["prediction"] = prediction
        return_dict["answer"] = self.data["answer"]
        return return_dict


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
