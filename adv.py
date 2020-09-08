from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# t_path needs to be filled with all of the directions to navigate this path

# get the room you are in
# use dfs and player.current_room to visited
# for each room visited, mark any other possible paths(to come back to)
# once you reach the end, use bfs to find the closest path that has another path to take
traversal_path = []
graph = {}
graph[0] = {'n': '?', 's': '?', 'w': '?', 'e': '?'}

def opposite(dir):
    if dir == 'n':
        return 's'
    elif dir == 's':
        return 'n'
    elif dir == 'e':
        return 'w'
    elif dir == 'w':
        return 'e'

def dfs_1(starting_room):
    stack = []
    dir_stack = []
    stack.append((starting_room, player.current_room.get_exits()[0]))
    visited = set()

    while len(stack) > 0:
        values = stack.pop()
        current = values[0]
        exits = player.current_room.get_exits() # get all exits [checks from n, s, w, e]

        # still need to move back to where there is an unexplored direction
        # before this fires, need to make sure there are no more places to go
        if len(dir_stack) >= 1 and len(exits) <= 1:
            print(player.current_room.id)
            print(exits, "HERE ARE THE EXITS")
            if exits == 0:
                return traversal_path
            while len(dir_stack) > 0:
                new_dir = dir_stack.pop()
                player.travel(opposite(new_dir))
                traversal_path.append(opposite(new_dir))
                # print(dir_stack, "DIR STACK SUBTRACT")
            # player.travel(stack[-1][1])
            # traversal_path.append(stack[-1][1])
            exits = player.current_room.get_exits()


        # have not been to the room before
        if current not in visited:
            visited.add(current)

            if len(exits) >= 2: # if there are more than one exit (there will always be one from the way you came)
                exits_added = [] # only get the exits not in visited

                exits_added = []
                for i in exits:
                    if player.current_room.get_room_in_direction(i).id not in visited: # we only want to add exits not in visited to stack
                        exits_added.append(i) # only add exits not in visited
                        stack.append((player.current_room.get_room_in_direction(i).id, i)) # add the room in that direction to the stack

                player.travel(exits_added[-1]) # travel in the direction of the last exit added to stack
                traversal_path.append(exits_added[-1]) # add direction traveld to the traversal path
                dir_stack.append(exits_added[-1]) # add the direction traveled
                print(dir_stack, "DIR STACK ADD")


dfs_1(player.current_room.id)
print(traversal_path, "TRAVERSAL PATH")


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
