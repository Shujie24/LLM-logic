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
Options: 
A, B

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
[Options]:
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
2) Define all variables for all entities in the problem.
3) Define all predicates in the problem. 
4) Give facts. You should write a comment indicating which sentence it is before the fact you give.
5) Create solver and add facts to solver
6) Check if the solver can find a model that satisfies the conditions, if it is unsat then print B; if the statement is sat(you should be very careful about this part), remove this fact constraint from solver, print A is the statement is unsat and C is still sat


The following is an example: 
Problem:
Anne is quiet. Erin is furry. Erin is green. Fiona is furry. Fiona is quiet. Fiona is red. Fiona is rough. Fiona is white. Harry is furry. Harry is quiet. Harry is white. Young people are furry. If Anne is quiet then Anne is red. Young, green people are rough. If someone is green then they are white. If someone is furry and quiet then they are white. If someone is young and white then they are rough. All red people are young.
Question:
Based on the above information, is the following statement true, false, or unknown? Anne is white.
Options:
A, B, C

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
[Options]: 
%s
"""


INSTRUCTION_PROMPT_PROOFWRITER = """
You should write in the format as comment in python script as follows:
Declare finite domain and universal quantifier: <domain and quantifier you define>
Define entities: <the entities you generate> 
Declare the predicates: <the predicates you generate> 
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
# PROMPT_FOLIO = """
# Task Description: You are given a problem description and a question. The task is to write a python script to translate the problem and question into executable z3 program. And the following are the steps:
# 1) Declare a finite domain for entites and declare a fresh constant for universal quantification
# 2) Define all predicates in the problem.
# 3) Define all variables for all entities in the problem.
# 4) Give facts. You should write a comment indicating which sentence it is before the fact you give.
# 5) Create solver and add facts to solver
# 6) Check if the solver can find a model that satisfies the conditions, if it is unsat then print B; if the statement is sat(you should be very careful about this part), remove this fact constraint from solver, print A is the statement is unsat and C is still sat

# Problem:
# If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, then they
# are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to further their academic careers and educational opportunities are students who
# attend the school. Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school."
# Question:
# Based on the above information, is the following statement true, false, or uncertain? Bonnie performs in school talent shows often.

# ```python
# from z3 import *

# # Declare a finite domain sort for the entities
# Entity = DeclareSort('Entity')
# # Declare a fresh constant for universal quantification
# x = Const('x', Entity)

# # Declare the predicates
# PerformInSchoolTalentShowsOften = Function('PerformInSchoolTalentShowsOften', Entity, BoolSort())
# AttendAndEngagedWithSchoolEvents = Function('AttendAndEngagedWithSchoolEvents', Entity, BoolSort())
# InactiveAndDisinterestedMemberOfCommunity = Function('InactiveAndDisinterestedMemberOfCommunity', Entity, BoolSort())
# ChaperoneHighSchoolDances = Function('ChaperoneHighSchoolDances', Entity, BoolSort())
# StudentAttendSchool = Function('StudentAttendSchool', Entity, BoolSort())
# TeenagerWishToFurtherAcademicCareersAndEducationalOpportunities = Function('TeenagerWishToFurtherAcademicCareersAndEducationalOpportunities', Entity, BoolSort())

# # Declare the entities
# Bonnie = Const('Bonnie', Entity)

