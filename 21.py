from collections import Counter

inpt = [4, 3]

if False:
    inpt = [4, 8]

dd     = 1
rolls  = 0
board  = inpt[:]
scores = [0, 0]

def one_mod(a, b):
    return (a - 1) % b + 1

def play(player):
    global dd
    global rolls
    global board
    global scores
    delta = one_mod(dd + 0, 100) + one_mod(dd + 1, 100) + one_mod(dd + 2, 100)
    dd = one_mod(dd + 3, 100)
    rolls += 3

    board[player] = one_mod(board[player] + delta, 10)
    scores[player] += board[player]
    return scores[player] < 1000

while play(0) and play(1):
    pass

print(rolls * min(scores))



options = []
for i in range(3):
    for j in range(3):
        for k in range(3):
            options.append(i + j + k + 3)
options = dict(Counter(options))


states = { ((inpt[0], 0), (inpt[1], 0)): 1 }

wins = [0, 0]

def turn(states, player):
    global wins

    new_states = {}
    for players, c in states.items():
        for delta, delta_count in options.items():
            p, s = players[player]
            new_p = one_mod(p + delta, 10)
            new_s = s + new_p
            count = c * delta_count
            if new_s >= 21:
                wins[player] += count
            else:
                key = list(players)
                key[player] = (new_p, new_s)
                key = tuple(key)
                new_states[key] = new_states.get(key, 0) + count

    return new_states

while len(states) > 0:
    states = turn(states, 0)
    states = turn(states, 1)

print(wins)
