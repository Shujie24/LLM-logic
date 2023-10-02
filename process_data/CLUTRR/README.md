## Dataset Card for CLUTRR
## Dataset Description
## Dataset Summary
CLUTRR (Compositional Language Understanding and Text-based Relational Reasoning), a diagnostic benchmark suite, is first introduced in (https://arxiv.org/abs/1908.06177) to test the systematic generalization and inductive reasoning capabilities of NLU systems.

The CLUTRR benchmark allows us to test a model’s ability for systematic generalization by testing on stories that contain unseen combinations of logical rules, and test for the various forms of model robustness by adding different kinds of superfluous noise facts to the stories.

## Dataset Task
CLUTRR contains a large set of semi-synthetic stories involving hypothetical families. The task is to infer the relationship between two family members, whose relationship is not explicitly mentioned in the given story.

Join the CLUTRR community in https://www.cs.mcgill.ca/~ksinha4/clutrr/

## Dataset Structure
We show detailed information for all 14 configurations of the dataset.

## configurations:
id: a unique series of characters and numbers that identify each instance
story: one semi-synthetic story involving hypothetical families
query: the target query/relation which contains two names, where the goal is to classify the relation that holds between these two entities
target: indicator for the correct relation for the query
target_text: text for the correct relation for the query
the indicator follows the rule as follows:
"aunt": 0, "son-in-law": 1, "grandfather": 2, "brother": 3, "sister": 4, "father": 5, "mother": 6, "grandmother": 7, "uncle": 8, "daughter-in-law": 9, "grandson": 10, "granddaughter": 11, "father-in-law": 12, "mother-in-law": 13, "nephew": 14, "son": 15, "daughter": 16, "niece": 17, "husband": 18, "wife": 19, "sister-in-law": 20
clean_story: the story without noise factors
proof_state: the logical rule of the kinship generation
f_comb: the kinships of the query followed by the logical rule
task_name: the task of the sub-dataset in a form of "task_[num1].[num2]"
The first number [num1] indicates the status of noise facts added in the story: 1- no noise facts; 2- Irrelevant facts*; 3- Supporting facts*; 4- Disconnected facts*.
The second number [num2] directly indicates the length of clauses for the task target.
for example:
task_1.2 -- task requiring clauses of length 2 without adding noise facts
task_2.3 -- task requiring clauses of length 3 with Irrelevant noise facts added in the story
story_edges: all the edges in the kinship graph
edge_types: similar to the f_comb, another form of the query's kinships followed by the logical rule
query_edge: the corresponding edge of the target query in the kinship graph
genders: genders of names appeared in the story
task_split: train,test

*Further explanation of Irrelevant facts, Supporting facts and Disconnected facts can be found in the 3.5 Robust Reasoning section in https://arxiv.org/abs/1908.06177

