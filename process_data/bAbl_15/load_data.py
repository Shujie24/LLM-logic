from datasets import load_dataset
from pathlib import Path
import json


if __name__ == "__main__":
    for type_ in ["en-10k", "en", "en-valid-10k", "en-valid"]:
        for task_no in range(1, 21):
            dataset = load_dataset("babi_qa", type=f'{type_}', task_no=f'qa{task_no}')
            train_dataset = dataset['train']['story']
            test_dataset = dataset['test']['story']
            with open(Path('/ssd005/projects/LLM-reasoning/Sophie/LLM-logic/datasets/bAbl_15') /f'{type_}{task_no}_train.jsonl', 'w') as f:
                json.dump(train_dataset, f, indent=4)
            
            with open(Path('/ssd005/projects/LLM-reasoning/Sophie/LLM-logic/datasets/bAbl_15') /f'{type_}{task_no}_test.jsonl', 'w') as f2:
                json.dump(test_dataset, f2, indent=4)
            
            if 'validation' in dataset:
                val_dataset = dataset['validation']['story']
                with open(Path('/ssd005/projects/LLM-reasoning/Sophie/LLM-logic/datasets/bAbl_15') /f'{type_}{task_no}_val.jsonl', 'w') as f3:
                    json.dump(val_dataset, f3, indent=4)
            
            #     val.save_to_disk(Path('/ssd005/projects/LLM-reasoning/Sophie/LLM-logic/datasets')/f'{type_}{task_no}_val.jsonl')
                    
            # train_dataset.save_to_disk(Path('/ssd005/projects/LLM-reasoning/Sophie/LLM-logic/datasets') /f'{type_}{task_no}_train.jsonl')
            # test_dataset.save_to_disk(Path('/ssd005/projects/LLM-reasoning/Sophie/LLM-logic/datasets') / f'{type_}{task_no}_test.jsonl')