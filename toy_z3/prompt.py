PROMPT = """
Task Description: You are given a problem description and a question. The task is to write a python script which includes: 
1) Define all variables for all entities in the problem
2) Create a solver instance
3) Parse the problem into relationships based on the defined entities, you should only use `Implies` and `Not` in this part
4) Create facts in the problem
4) Create statements to be checked
5) Check if the solver can find a model that satisfies the conditions, if true, return A, if false, return B

Following is an example to follow:
Problem:
Every zumpus is aggressive. Zumpuses are Wumpuses. Wumpuses are not small. Polly is zumpus,
[Question]:
Is the following statement true or false? Polly is not small.

```python
from z3 import * 

# Define boolean variables for all entities
zumpus = Bool("zumpus")
aggressive = Bool('aggressive')
wumpus = Bool('wumpus')
small = Bool("small")
polly = Bool("polly")

# Create a solver instance
solver = Solver()

# Parse the problem into relationships
solver.add(Implies(zumpus, aggressive))
solver.add(Implies(zumpus, wumpus))
solver.add(Implies(wumpus, Not(small)))
solver.add(Implies(polly, zumpus))

# Create facts in the problem
solver.add(polly)

# Create statements to be checked
solver.add(polly, Not(small))

# Check if the solver can find a model that satisfies the conditions
if solver.check() == sat:
    print("A")  # The statement is true
else:
    print("B")  # The statement is false
```
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[Problem]:
%s
Question:
%s
"""


INSTRUCTION_PROMPT = f"""
You should write in the format as comment in python script as follows:
Define boolean variables for all entities: <the entities you generate> \\ 
Create a solver instance: `solver = Solver()`
Parse the problem into relationships: <Relationships you generate> \\
Fact: <Fact you generate> \\
Create statements to be checked: <Statements to be checked>\\
Check if satisfy the condition: print A if the statement is true and B if the statement is false.

You must meet the following requirements:
1. The output should be a python script of the format ```python <code generate> ```
2. All boolen variables should be defined.
3. Number of Relationships you generate should be the same as number of sentences in the [Problem](A sentence is defined as ending with ".").
"""


