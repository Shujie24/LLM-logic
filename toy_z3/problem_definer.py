from prompt import PROMPT_PRONTOQA


class Problem:
    pass


class ProntoQA(Problem):
    def __init__(self):
        self.dataset_path = "datasets/ProntoQA.json"
        self.prompt = PROMPT_PRONTOQA
        self.answer_save_path = "output_file/ProntoQA_answer.json"
        self.program_save_path = "output_file/ProntoQA_program.json"


class FOLIO(Problem):
    def __init__(self):
        self.dataset_path = "datasets/FOLIO.json"
        self.prompt = PROMPT_FOLIO
        self.answer_save_path = "output_file/FOLIO_answer.json"
        self.program_save_path = "output_file/FOLIO_program.json"


class ProofWriter(Problem):
    pass


class LogicalDeduction(Problem):
    pass
