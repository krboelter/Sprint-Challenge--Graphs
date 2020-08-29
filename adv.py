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
stack = []
stack.append(graph[0])
visited = []
# if something is in path_back, this is a way back.
# once no more directions can be traveled in path_back, remove room from path_back
way_back = [] # stack
# if something is in visteded but not in way back, that means there are 2 ajoining paths

while len(stack) > 0:
    # check all directions, log which ones are available
    current_room = stack.pop() # gets current room with directions
    current_room_id = player.current_room.id # current room number

    if current_room_id not in graph:
        room_directions = player.current_room.get_exits() # all directions that exist for that room
        for dir in room_directions:
            graph[current_room_id][str(dir)] = '?'

        print(graph[current_room_id], "CURENT ROOM ID")

    for dir in current_room:
        # add room to visited
        # if it hasn't been visited and isn't in way_back it's a new room
        # add current room to stack and way back
        if dir not in visited and dir not in way_back: # this room has never been visited






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
