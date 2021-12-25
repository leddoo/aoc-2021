from collections import Counter

inpt = """PBFNVFFPCPCPFPHKBONB

KK -> S
FO -> B
PP -> O
HN -> S
CN -> H
VH -> P
BK -> B
VC -> N
CB -> H
OC -> K
BF -> P
FV -> K
SP -> F
OP -> K
SS -> B
NN -> O
CS -> K
CF -> K
FF -> S
SV -> P
OK -> S
CO -> F
OB -> K
BH -> B
HH -> S
VB -> V
KV -> H
CK -> V
NV -> N
SF -> V
PK -> H
PV -> N
FB -> O
BO -> K
FP -> N
OF -> N
FK -> O
VK -> V
NO -> V
NS -> C
KC -> S
VF -> V
BV -> N
CP -> K
PB -> V
CC -> S
NH -> B
CV -> P
SO -> V
NC -> O
HK -> K
SB -> H
OO -> V
HO -> P
PS -> B
BC -> P
KO -> C
KB -> C
VV -> F
BS -> F
HB -> B
KN -> S
FC -> C
SN -> S
HC -> O
HP -> F
BP -> V
ON -> K
BB -> K
KH -> O
NP -> H
KS -> N
SH -> K
VP -> O
PF -> O
HF -> S
BN -> S
NK -> C
FH -> O
CH -> B
KP -> B
FN -> K
OV -> P
VS -> K
OH -> V
PC -> F
VO -> H
SK -> S
PO -> O
KF -> N
NF -> V
NB -> C
PN -> O
FS -> C
PH -> F
VN -> S
OS -> V
HV -> H
HS -> B
SC -> C"""

if False:
    inpt = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""


template, rules = inpt.split("\n\n")

rules = rules.splitlines()
rules = [ rule.split(" -> ") for rule in rules ]
rules = { rule[0]: rule[1] for rule in rules }

last_counts = None

poly = template[:]
for iteration in range(10):
    new_poly = poly[0]

    for i in range(len(poly) - 1):
        pair = poly[i : i + 2]
        new_poly += rules[pair]
        new_poly += poly[i + 1]

    poly = new_poly


counts = Counter(poly)
min_count = min(counts.values())
max_count = max(counts.values())
print(counts)
print(max_count - min_count)


pairs = dict(Counter([ template[i : i + 2] for i in range(len(template) - 1) ]))
for iteration in range(40):
    new_pairs = { pair: 0 for pair in rules }

    for pair in pairs:
        middle = rules[pair]
        left = pair[0] + middle
        right = middle + pair[1]
        new_pairs[left]  += pairs[pair]
        new_pairs[right] += pairs[pair]

    pairs = new_pairs

counts = { letter: 0 for letter in set(rules.values()) }
counts[template[-1]] += 1
for pair in pairs:
    counts[pair[0]] += pairs[pair]

min_count = min(counts.values())
max_count = max(counts.values())
print(counts)
print(max_count - min_count)
