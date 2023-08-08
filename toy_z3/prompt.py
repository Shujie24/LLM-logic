PROMPT = """
Task Description: You are given a problem description and a question. The task is to write a python script which includes: 
1) define all the variables for properties in the problem
2) define all variables for entities in the problem
3) parse the problem into relationships and properties based on the defined variables and entities
4) write all the facts mentioned in the problem

Problem:
Every zumpus is aggressive. Zumpuses are yumpuses. Wumpuses are not small. Each yumpus is not luminous. Every yumpus is a jompus. Jompuses are orange. Jompuses are numpuses. Each numpus is earthy. Each numpus is a rompus. Rompuses are not sweet. Each rompus is a vumpus. Every vumpus is bright. Each vumpus is a dumpus. Each dumpus is small. Dumpuses are tumpuses. Every tumpus is cold. Every tumpus is an impus. Polly is a jompus.",
Question:
Is the following statement true or false? Polly is not small.

```python
from z3 import * 

# Create solver object
solver = Solver()

# Variables for properties: 
Aggressive = Bool('Aggressive')
Luminous = Bool('Luminous')
Orange = Bool('Orange')
Earthy = Bool('Earthy')
Sweet = Bool('Sweet')
Bright = Bool('Bright')
Small = Bool('Small')
Cold = Bool('Cold')
variables = [Aggressive, Luminous, Orange, Earthy, Sweet, Bright, Small, Cold]
for v in variables:
    solver.add(v)


# Variables for entities
Zumpus = Bool('Zumpus')
Yumpus = Bool('Yumpus')
Wumpus = Bool('Wumpus')
Jompus = Bool('Jompus')
Numpus = Bool('Numpus')
Rompus = Bool('Rompus')
Vumpus = Bool('Vumpus')
Dumpus = Bool('Dumpus')
Tumpus = Bool('Tumpus')
Impus = Bool('Impus')
entities = [Zumpus, Yumpus, Wumpus, Jompus, Numpus, Rompus, Vumpus, Dumpus, Tumpus, Impus]
for e in entities:
    solver.add(e)

# Relationships
Zumpus_implies_Aggressive = Implies(Zumpus, True)
Zumpus_implies_Yumpuses = Implies(Zumpus, Yumpuses)
Wumpuse_implies_Small = Implies(Wumpuse, False)
Yumpus_implies_Luminous = Implies(Yumpus, False)
Yumpus_implies_Jompus = Implies(Yumpus, Jompus)
Jompuses_implies_Orange = Implies(Jompuses, True)
Jompuses_implies_Numpuses = Implies(Jompuses, Numpuses)
Numpus_implies_Earthy = Implies(Numpus, True)
Numpus_implies_Rompus = Implies(Numpus, Rompus)
Rompus_implies_Sweet = Implies(Rompus, False)
Rompus_implies_Vumpus = Implies(Rompus, Vumpus)
Vumpus_implies_Bright = Implies(Vumpus, True)
Vumpus_implies_Dumpus = Implies(Vumpus, Dumpus)
Dumpus_implies_Small = Implies(Dumpus, True)
Dumpuses_implies_Tumpuses = Implies(Dumpus, Tumpuses)
Tumpuses_implies_Cold = Implies(Tumpuses, True)
Tumpuses_implies_Impus = Implies(Tumpuses, Impus)
Polly_implies_Jompus = Implies(Polly, Jompus)

relationships = [Zumpus_implies_Aggressive, 
Zumpus_implies_Yumpuses,
Wumpuse_implies_Small,
Yumpus_implies_Luminous,
Yumpus_implies_Jompus,
Jompuses_implies_Orange,
Jompuses_implies_Numpusesm,
Numpus_implies_Earthy,
Numpus_implies_Rompus,
Rompus_implies_Sweet,
Rompus_implies_Vumpus,
Vumpus_implies_Bright,
Vumpus_implies_Dumpus,
Dumpus_implies_Small,
Dumpuses_implies_Tumpuses,
Tumpuses_implies_Cold,
Tumpuses_implies_Impus,
Polly_implies_Jompus]
for r in relationships:
    solver.add(r)

# Fact:
Polly_implies_Small = Implies(Polly, False)
facts = [Polly_implies_Small]
for f in facts:
    solver.add(f)

print(s.check(Polly_implies_Small))
```
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Problem:
%s
Question:
%s
"""


INSTRUCTION_PROMPT = f"""
You should write in the format as comment in python script as follows:
Variables for properties: <the property variables you generate> \\ 
Variables for entities: <the entities variables you generate> \\ 
Relationships: <Relationships you generate> \\
Fact: <Fact you generate> 
"""