# # Define all facts
# facts = [
#     # If people perform in school talent shows often, then they attend and are very engaged with school events.
#     ForAll([x], Implies(PerformInSchoolTalentShowsOften(x), AttendAndEngagedWithSchoolEvents(x))),
#     # People either perform in school talent shows often or are inactive and disinterested members of their community.
#     ForAll([x], Or(PerformInSchoolTalentShowsOften(x), InactiveAndDisinterestedMemberOfCommunity(x))),
#     # If people chaperone high school dances, then they are not students who attend the school.
#     ForAll([x], Implies(ChaperoneHighSchoolDances(x), Not(StudentAttendSchool(x)))),
#     # All people who are inactive and disinterested members of their community chaperone high school dances.
#     ForAll([x], Implies(InactiveAndDisinterestedMemberOfCommunity(x), ChaperoneHighSchoolDances(x))),
#     # All young children and teenagers who wish to further their academic careers and educational opportunities are students who attend the school.
#     ForAll([x], Implies(TeenagerWishToFurtherAcademicCareersAndEducationalOpportunities(x), StudentAttendSchool(x))),
#     # Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.
#     Or(And(AttendAndEngagedWithSchoolEvents(Bonnie), StudentAttendSchool(Bonnie)), Not(Or(AttendAndEngagedWithSchoolEvents(Bonnie), StudentAttendSchool(Bonnie))))
# ]

# # Create a solver instance
# solver = Solver()
# solver.add(facts)

# # add problem to solver
# solver.push()
# solver.add(PerformInSchoolTalentShowsOften(Bonnie))
# if solver.check() == sat:
#     solver.pop()
#     solver.add(Not(PerformInSchoolTalentShowsOften(Bonnie)))
#     if solver.check() == sat:
#         print("C")  # The statement is unknown(C) when sat
#     else:
#         print("A") # The statement is true(A) when unsat
# else:
#     print("B") # The statement is false(B)
# ```
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# [Problem]:
# %s
# [Question]:
# %s
# """

# PROMPT_FOLIO = """
# Problem:
# Miroslav Venhoda was a Czech choral conductor who specialized in the performance of Renaissance and Baroque music. Any choral conductor is a musician. Some musicians love music. Miroslav Venhoda published a book in 1946 called Method of Studying Gregorian Chant.
# Question:
# Based on the above information, is the following statement true, false, or uncertain? Miroslav Venhoda loved music.
# Based on the above information, is the following statement true, false, or uncertain? A Czech person wrote a book in 1946.
# Based on the above information, is the following statement true, false, or uncertain? No choral conductor specialized in the performance of Renaissance.

# ```python
# from z3 import *

# # Declare a finite domain sort for the entities
# Entity = DeclareSort('Entity')
# # Declare a fresh constant for universal quantification
# x1 = Const('x1', Entity)
# x2 = Const('x2', Entity)

# # Declare the predicates
# Czech = Function('Czech', Entity, BoolSort())
# ChoralConductor = Function('ChoralConductor', Entity, BoolSort())
# Specialize = Function('Specialize', Entity, Entity, BoolSort())
# Musician = Function('Musician', Entity, BoolSort())
# LoveMusic = Function('LoveMusic', Entity, BoolSort())
# Book = Function('Book', Entity, BoolSort())
# Publish = Function('Publish', Entity, Entity, BoolSort())
# Author = Function('Author', Entity, Entity, BoolSort())

# # Declare the entities
# miroslav_venhoda = Const('miroslav_venhoda', Entity)
# baroque = Const('baroque', Entity)
# renaissance = Const('renaissance', Entity)
# method_of_studying_gregorian_chant = Const('method_of_studying_gregorian_chant', Entity)
# year1946 = Const('year1946', Entity)

# # Define all facts
# facts = [
#     # Miroslav Venhoda was a Czech choral conductor who specialized in the performance of Renaissance and Baroque music.
#     And(And(Czech(miroslav_venhoda), ChoralConductor(miroslav_venhoda)), And(Specialize(miroslav_venhoda, renaissance), Specialize(miroslav_venhoda, baroque))),
#     # Any choral conductor is a musician.
#     ForAll([x1], Implies(ChoralConductor(x1), Musician(x1))),
#     # Some musicians love music.
#     Exists([x1], Implies(Musician(x1), LoveMusic(x1))),
#     # Miroslav Venhoda published a book in 1946 called Method of Studying Gregorian Chant.
#     And(And(Book(method_of_studying_gregorian_chant), Publish(year1946, method_of_studying_gregorian_chant)), Author(method_of_studying_gregorian_chant, miroslav_venhoda))
# ]

