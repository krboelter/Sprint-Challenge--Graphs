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
visited = set()

def dfs_1(starting_dir):
    stack = []
    stack.append(start)
    new_dir = []
    new_dir.append(starting_dir)

    while len(stack) > 0:
        current = stack.pop()
        new_dir.pop()

        if current not in visited:
            visited.add(current)
            player.travel(new_dir)
            traversal_path.append(new_dir)

            for i in player.current_room.get_exits():
                new_dir.append(i)

dfs_1(player.current_room.id)


def opposite(dir):
    if dir == 'n':
        return 's'
    elif dir == 's':
        return 'n'
    elif dir == 'e':
        return 'w'
    elif dir == 'w':
        return 'e'

# start will equal the current room
def dfs(start):
    stack = []
    stack.append([start])

    while len(stack) > 0:
        current_room = stack.pop()
        current_room_id = player.current_room.id
        path_dirs = player.current_room.get_exits()

        for dir in path_dirs: # make sure to break for every direction taken
            # this path will be the first path that hasn't been visited
            opposite_dir = opposite(dir) # get the opposite direction

            if current_room[current_room_id][dir] == "?": # has not been visited
                player.travel(dir) # move the player
                new_room_id = player.current_room.id # set new room id
                new_dirs = player.current_room.get_exits() # get new room directions

                if new_room_id not in graph: # if the new location isn't in graph...
                    graph[new_room_id] = {} # add it to the graph

                    for i in new_dirs:
                        graph[new_room_id][i] = '?' # add a '?' for each location of new room

                # update old room with new location
                graph[current_room_id][dir] = new_room_id # old location in graph, update with new room id
                # update new room with old location
                graph[new_room_id][opposite_dir] = current_room_id # add the old location to the new graph entry

                if '?' in current_room: # if there are still '?' in the current room, add to stack
                    stack.append(current_room) # add the current room to the stack (still more rooms to explore)
                else:
                    break
                    # MIGHT NEED TO CALL BFS HERE
                    # player.travel(opposite_dir) # travel back from the direction you came

                if '?' in graph[new_room_id]: # if there are still rooms to explore
                    stack.append(graph[current_room_id]) # add it to the stack


        print(graph, "GRAPH AS OF NOW")
        stack = []


# dfs(graph[0])

def bfs(start, end):
    stack = []
    visited = []


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
