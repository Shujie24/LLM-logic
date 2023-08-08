PROMPT = """
Task Description: You are given a problem description and a question. The task is to: 
1) define all the variables for properties in the problem
2) define all variables for entities in the problem
3) parse the problem into relationships and properties based on the defined variables and entities
4) write all the facts mentioned in the problem

Problem:
Every zumpus is aggressive. Zumpuses are yumpuses. Wumpuses are not small. Each yumpus is not luminous. Every yumpus is a jompus. Jompuses are orange. Jompuses are numpuses. Each numpus is earthy. Each numpus is a rompus. Rompuses are not sweet. Each rompus is a vumpus. Every vumpus is bright. Each vumpus is a dumpus. Each dumpus is small. Dumpuses are tumpuses. Every tumpus is cold. Every tumpus is an impus. Polly is a jompus.",
Question:
Is the following statement true or false? Polly is not small.

Variables for properties: 
Aggressive = Bool('Aggressive')
Luminous = Bool('Luminous')
Orange = Bool('Orange')
Earthy = Bool('Earthy')
Sweet = Bool('Sweet')
Bright = Bool('Bright')
Small = Bool('Small')
Cold = Bool('Cold')

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

Fact:
Polly_implies_Small = Implies(Polly, True)

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Problem:
%s
Question:
%s
"""


INSTRUCTION_PROMPT = f"""
You should write in the format as follows:
Variables for properties: <the property variables you generate> \\ 
Variables for entities: <the entities variables you generate> \\ 
Relationships: <Relationships you generate> \\
Fact: <Fact you generate> 
"""