# # Add facts to solver
# solver = Solver()
# solver.add(facts)

# def query(solver, constraint):
#     # add problem to solver
#     solver.push()
#     solver.add(constraint)
#     if solver.check() == sat:
#         solver.pop()
#         solver.push()
#         solver.add(Not(constraint))
#         if solver.check() == sat:
#             answer = "C"  # The statement is unknown(C) when sat
#         else:
#             answer = "A" # The statement is true(A) when unsat
#         solver.pop()
#     else:
#         solver.pop()
#         answer = "B" # The statement is false(B)
#     return answer

# # Queries
# # Based on the above information, is the following statement true, false, or uncertain? Miroslav Venhoda loved music.
# constraint_1 = LoveMusic(miroslav_venhoda)
# print(query(solver, constraint_1))
# # Based on the above information, is the following statement true, false, or uncertain? A Czech person wrote a book in 1946.
# constraint_2 = Exists([x1, x2], And(And(Czech(x1), Author(x2, x1)), And(Book(x2), Publish(year1946, x2))))
# print(query(solver, constraint_2))
# # Based on the above information, is the following statement true, false, or uncertain? No choral conductor specialized in the performance of Renaissance.
# constraint_3 = Not(Exists([x1], And(ChoralConductor(x1), Specialize(x1, renaissance))))
# print(query(solver, constraint_3))
# ```
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# [Problem]:
# %s
# [Question]:
# %s
# """

