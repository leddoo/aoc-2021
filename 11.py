inpt = """6636827465
6774248431
4227386366
7447452613
6223122545
2814388766
6615551144
4836235836
5334783256
4128344843"""

if False:
    inpt = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

def parse_grid():
    return [ [ int(char) for char in line ] for line in inpt.split("\n") ]


grid = parse_grid()

width = 10
height = 10

def step():
    flashes = 0
    stack = []

    def increment(x, y):
        grid[y][x] += 1
        if grid[y][x] == 10:
            stack.append((x, y))

    for y in range(height):
        for x in range(width):
            increment(x, y)

    while len(stack):
        flashes += 1
        x, y = stack.pop()

        x0 = max(x - 1, 0)
        x1 = min(x + 1, width - 1)
        y0 = max(y - 1, 0)
        y1 = min(y + 1, height - 1)
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                increment(x, y)

    for y in range(height):
        for x in range(width):
            if grid[y][x] > 9:
                grid[y][x] = 0

    return flashes

total_flashes = 0
for i in range(100):
    total_flashes += step()

print(total_flashes)



grid = parse_grid()

first_sync = 1
while step() != width * height:
    first_sync += 1

print(first_sync)
