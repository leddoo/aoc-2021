import operator
from pprint import pprint
from copy import deepcopy

inpt = """inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 7
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 12
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 15
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -16
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 12
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 10
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 8
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -11
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 1
add x 13
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -8
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 3
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -1
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 9
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -4
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 4
mul y x
add z y
inp w
mul x 0
add x z
mod x 26
div z 26
add x -14
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y 13
mul y x
add z y"""


var_names = ["w", "x", "y", "z"]

ops = [ line.split(" ") for line in inpt.splitlines() ]

divs_after_op = [0] * len(ops)
divs_remaining = 0
for i in reversed(range(len(ops))):
    if ops[i][0] == "div" and ops[i][2] == "26":
        divs_remaining += 1
    divs_after_op[i] = divs_remaining


def _solve(state, cache):
    pc, regs = state

    values = { name: value for name, value in regs }

    if pc >= len(ops):
        if values["z"] == 0:
            return ""
        else:
            return None

    # this is crucial, as it prunes a lot of the search space!
    # z is added to, multiplied by 26, and divided by 26.
    # so if the divides can't get it down to zero anymore, we don't need to
    # bother with this state.
    if values["z"] > 26 ** divs_after_op[pc]:
        return None

    op = ops[pc]

    if op[0] == "inp":
        pc += 1

        # part 1/2
        for digit in reversed(range(1, 9 + 1)):
        #for digit in range(1, 9 + 1):
            values[op[1]] = digit
            state = (pc, tuple(values.items()))
            result = solve(state, cache)
            if result is not None:
                return str(digit) + result
    else:
        while pc < len(ops) and ops[pc][0] != "inp":
            op = ops[pc]
            pc += 1

            other = values[op[2]] if op[2] in var_names else int(op[2])

            if op[0] == "add":
                values[op[1]] += other
            elif op[0] == "mul":
                values[op[1]] *= other
            elif op[0] == "div":
                values[op[1]] //= other
            elif op[0] == "mod":
                values[op[1]] %= other
            elif op[0] == "eql":
                values[op[1]] = 1 if values[op[1]] == other else 0
            else:
                assert False

        return solve((pc, tuple(values.items())), cache)

def solve(state, cache):
    if state in cache:
        return None
    else:
        result = _solve(state, cache)
        if result is None:
            cache.add(state)
        return result


import time

t0 = time.time()

print(solve((0, tuple((name, 0) for name in var_names)), set()))

t1 = time.time()
print(t1 - t0, "s")

exit(0)










# below is my first attempt.
# it computes the result symbolically.
# the idea was to have a relatively simple formula at the end and analyze it
# manually. the above solution is obviously much simpler. lesson learned, know
# your problem and abuse its details. clearly, there was a pattern to the
# instructions, but I was intimidated by the number of instructions, and didn't
# want to analyze the program by hand.


def is_int(a):
    return isinstance(a, int)

def are_ints(*args):
    return all(is_int(a) for a in args)


def is_str(a):
    return isinstance(a, str)

def is_list(a):
    return isinstance(a, list)

def is_tuple(a):
    return isinstance(a, tuple)


def fun_div(a, b):
    return a // b

def fun_eql(a, b):
    return 1 if a == b else 0


fun_map = {
    "add": operator.add,
    "mul": operator.mul,
    "div": fun_div,
    "mod": operator.mod,
    "eql": fun_eql,
}


var_names = ["x", "y", "z", "w"]


bounds = {}


# evaluate

inputs = {
    f"i{i}": int(n)
    for i, n in enumerate("99999999999999")
}


var_values = {
    name: 0
    for name in var_names
}

input_counter = 0

for line in inpt.splitlines():
    parts = line.split(" ")
    op = parts[0]

    #inp a - Read an input value and write it to variable a.
    if op == "inp":
        reg = parts[1]
        var_values[reg] = inputs[f"i{input_counter}"]
        input_counter += 1
        continue

    r1, o2 = parts[1:]
    v1 = var_values[r1]
    v2 = var_values[o2] if o2 in var_names else int(o2)

    var_values[r1] = fun_map[op](v1, v2)

reference = var_values.copy()

print("direct")
print(reference)
print()



def evaluate(value, inputs, cache):
    vid = get_vid(value)
    if vid in cache:
        return cache[vid]

    result = value
    if is_str(value):
        result = inputs[value]
    elif is_list(value):
        op = value[0]
        v1 = evaluate(value[1], inputs, cache)
        v2 = evaluate(value[2], inputs, cache)
        result = fun_map[op](v1, v2)

    cache[vid] = result
    return result



def get_vid(value):
    if isinstance(value, list):
        return (id(value), )
    else:
        return value

values = { name: 0 for name in var_names }


input_counter = 0

for line in inpt.splitlines():
    parts = line.split(" ")
    op = parts[0]

    #inp a - Read an input value and write it to variable a.
    if op == "inp":
        reg = parts[1]
        values[reg] = f"i{input_counter}"
        input_counter += 1
        continue

    r1, o2 = parts[1:]
    v1 = values[r1]
    v2 = values[o2] if o2 in var_names else int(o2)

    values[r1] = [op, v1, v2]


print("kinda symbolic")
for name, value in values.items():
    print(name, evaluate(value, inputs, {}))
print()


