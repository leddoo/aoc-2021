import heapq
import time
import sys

inpt = ["BC", "DD", "CB", "AA"]

if True:
    inpt = ["BA", "CD", "BC", "DA"]

room_depth = 2


if True:
    inpt = ["BDDC", "DCBD", "CBAB", "AACA"]

    if False:
        inpt = ["BDDA", "CCBD", "BBAC", "DACA"]

    room_depth = 4


move_cost = { "A": 1, "B": 10, "C": 100, "D": 1000 }

hallway_length = 11

room_entries = [ 2, 4, 6, 8 ]

target_rooms = { "A": 0, "B": 1, "C": 2, "D": 3 }


class Task:
    def __init__(self, sort_key, payload):
        self.sort_key = sort_key
        self.payload  = payload

    def __lt__(self, other):
        return self.sort_key < other.sort_key



queue = []

visited = set()

def enqueue(cost, rooms, hallway):
    # this helps a ton!
    # reduces execution time from minutes to seconds.
    # there are only around 100k states.
    # without caching, the queue can contain upwards of 200k entries, constantly
    # triggering gc's.
    key = (tuple(tuple((tuple(entry) if entry is not None else None) for entry in room) for room in rooms), tuple(hallway))
    if key in visited:
        return

    heapq.heappush(queue, Task(cost, (cost, rooms, hallway)))
    visited.add(key)

def dequeue():
    return heapq.heappop(queue).payload


PAWN_WAITING = 1
PAWN_FINAL   = 2

def patch_states(room, color):
    all_final = True
    for i in reversed(range(room_depth)):
        if room[i] is None:
            all_final = False
            continue

        if all_final and room[i][0] == color:
            room[i][1] = PAWN_FINAL
        else:
            room[i][1] = PAWN_WAITING
            all_final = False


def patch_all_states(rooms):
    for color, room_index in target_rooms.items():
        patch_states(rooms[room_index], color)


start_hallway = [ None ] * hallway_length
start_rooms = [ [ [pawn, 0] for pawn in room ] for room in inpt ]

patch_all_states(start_rooms)


enqueue(0, start_rooms, start_hallway)


printer = 0
start_time = time.time()

while len(queue) > 0:
    state = dequeue()
    cost, rooms, hallway = state

    # print "progress"
    if printer == 0:
        #now = time.time() - start_time
        #print(f"Point({{{now}, {cost}}}),", end = "")
        #sys.stdout.flush()
        print(len(queue), cost, len(visited))

    printer = (printer + 1) % 5000

    # detect done.
    any_non_final = False
    for room in rooms:
        for entry in room:
            if entry is None or entry[1] != PAWN_FINAL:
                any_non_final = True
                break

    if not any_non_final:
        print("done!")
        print(state)
        print(cost)
        break


    def can_enter_target_room(pawn, hallway_index):
        target_room_index    = target_rooms[pawn]
        target_hallway_index = room_entries[target_room_index]
        room = rooms[target_room_index]

        has_space = room[0] is None
        if not has_space:
            return None

        # skip Nones
        room_cursor = 1
        while room_cursor < room_depth and room[room_cursor] is None:
            room_cursor += 1
        pawn_index = room_cursor - 1

        # validate pawns below insertion index.
        while room_cursor < room_depth:
            entry = room[room_cursor]
            if entry is None or entry[0] != pawn:
                return None

            room_cursor += 1

        # check if hallway is free.
        direction = 1 if hallway_index < target_hallway_index else -1
        cursor    = hallway_index + direction
        blocked   = False
        while cursor != target_hallway_index:
            if hallway[cursor] is not None:
                blocked = True
                break
            cursor += direction

        if blocked:
            return None

        return (pawn_index, target_room_index, abs(target_hallway_index - hallway_index))


    # move waiting pawns out:
    #   move to target if possible.
    #   else, move to all possible hallway positions.
    for room_index, room in enumerate(rooms):
        pawn_index = None
        for i in range(room_depth):
            if room[i] is not None and room[i][1] == PAWN_WAITING:
                pawn_index = i
                break
        if pawn_index is None:
            continue

        pawn = room[pawn_index][0]

        hallway_index = room_entries[room_index]

        direct = can_enter_target_room(pawn, hallway_index)

        # go into target if possible.
        if direct is not None:
            enter_index, target_room, hallway_steps = direct

            steps = pawn_index + 1 + hallway_steps + 1 + enter_index

            new_cost = cost
            new_cost += steps * move_cost[pawn]

            # these are optimized deepcopy's.
            # helped when there was no visited tracking.
            new_rooms = rooms[:]

            new_rooms[room_index] = rooms[room_index][:]
            new_rooms[room_index][pawn_index] = None

            new_rooms[target_room] = rooms[target_room][:]
            new_rooms[target_room][enter_index] = (pawn, PAWN_FINAL)

            new_hallway = hallway

            enqueue(new_cost, new_rooms, new_hallway)

        else:
            # move to hallway. consider all possible positions.
            def explore(cursor):
                if hallway[cursor] is not None:
                    return False

                if cursor not in room_entries:
                    steps = abs(cursor - hallway_index) + 1 + pawn_index

                    new_cost = cost
                    new_cost += steps * move_cost[pawn]

                    new_rooms = rooms[:]

                    new_rooms[room_index] = rooms[room_index][:]
                    new_rooms[room_index][pawn_index] = None

                    new_hallway = hallway[:]
                    new_hallway[cursor] = pawn

                    enqueue(new_cost, new_rooms, new_hallway)

                return True

            cursor = hallway_index
            while cursor >= 0 and explore(cursor):
                cursor -= 1

            cursor = hallway_index
            while cursor < hallway_length and explore(cursor):
                cursor += 1

    # move hallway pawns in.
    #   move to target if possible.
    for hallway_index, pawn in enumerate(hallway):
        if pawn is None:
            continue

        direct = can_enter_target_room(pawn, hallway_index)

        if direct is not None:
            enter_index, target_room, hallway_steps = direct

            steps = hallway_steps + 1 + enter_index

            new_cost = cost
            new_cost += steps * move_cost[pawn]

            new_rooms = rooms[:]

            new_rooms[target_room] = rooms[target_room][:]
            new_rooms[target_room][enter_index] = (pawn, PAWN_FINAL)

            new_hallway = hallway[:]
            new_hallway[hallway_index] = None

            enqueue(new_cost, new_rooms, new_hallway)

