
from typing import Set, Tuple

nrs = [4, 5, 7, 8, 9, 10]

class Expr:
    def __init__(self):
        self.used_digits: int = 0
        # a bit mask of all digits used in the expression
        self.value: int = None

class Number(Expr):
    """Expressions containing a single number"""
    def __init__(self, nr):
        self.number: int = nr
        self.value = nr
        self.used_digits = 1 << nr
    
    def __str__(self):
        return str(self.number)

class BinaryExpr(Expr):
    """Binary expressions"""
    def __init__(self, op: str, expr1: Expr, expr2: Expr):
        self.op = op
        self.expr1 = expr1
        self.expr2 = expr2
        self.used_digits = expr1.used_digits | expr2.used_digits
        if op == "+":
            self.value = expr1.value + expr2.value
        elif op == "*":
            self.value = expr1.value * expr2.value

    def __str__(self):
        return f"({self.expr1} {self.op} {self.expr2})"

value_to_expr = 1000 * [None]
nrs_found = 0

# If we have two expressions with same value and same used digits,
# then we consider them to be equal; keep a cache of all generated expressions
expression_cache: Set[Tuple[int, int]] = set()

# Will contain all generated expressions
expressions = []
# start by adding all numbers
new_expressions = [Number(nr) for nr in nrs]

def add_expr(exp: Expr):
    t = (exp.value, exp.used_digits)
    if t in expression_cache:
        # this expression has already been generated before
        return
    expression_cache.add(t)
    new_expressions.append(exp)
    if exp.value >= 100 and exp.value < 1000 and not value_to_expr[exp.value]:
        # Found a new result
        global nrs_found
        nrs_found += 1
        value_to_expr[exp.value] = exp
        print(f"{nrs_found}: {exp.value} = {value_to_expr[exp.value]}")
    
while new_expressions:
    expressions.extend(new_expressions)
    new_expressions = []
    # Create all binary expressions
    # (very ineffective, the same expressions are generated over and over again)
    for op in "+*":
        for i in range(len(expressions)):
            expr1 = expressions[i]
            for j in range(len(expressions)):
                expr2 = expressions[j]
                if expr1.used_digits & expr2.used_digits == 0:
                    exp = BinaryExpr(op, expr1, expr2)
                    add_expr(exp)
                # else some number is used in both expr1 and expr2
    print(f"Added {len(new_expressions)} new expressions")
for exp in expressions:
    print(f"{exp} = {exp.value}")
    if exp.value >= 0 and exp.value < 1000:
        value_to_expr[exp.value] = exp
for i in range(100, 1000):
    print(f"{i} = {value_to_expr[i]}")
print(len([x for x in value_to_expr[100:1000] if x is None]), "values missing")
    