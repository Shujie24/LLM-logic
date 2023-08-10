def evaluation(answer_list: list) -> list:
    correct = 0
    total = len(answer_list)
    for i in range(len(answer_list)):
        if answer_list[i]["prediction"] == answer_list[i]["answer"]:
            correct += 1
    print(f"The accuracy of the dataset is {correct / total}")
    return correct / total