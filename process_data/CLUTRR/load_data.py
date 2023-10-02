from datasets import load_dataset
from pathlib import Path
import json
import os

def create_context(story, gender):
    return "Story: " + story + '\n' + "Gender: " + gender + '\n'

def create_question(query):
    que = f'What is the relation between {query[0]} and {query[1]}?'


if __name__ == "__main__":
    for type_ in ["gen_train23_test2to10", "gen_train234_test2to10", "rob_train_clean_23_test_all_23", "rob_train_sup_23_test_all_23",
                  "rob_train_irr_23_test_all_23", "rob_train_disc_23_test_all_23"]:
        for task in ['train', 'validation', 'test']:
            dataset = load_dataset("CLUTRR/v1", type_, split=task).to_pandas()
            dataset['context'] = dataset.apply(lambda x: create_context(story=x['story'], gender=x['genders']), axis=1)
            dataset['clear_context'] = dataset.apply(lambda x: create_context(story=x['clean_story'], gender=x['genders']), axis=1)
            dataset['question'] = dataset.apply(lambda x: create_question(query=x['query']), axis=1)
            
            output_dir = os.makedirs(Path('/ssd005/projects/LLM-reasoning/Sophie/LLM-logic/datasets/CLUTRR') / type_, exist_ok=True)
            output_path = os.path.join(Path('/ssd005/projects/LLM-reasoning/Sophie/LLM-logic/datasets/CLUTRR') / type_,  f'{task}.json')
            dataset[["context", "clear_context", "question", "target",
                    "target_text"]].to_json(output_path,
                                            lines=True,
                                            orient='records')