PROMPT_FOLIO = """
Task Description: You are given a problem description and a question. The task is to write a python script to translate the problem and question into executable z3 program. And the following are the steps:
1) Declare a finite domain for entites and declare a fresh constant for universal quantification
2) Define all predicates in the problem.
3) Define all variables for all entities in the problem.
4) Give facts. You should write a comment indicating which sentence it is before the fact you give.
5) Create solver and add facts to solver
6) Check if the solver can find a model that satisfies the conditions, if it is unsat then print B; if the statement is sat(you should be very careful about this part), remove this fact constraint from solver, print A is the statement is unsat and C is still sat

Problem:
All people who regularly drink coffee are dependent on caffeine. People either regularly drink coffee or joke about being addicted to caffeine. No one who jokes about being addicted to caffeine is unaware that caffeine is a drug. Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug. If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.
Question:
Based on the above information, is the following statement true, false, or uncertain? Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.
Based on the above information, is the following statement true, false, or uncertain? Rina is either a person who regularly drinks coffee or a person who is unaware that caffeine is a drug.
Based on the above information, is the following statement true, false, or uncertain? If Rina is either a person who jokes about being addicted to caffeine and a person who is unaware that caffeine is a drug, or neither a person who jokes about being addicted to caffeine nor a person who is unaware that caffeine is a drug, then Rina jokes about being addicted to caffeine and regularly drinks coffee.
Options: 
A, B, C

```python
from z3 import *

# Declare a finite domain sort for the entities
Entity = DeclareSort('Entity')
# Declare a fresh constant for universal quantification
x = Const('x', Entity)

# Declare the predicates
RegularlyDrinkCoffee = Function('RegularlyDrinkCoffee', Entity, BoolSort())
DependentOnCaffeine = Function('DependentOnCaffeine', Entity, BoolSort())
JokeAboutBeingAddictedToCaffeine = Function('JokeAboutBeingAddictedToCaffeine', Entity, BoolSort())
UnawareThatCaffeineIsADrug = Function('UnawareThatCaffeineIsADrug', Entity, BoolSort())
Student = Function('Student', Entity, BoolSort())
DependentOnCaffeine = Function('DependentOnCaffeine', Entity, BoolSort())


# Declare the entities
Rina = Const('Rina', Entity)

# Define all facts
facts = [
    # All people who regularly drink coffee are dependent on caffeine.
    ForAll([x], Implies(RegularlyDrinkCoffee(x), DependentOnCaffeine(x))),
    # People either regularly drink coffee or joke about being addicted to caffeine.
    ForAll([x], Xor(RegularlyDrinkCoffee(x), JokeAboutBeingAddictedToCaffeine(x))),
    # No one who jokes about being addicted to caffeine is unaware that caffeine is a drug.
    ForAll([x], Implies(JokeAboutBeingAddictedToCaffeine(x), Not(UnawareThatCaffeineIsADrug(x)))),
    # Rina is either a student and unaware that caffeine is a drug, or neither a student nor unaware that caffeine is a drug.
    Xor(And(Student(Rina), UnawareThatCaffeineIsADrug(Rina)), And(Not(Student(Rina)), Not(UnawareThatCaffeineIsADrug(Rina)))),
    # If Rina is not a person dependent on caffeine and a student, then Rina is either a person dependent on caffeine and a student, or neither a person dependent on caffeine nor a student.
    Implies(Not(And(DependentOnCaffeine(Rina), Student(Rina))), Xor(And(DependentOnCaffeine(Rina), Student(Rina)), And(Not(DependentOnCaffeine(Rina)), Not(Student(Rina)))))
]

# Create a solver instance
solver = Solver()
solver.add(facts)

def query(solver, constraint):
    # add problem to solver
    solver.push()
    solver.add(constraint)
    if solver.check() == sat:
        solver.pop()
        solver.push()
        solver.add(Not(constraint))
        if solver.check() == sat:
            answer = "C"  # The statement is unknown(C) when sat
        else:
            answer = "A" # The statement is true(A) when unsat
        solver.pop()
    else:
        solver.pop()
        answer = "B" # The statement is false(B)
    return answer

# Based on the above information, is the following statement true, false, or uncertain? Rina is either a person who jokes about being addicted to caffeine or is unaware that caffeine is a drug.
constraint_1 = Xor(JokeAboutBeingAddictedToCaffeine(Rina), UnawareThatCaffeineIsADrug(Rina))
print(query(solver, constraint_1))
constraint_2 = Xor(RegularlyDrinkCoffee(Rina), UnawareThatCaffeineIsADrug(Rina))
print(query(solver, constraint_2))
constraint_3 = Implies(Xor(And(JokeAboutBeingAddictedToCaffeine(Rina), UnawareThatCaffeineIsADrug(Rina)), And(Not(JokeAboutBeingAddictedToCaffeine(Rina)), Not(UnawareThatCaffeineIsADrug(Rina)))), And(JokeAboutBeingAddictedToCaffeine(Rina), RegularlyDrinkCoffee(Rina)))
print(query(solver, constraint_3))
```
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[Problem]:
%s
[Question]:
%s
[Options]:
%s
"""

INSTRUCTION_PROMPT_FOLIO = """
You should write in the format as comment in python script as follows:
Declare finite domain and universal quantifier: <domain and quantifier you define>
Declare the predicates: <the predicates you generate>
Define entities: <the entities you generate>
Give facts:  <facts you generate>
Create solver and add facts to solver: <create solver and add facts>
Check if satisfy the condition: if it is unsat then print B; if the statement is sat(you should be very careful about this part), remove this fact constraint from solver, print A is the statement is unsat and C is still sat


You must meet the following requirements:
1. The output should be a python script of the format ```python <code generate> ```
2. All boolen variables and all predicates should be defined, and you should only define each variable and predicate once, not multiple times.
3. All facts should be stated. Number of Facts you generate should be the same as number of sentences in the [Problem](A sentence is defined as ending with ".").
4. In the code, there must be an uncertain case for outputing C, other than just output A and B
5. You should only use these functions: And, Implies, Not, Or, Forall, Exists, Function, BoolSort
    1) And(arg1, arg2) - logical conjunction of arg1 and arg2
    2) Implies(arg1, arg2) - logical implication of arg1 and arg2
    3) Not(arg1) - logical negation of arg1
    4) Or(arg1, arg2) - either arg1 or arg2
    5) Forall(variable, arg1) - logical universal quantification of arg1 with respect to variable
    6) Exists(variable, arg1) - logical existential quantification of arg1 with respect to variable
    7) Function - a definition of function
    8) Boolsort
6. Do not make extra reasoning, just follow the sentences and define each variable and fact as what the problem says. For example, if the sentence says "have lunch at home." do not intepret as "not have lunch in company".
"""
Placeholder = """
The following is an example: 
Problem:
If people perform in school talent shows often, then they attend and are very engaged with school events. People either perform in school talent shows often or are inactive and disinterested members of their community. If people chaperone high school dances, 
then they are not students who attend the school. All people who are inactive and disinterested members of their community chaperone high school dances. All young children and teenagers who wish to further their academic careers and educational opportunities are 
students who attend the school. Bonnie either both attends and is very engaged with school events and is a student who attends the school, or she neither attends and is very engaged with school events nor is a student who attends the school.
Question: Based on the above information, is the following statement true, false, or uncertain? Bonnie performs in school talent shows often.
5. In facts, don't use universal quantifier if each entity has already been defined.
"""

