from prompt import (
    PROMPT_PRONTOQA,
    PROMPT_PROOFWRITER,
    PROMPT_FOLIO,
    PROMPT_LOGICALDEDUCTION,
    INSTRUCTION_PROMPT_PRONTOQA,
    INSTRUCTION_PROMPT_PROOFWRITER,
    INSTRUCTION_PROMPT_FOLIO,
    INSTRUCTION_PROMPT_LOGICALDEDUCTION,
)


class Problem:
    pass


class ProntoQA(Problem):
    def __init__(self):
        self.dataset_path = "datasets/ProntoQA.json"
        self.prompt = PROMPT_PRONTOQA
        self.answer_save_path = "output_file/ProntoQA_answer.json"
        self.program_save_path = "output_file/ProntoQA_program.json"
        self.instruction_prompt = INSTRUCTION_PROMPT_PRONTOQA
        self.choice = ["A", "B"]


class FOLIO(Problem):
    def __init__(self):
        self.dataset_path = "datasets/FOLIO.json"
        self.prompt = PROMPT_FOLIO
        self.instruction_prompt = INSTRUCTION_PROMPT_FOLIO
        self.answer_save_path = "output_file/FOLIO_answer.json"
        self.program_save_path = "output_file/FOLIO_program.json"
        self.choice = ["A", "B", "C"]


class ProofWriter(Problem):
    def __init__(self):
        self.dataset_path = "datasets/ProofWriter.json"
        self.prompt = PROMPT_PROOFWRITER
        self.answer_save_path = "output_file/ProofWriter_answer.json"
        self.program_save_path = "output_file/ProofWriter_program.json"
        self.instruction_prompt = INSTRUCTION_PROMPT_PROOFWRITER
        self.choice = ["A", "B", "C"]


class LogicalDeduction(Problem):
    def __init__(self):
        self.dataset_path = "datasets/LogicalDeduction.json"
        self.prompt = PROMPT_LOGICALDEDUCTION
        self.answer_save_path = "output_file/LogicalDeduction_answer.json"
        self.program_save_path = "output_file/LogicalDeduction_program.json"
        self.instruction_prompt = INSTRUCTION_PROMPT_LOGICALDEDUCTION
        self.choice = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
