########################################################################################
#################################    ProntoQA    #######################################
########################################################################################
PROMPT_PRONTOQA = """
Task Description: You are given a problem description and a question. The task is to write a python script which includes: 
1) Define all variables for all entities in the problem. You should write a comment indicating which sentence the entity is in,and if the entity has been defined before, also write a comment indicating it has been defined and not define the entity again.
2) Create a solver instance
3) Parse the problem into relationships based on the defined entities, you should only use `Implies` and `Not` in this part. You should write a comment indicating which sentence the relationship is in.
4) Create statements to be checked. You shoud write a comment indicating the statement.
5) Check if the solver can find a model that satisfies the conditions, if true, return A, if false, return B

Following is an example to follow:
Problem:
Every zumpus is aggressive. Zumpuses are Wumpuses. Wumpuses are not small. Wumpuses are aggressive. Polly is zumpus. 
Question:
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
[Question]:
%s
"""

INSTRUCTION_PROMPT_PRONTOQA = f"""
You should write in the format as comment in python script as follows:
Define boolean variables for all entities: <the entities you generate> 
Create a solver instance: `solver = Solver()`
Parse the problem into relationships: <Relationships you generate> 
Create statements to be checked: <Statements to be checked>
Check if satisfy the condition: print A if the statement is true and B if the statement is false

You must meet the following requirements:
1. The output should be a python script of the format ```python <code generate> ```
2. All boolen variables should be defined, and you should only define each variable once, not multiple times.
3. Number of Relationships you generate should be the same as number of sentences in the [Problem](A sentence is defined as ending with ".").
"""
########################################################################################
#################################    ProofWriter    ####################################
########################################################################################

PROMPT_PROOFWRITER = """
Task Description: You are given a problem description and a question. The task is to write a python script to translate the problem and question into executable z3 program. And the following are the steps: 
1) Declare a finite domain for entites and declare a fresh constant for universal quantification
1) Define all variables for all entities in the problem.
2) Define all predicates in the problem. 
3) Give facts. You should write a comment indicating which sentence it is before the fact you give.
4) Create solver and add facts to solver
5) Check if the solver can find a model that satisfies the conditions, if it is unsat then print B; if the statement is sat(you should be very careful about this part), remove this fact constraint from solver, print A is the statement is unsat and C is still sat


The following is an example: 
Problem:
Anne is quiet. Erin is furry. Erin is green. Fiona is furry. Fiona is quiet. Fiona is red. Fiona is rough. Fiona is white. Harry is furry. Harry is quiet. Harry is white. Young people are furry. If Anne is quiet then Anne is red. Young, green people are rough. If someone is green then they are white. If someone is furry and quiet then they are white. If someone is young and white then they are rough. All red people are young.
Question:
Based on the above information, is the following statement true, false, or unknown? Anne is white.

```python
from z3 import *

# Declare a finite domain sort for the entities
Entity = DeclareSort('Entity')
# Declare a fresh constant for universal quantification
x = Const('x', Entity)


# Declare the entities
# Anne = Const('Anne', Entity)
Erin = Const('Erin', Entity)
Fiona = Const('Fiona', Entity)
Harry = Const('Harry', Entity)
Anne = Const('Anne', Entity)

# Declare the predicates
Quiet = Function('Quiet', Entity, BoolSort())
Furry = Function('Furry', Entity, BoolSort())
Green = Function('Green', Entity, BoolSort())
Red = Function('Red', Entity, BoolSort())
Rough = Function('Rough', Entity, BoolSort())
White = Function('White', Entity, BoolSort())
Young = Function('Young', Entity, BoolSort())


# Define all facts
facts = [
    # Facts about individuals
    # Anne is quiet.
    Quiet(Anne),
    # Erin is furry.
    Furry(Erin),
    # Erin is green.
    Green(Erin),
    # Fiona is furry.
    Furry(Fiona),
    # Fiona is quiet.
    Quiet(Fiona),
    # Fiona is red.
    Red(Fiona),
    # Fiona is rough.
    Rough(Fiona),
     # Fiona is white.
    White(Fiona),
    # Harry is furry.
    Furry(Harry),
    # Harry is quiet.
    Quiet(Harry),
    # Harry is white.
    White(Harry),
    # Facts about conditions
    # Young people are furry.
    ForAll([x], Implies(Young(x), Furry(x))),
    # If Anne is quiet then Anne is red.
    Implies(Quiet(Anne), Red(Anne)),
    # Green people are rough.
    ForAll([x], Implies(Green(x), Rough(x))),
    # If someone is green then they are white. 
    ForAll([x], Implies(Green(x), White(x))),
    # If someone is furry and quiet then they are white. 
    ForAll([x], Implies(And(Furry(x), Quiet(x)), White(x))),
    # If someone is young and white then they are rough.
    ForAll([x], Implies(And(Young(x), White(x)), Rough(x))),
    #  All red people are young.
    ForAll([x], Implies(Red(x), Young(x)))
]
# Create a solver instance
solver = Solver()
solver.add(facts)

# add problem to solver
solver.push()
solver.add(White(Anne))
if solver.check() == sat:
    solver.pop()
    solver.add(Not(White(Anne)))
    if solver.check() == sat:
        print("C")  # The statement is unknown(C) when sat
    else:
        print("A") # The statement is true(A) when unsat
else:
    print("B") # The statement is false(B)

```
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[Problem]:
%s
[Question]:
%s
"""


INSTRUCTION_PROMPT_PROOFWRITER = """
You should write in the format as comment in python script as follows:
Declare finite domain and universal quantifier: <domain and quantifier you define>
Define entities: <the entities you generate> 
Give facts:  <facts you generate> 
Create solver and add facts to solver: <create solver and add facts>
Check if satisfy the condition: if it is unsat then print B; if the statement is sat(you should be very careful about this part), remove this fact constraint from solver, print A is the statement is unsat and C is still sat


You must meet the following requirements:
1. The output should be a python script of the format ```python <code generate> ```
2. All boolen variables and all predicates should be defined, and you should only define each variable and predicate once, not multiple times.
3. All facts should be stated. Number of Facts you generate should be the same as number of sentences in the [Problem](A sentence is defined as ending with ".").
4. In the code, there must be an uncertain case for outputing C, other than just output A and B
5. You should only use these functions: Implies, Not, And, Function, BoolSort, Bool, Bools
6. In facts, don't use universal quantifier if each entity has already been defined.
"""

########################################################################################
#################################    FOLIO    ##########################################
########################################################################################
PROMPT_FOLIO = """
Task Description: You are given a problem description and a question. The task is to write a python script to translate the problem and question into executable z3 program. And the following are the steps: 
1) Declare a finite domain for entites and declare a fresh constant for universal quantification
1) Define all variables for all entities in the problem.
2) Define all predicates in the problem. 
3) Give facts. You should write a comment indicating which sentence it is before the fact you give.
4) Create solver and add facts to solver
5) Check if the solver can find a model that satisfies the conditions, if it is unsat then print B; if the statement is sat(you should be very careful about this part), remove this fact constraint from solver, print A is the statement is unsat and C is still sat

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[Problem]:
%s
[Question]:
%s
"""

INSTRUCTION_PROMPT_FOLIO = """"""
Placeholder = """
The following is an example: 
Problem:
If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, 
then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to further their academic careers and educational opportunities are 
students who attend the school. Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.
Question: Based on the above information, is the following statement true, false, or uncertain? Bonnie performs in school talent shows often.
"""
