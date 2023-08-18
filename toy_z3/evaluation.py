class Evaluator():
    def __init__(self, answer_list):
        self.answer_list = answer_list

    def evaluation(self) -> float:
        correct = 0
        total = len(self.answer_list)
        for i in range(total):
            if self.answer_list[i]["prediction"] == self.answer_list[i]["answer"]:
                correct += 1
        print(f"The accuracy of the dataset is {correct / total}")
        return correct / total