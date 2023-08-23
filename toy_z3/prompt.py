PROMPT = """
Task Description: You are given a problem description and a question. The task is to write a python script which includes: 
1) Define all variables for all entities in the problem. You should write a comment indicating which sentence the entity is in,and if the entity has been defined before, also write a comment indicating it has been defined and not define the entity again.
2) Create a solver instance
3) Parse the problem into relationships based on the defined entities, you should only use `Implies` and `Not` in this part. You should write a comment indicating which sentence the relationship is in.
4) Create statements to be checked. You shoud write a comment indicating the statement.
5) Check if the solver can find a model that satisfies the conditions, if true, return A, if false, return B

Following is an example to follow:
Problem:
Every zumpus is aggressive. Zumpuses are Wumpuses. Wumpuses are not small. Wumpuses are aggressive. Polly is zumpus. 
[Question]:
Is the following statement true or false? Polly is not small.

```python
from z3 import * 

# Define boolean variables for all entities
# Every zumpus is aggressive
zumpus = Bool("zumpus")
aggressive = Bool('aggressive') 

# Zumpuses are Wumpuses
# zumpus has been defined before
wumpus = Bool('wumpus') 

# Wumpuses are not small.
# Wumpuses has been defined before
small = Bool("small") 

# Wumpuses are aggressive.
# Wumpuses has been defined before
# Aggressive has been defined before

# Polly is zumpus.
polly = Bool("polly") 
# Zumpuses has been defined before

# Create a solver instance
solver = Solver()

# Parse the problem into relationships
# Every zumpus is aggressive
solver.add(Implies(zumpus, aggressive)) 
# Zumpuses are Wumpuses
solver.add(Implies(zumpus, wumpus))
# Wumpuses are not small
solver.add(Implies(wumpus, Not(small))) 
# Wumpuses are aggressive.
solver.add(Implies(wumpus, aggressive)) 
# Polly is zumpus
solver.add(Implies(polly, zumpus)) 

# Create facts in the problem
solver.add(polly)

# Create statements to be checked
# Polly is not small.
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
Define boolean variables for all entities: <the entities you generate> 
Create a solver instance: `solver = Solver()`
Parse the problem into relationships: <Relationships you generate> 
Fact: <Fact you generate> 
Create statements to be checked: <Statements to be checked>
Check if satisfy the condition: print A if the statement is true and B if the statement is false.

You must meet the following requirements:
1. The output should be a python script of the format ```python <code generate> ```
2. All boolen variables should be defined, and you should only define each variable once, not multiple times.
3. Number of Relationships you generate should be the same as number of sentences in the [Problem](A sentence is defined as ending with ".").
"""


