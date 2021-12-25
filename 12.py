inpt = """KF-sr
OO-vy
start-FP
FP-end
vy-mi
vy-KF
vy-na
start-sr
FP-lh
sr-FP
na-FP
end-KF
na-mi
lh-KF
end-lh
na-start
wp-KF
mi-KF
vy-sr
vy-lh
sr-mi"""

if False:
    inpt = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

if False:
    inpt = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

if False:
    inpt = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


edges = {}
for line in inpt.splitlines():
    a, b = line.split("-")
    if a not in edges:
        edges[a] = [b]
    else:
        edges[a].append(b)
    if b not in edges:
        edges[b] = [a]
    else:
        edges[b].append(a)


def find_paths():
    def recurse(path, visited):
        current = path[-1]
        if current == "end":
            return 1
        if current.lower() == current and current in visited:
            return 0

        visited = visited.union(set([current]))

        result = 0
        for neighbor in edges[current]:
            result += recurse(path + [neighbor], visited)
        return result

    return recurse(["start"], set())

print(find_paths())


def find_paths():
    def recurse(path, visited, visited_small_cave_twice):
        current = path[-1]
        if current == "end":
            return 1
        if current.lower() == current and current in visited:
            if visited_small_cave_twice or current == "start":
                return 0
            visited_small_cave_twice = True

        visited = visited.union(set([current]))

        result = 0
        for neighbor in edges[current]:
            result += recurse(path + [neighbor], visited, visited_small_cave_twice)
        return result

    return recurse(["start"], set(), False)

print(find_paths())