def update(values):
    bounds = {}

    def find_bounds(value):
        vid = get_vid(value)
        if vid in bounds:
            return bounds[vid]

        b = None

        if is_int(value):
            b = (value, value)
        elif is_str(value):
            b = (None, None)
            if value.startswith("i"):
                b = (1, 9)
        else:
            assert is_list(value)

            op = value[0]
            v1 = value[1]
            v2 = value[2]

            b1 = find_bounds(v1)
            b2 = find_bounds(v2)

            b1_lo = b1[0]
            b1_hi = b1[1]
            b2_lo = b2[0]
            b2_hi = b2[1]

            b = (None, None)

            if op in ["add", "mul"]:
                b = [None, None]

                if are_ints(b1_lo, b2_lo):
                    b[0] = fun_map[op](b1_lo, b2_lo)
                if are_ints(b1_hi, b2_hi):
                    b[1] = fun_map[op](b1_hi, b2_hi)

                b = tuple(b)

            if op == "mod":
                if are_ints(b2_lo, b2_hi) and b2_lo > 0 and b2_hi > 0:
                    b = (0, b2_hi - 1)

            if op == "eql":
                if are_ints(*b1, *b2) and (b2_lo > b1_hi or b1_lo > b2_hi):
                    b = (0, 0)
                else:
                    b = (0, 1)

        bounds[vid] = b
        return b

    def is_tight(b):
        return b[0] is not None and b[0] == b[1]


    factors = {}

    def find_factors(value):
        vid = get_vid(value)
        if vid in factors:
            return factors[vid]

        fs = set()

        if is_int(value):
            if value < 0:
                value = -value
                fs.add(-1)

            for i in range(1, value + 1):
                if value % i == 0:
                    fs.add(i)

        elif is_list(value):
            op = value[0]
            v1 = value[1]
            v2 = value[2]

            fs1 = find_factors(v1)
            fs2 = find_factors(v2)

            if op == "mul":
                fs = fs1.union(fs2)

        factors[vid] = fs
        return fs


    for name, value in values.items():
        bounds[name] = find_bounds(value)
        factors[name] = find_factors(value)


    changed = [False]

    simplify_cache = {}

    def simplify(value):
        vid = get_vid(value)
        if vid in simplify_cache:
            return simplify_cache[vid]

        #print("simp<")
        old_eval = evaluate(value, inputs, {})

        b  = bounds[vid]
        fs = factors[vid]

        new_value = None

        if is_tight(b):
            new_value = b[0]

        elif is_list(value):
            value[1] = simplify(value[1])
            value[2] = simplify(value[2])

            op = value[0]
            v1 = value[1]
            v2 = value[2]

            b1 = bounds[get_vid(v1)]
            b2 = bounds[get_vid(v2)]

            i1 = b1[0] if is_tight(b1) else None
            i2 = b2[0] if is_tight(b2) else None

            if are_ints(i1, i2):
                new_value = fun_map[op](i1, i2)
            elif op == "add":
                if i1 == 0:
                    new_value = v2
                elif i2 == 0:
                    new_value = v1
            elif op == "mul":
                if i1 == 0 or i2 == 0:
                    new_value = 0
                elif i1 == 1:
                    new_value = v2
                elif i2 == 1:
                    new_value = v1
            elif op == "div":
                if is_int(i2) and i2 > 0 and is_int(b1[1]) and b1[1] < i2:
                    new_value = 0
                elif i2 == 1:
                    new_value = v1
            elif op == "mod":
                if is_int(i2) and i2 > 0:
                    if is_int(b1[1]) and b1[1] < i2:
                        new_value = v1
                    elif is_list(v1) and v1[0] == "add":
                        is_zero = tuple(i2 in factors[get_vid(v)] for v in (v1[1], v1[2]))

                        if any(is_zero):
                            changed[0] = True

                            new_value = value[:]
                            new_value[1] = v1[:]
                            for i, z in enumerate(is_zero):
                                if z:
                                    new_value[1][1 + i] = 0

        if new_value is not None and new_value != value:
            new_eval = evaluate(new_value, inputs, {})
            assert old_eval == new_eval

            changed[0] = True
            bounds[get_vid(new_value)]  = find_bounds(new_value)
            factors[get_vid(new_value)] = find_factors(new_value)
            value = new_value

        #print("simp>")

        simplify_cache[vid] = value
        return value

    old_evals = {
        name: evaluate(value, inputs, {})
        for name, value in values.items()
    }

    new_values = {
        name: simplify(value)
        for name, value in values.items()
    }

    for name, new_value in new_values.items():
        values[name] = new_value

    new_evals = {
        name: evaluate(value, inputs, {})
        for name, value in values.items()
    }

    assert new_evals == old_evals

    #print("bounds:", bounds)
    #print("factors:", factors)

    return changed[0]


while update(values):
    pass

for name, value in values.items():
    print(name, value)

#pprint(values["z"])
#pprint(values)


print("kinda symbolic")
for name, value in values.items():
    print(name, evaluate(value, inputs, {}))
print()



def print_infix(value):
    if is_list(value):
        op = { "add": "+", "mul": "*", "div": "/", "mod": "%", "eql": "=" }[value[0]]
        print("(", end = "")
        print_infix(value[1])
        print(f" {op} ", end = "")
        print_infix(value[2])
        print(")", end = "")
    else:
        print(value, end = "")

#print_infix(values["z"])
#print()

