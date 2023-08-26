import json

if __name__ == "__main__":
    file_name = "datasets/ProofWriter.json"
    output_file = "datasets/ProofWriter.json"
    with open(file_name, "r") as f:
        lst = json.load(f)
    return_lst = []
    idx_lst = []
    dup_num = 0
    total = 0
    for (i, dic) in enumerate(lst):
        total += 1
        if dic["context"] in idx_lst:
            dup_num += 1
        else:
            idx_lst.append(dic["id"])
            dic["id_extend"] = dic["id"]
            dic["id"] = f"ProofWriter_{i+1}"
            return_lst.append(dic)
    print(f"total number of duplicates is {dup_num}, total num is {total}, duplicate proportion is {dup_num / total}")

    with open(output_file, "w") as f:
        json.dump(return_lst, f, indent=2, ensure_ascii=False)