########################################################################################
#################################    Logical Deduction    ##############################
########################################################################################
PROMPT_LOGICALDEDUCTION = """
Task Description: You are given a problem description and a question. The task is to write an executable python script.  And the following are the steps:
1) Define variables
2) Create a solver instance 
3) Add constraints for variables
4) Solve the constraints

The following is an example: 
Problem:
The following paragraphs each describe a set of five objects arranged in a fixed order. The statements are logically consistent within each paragraph.\n\nOn a shelf, there are five books: a green book, a blue book, a white book, a purple book, and a yellow book. The blue book is to the right of the yellow book. The white book is to the left of the yellow book. The blue book is the second from the right. The purple book is the second from the left.
Question: Which of the following is true?
Options: 
A) The green book is the second from the left.,
B) The blue book is the second from the left.,
C) The white book is the second from the left.",
D) The purple book is the second from the left.",
E) The yellow book is the second from the left."
```python
from z3 import *

# Define the position variables for the books
Green, Blue, White, Purple, Yellow = Ints('Green Blue White Purple Yellow')

# Define the order as leftest being 1, rightest being 5.
# Create a solver instance
s = Solver()

# Add constraints for the positions of the books
s.add(And(Green >= 1, Green <= 5))
s.add(And(Blue >= 1, Blue <= 5))
s.add(And(White >= 1, White <= 5))
s.add(And(Purple >= 1, Purple <= 5))
s.add(And(Yellow >= 1, Yellow <= 5))

# All positions are distinct
s.add(Distinct(Green, Blue, White, Purple, Yellow))

# The blue book is to the right of the yellow book.
s.add(Blue > Yellow)

# The white book is to the left of the yellow book.
s.add(White < Yellow)

# The blue book is the second from the right. (So it's 4th from the left)
s.add(Blue == 4)

# The purple book is the second from the left.
s.add(Purple == 2)

# Solve the constraints
# Check the solution and print the corresponding answer
if s.check() == sat:
    m = s.model()
    if m[Green].as_long() == 2:
        print("A")
    elif m[Blue].as_long() == 2:
        print("B")
    elif m[White].as_long() == 2:
        print("C")
    elif m[Purple].as_long() == 2:
        print("D")
    elif m[Yellow].as_long() == 2:
        print("E")
else:
    print("No solution")
```
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[Problem]:
%s
[Question]:
%s
[Options]:
%s
"""
INSTRUCTION_PROMPT_LOGICALDEDUCTION = """
You must meet the following requirements:
1. The output should be a python script of the format ```python <code generate> ```
2. All boolen variables and all predicates should be defined, and you should only define each variable and predicate once, not multiple times.
3. All facts should be stated.
4. Write a comment after defining a solver instance to state how you define the order of objects and you should follow the definiton of the order in later relationships. Eg. if the scope is left and right, then define leftest as 1, rightest as 5; if scope is old and new, then define oldest as 1, newest as 5
"""
