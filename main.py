import random
import math
import numpy as np

city_count = 5
cities = {}
list_of_distances = [[0 for x in range(city_count)] for y in range(city_count)]
letter_to_number = {}

finished_states = {}

first_visited = {}
first_not_visited = []
last_visited = {}
last_not_visited = []


def create_cities():
    letter = "A"
    for x in range(city_count):
        coordinate_x = random.randint(-100, 100)
        coordinate_y = random.randint(-100, 100)
        cities.update({letter: [coordinate_x, coordinate_y]})
        letter = ord(letter) + 1
        letter = chr(letter)


def fill_distances():
    letter1 = "A"
    for i in range(city_count):
        letter2 = "A"
        letter_to_number.update({letter1: i})
        for j in range(city_count):
            f = cities.get(letter1)
            x1 = f[0]
            y1 = f[1]
            g = cities.get(letter2)
            x2 = g[0]
            y2 = g[1]
            distance = math.sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))
            list_of_distances[i][j] = distance
            letter2 = ord(letter2) + 1
            letter2 = chr(letter2)
        letter1 = ord(letter1) + 1
        letter1 = chr(letter1)


def fill_distances_80percent():
    fill_distances()

    deleted_roads = ((pow(city_count, 2) - city_count) / 2) * 0.2
    deleted_roads = math.floor(deleted_roads)
    while deleted_roads != 0:
        rand_x = random.randint(0, city_count - 1)
        rand_y = random.randint(0, city_count - 1)
        if list_of_distances[rand_x][rand_y] != 0 and list_of_distances[rand_x][rand_y] != math.inf:
            list_of_distances[rand_x][rand_y] = math.inf
            list_of_distances[rand_y][rand_x] = math.inf
            deleted_roads -= 1


def get_distance_and_temp_states(states, not_visited, temp_states):
    distance = 0
    for state in states.keys():
        current_distance = states.get(state)
        for city in not_visited:
            temp_string = state
            temp_string = str(temp_string)
            if city not in temp_string:
                temp_string = temp_string + str(city)
                f = letter_to_number.get(temp_string[-2])
                g = letter_to_number.get(city)
                distance = list_of_distances[f][g]
                if not math.isinf(distance):
                    temp_states.update({temp_string: distance + current_distance})

    return distance, temp_states


def search_tree_bfs(states):
    not_visited = []
    for key in cities.keys():
        not_visited.append(key)
        if not states:
            not_visited.remove(key)
            states.update({key: 0})

    temp_states = {}
    distance, temp_states = get_distance_and_temp_states(states, not_visited, temp_states)

    if len(list(temp_states.keys())[0]) != city_count:
        states.clear()
        states.update(temp_states)
        search_tree_bfs(states)
    else:
        states.clear()
        states.update(temp_states)
        temp_states.clear()

        temp_states = get_states(temp_states, states)

        states.clear()
        states.update(temp_states)
        keys = [k for k, v in states.items() if v == min(states.values())]
        print("BFS: the cheapest road(s) are: " + str(keys))
        print("with value: " + str(min(states.values())))


def get_states(states, completed_states):
    starting = ["A"]
    for state in completed_states.keys():
        current_distance = completed_states.get(state)
        for city in starting:
            temp_string = state
            temp_string = str(temp_string)
            temp_string = temp_string + str(city)
            f = letter_to_number.get(temp_string[-2])
            g = letter_to_number.get(city)
            distance = list_of_distances[f][g]
            if not math.isinf(distance):
                states.update({temp_string: distance + current_distance})
    return states


def search_tree_dfs(states):
    not_visited = []
    for key in cities.keys():
        not_visited.append(key)
        if not states:
            not_visited.remove(key)
            states.update({key: 0})

    state = list(states.keys())[-1]
    for city in not_visited:
        current_distance = states.get(state)
        temp_string = state
        temp_string = str(temp_string)
        if city not in temp_string:
            temp_string = temp_string + str(city)
            f = letter_to_number.get(temp_string[-2])
            g = letter_to_number.get(city)
            distance = list_of_distances[f][g]
            if not math.isinf(distance):
                if len(temp_string) != city_count:
                    states.update({temp_string: distance + current_distance})
                else:
                    finished_states.update({temp_string: distance + current_distance})
    states.pop(state)

    if len(list(states.keys())) != 0:
        search_tree_dfs(states)
    else:
        states = get_states(states, finished_states)

        keys = [k for k, v in states.items() if v == min(states.values())]
        print("DFS: the cheapest road(s) are: " + str(keys))
        print("with value: " + str(min(states.values())))


def greedy_search(states):
    not_visited = []
    for key in cities.keys():
        not_visited.append(key)
        if not states:
            not_visited.remove(key)
            states.update({key: 0})

    temp_states = {}
    for state in states.keys():
        current_distance = states.get(state)
        for city in not_visited:
            temp_string = state
            temp_string = str(temp_string)
            if city not in temp_string:
                temp_string = temp_string + str(city)
                f = letter_to_number.get(temp_string[-2])
                g = letter_to_number.get(city)
                distance = list_of_distances[f][g]
                if not math.isinf(distance):
                    temp_states.update({temp_string: distance + current_distance})
                else:
                    print("Gr: City " + city + " unreachable in chain " +
                          temp_string)

    min_value = min(temp_states.values())
    min_key = [k for k in temp_states if temp_states[k] == min_value]
    min_key = str(min_key[0])

    states.clear()
    states.update({min_key: min_value})
    if len(str(min_key)) != city_count:
        greedy_search(states)
    else:
        for state in states.keys():
            current_distance = states.get(state)
            city = "A"
            temp_string = state
            temp_string = str(temp_string)
            temp_string = temp_string + str(city)
            f = letter_to_number.get(temp_string[-2])
            g = letter_to_number.get(city)
            distance = list_of_distances[f][g]
            if not math.isinf(distance):
                temp_states.clear()
                temp_states.update({temp_string: distance + current_distance})
                if temp_states:
                    print("greedy: road and its value:")
                    print(temp_states)
                else:
                    print("greedy: no road found due to missing chain")
                    print(temp_states)
            else:
                print("greedy: starting city may be unreachable from last "
                      "chosen city.")
                print(temp_states)


def sort_distances(sorted_distances):
    sorted_distances = sorted(sorted_distances.items(), key=lambda z: z[1])
    return sorted_distances


def minimum_spanning_tree(not_visited, visited):
    if not visited:
        visited.update({"A": 0})
        not_visited.remove("A")

    current_tree, current_distance = '', 0

    temp_states = {}
    for state in visited.keys():
        for city in not_visited:
            temp_string = str(state) + str(city)
            f = letter_to_number.get(temp_string[-2])
            g = letter_to_number.get(city)
            distance = list_of_distances[f][g]
            if not math.isinf(distance):
                temp_states.update({temp_string: distance})
    for state in visited.keys():
        for city in not_visited:
            temp_string = str(city) + str(state)
            f = letter_to_number.get(city)
            g = letter_to_number.get(temp_string[1])
            distance = list_of_distances[f][g]
            if not math.isinf(distance):
                temp_states.update({temp_string: distance})
        current_tree = str(state)

    temp_states = sort_distances(temp_states)

    shortest = temp_states[0][1]
    temp_string = temp_states[0][0]

    for letter in temp_string:
        if letter not in current_tree:
            not_visited.remove(letter)

    for state in visited.keys():
        current_distance = visited.get(state)

    visited.clear()
    visited.update({temp_string: float(shortest) + current_distance})

    if len(temp_string) != city_count:
        minimum_spanning_tree(not_visited, visited)
    else:
        temp_states = {}
        first_letter = str(temp_string[0])
        for state in visited.keys():
            current_distance = visited.get(state)
            temp_string = str(state) + str(first_letter)
            f = letter_to_number.get(temp_string[-2])
            g = letter_to_number.get(first_letter)
            distance = list_of_distances[f][g]
            if not math.isinf(distance):
                temp_states.update({temp_string: distance + current_distance})
        if temp_states:
            print("MST: the shortest might be: ")
            print(temp_states)
        else:
            print("MST: the road back is missing")
            print(visited)


def check_path():
    temp_states = {}
    for path_beg in first_visited.keys():
        for path_end in last_visited.keys():
            temp_beg = str(path_beg)
            temp_beg = temp_beg[-1]
            temp_end = str(path_end[1:])
            temp_end = temp_end[::-1]
            if temp_beg == temp_end:
                letters = temp_end
                temp_end = path_end.replace(letters, '')
                path = str(path_beg) + str(temp_end)
                dist1 = first_visited.get(path_beg)
                dist2 = last_visited.get(path_end)
                distance = dist1 + dist2
                temp_states.update({path: distance})
            else:
                pass
    if not temp_states:
        return 0, 0
    else:
        temp_states = sort_distances(temp_states)
        shortest_value = temp_states[0][1]
        shortest = temp_states[0][0]
        return shortest, shortest_value


def bidirectional():
    if not first_visited:
        for key in cities.keys():
            first_not_visited.append(key)
        first_visited.update({"A": 0})
        first_not_visited.remove("A")
    if not last_visited:
        for key in cities.keys():
            last_not_visited.append(key)
        last_city = [i for i in letter_to_number if letter_to_number[i] ==
                     city_count - 1]
        last_city = str(last_city[0])
        last_visited.update({last_city: 0})
        last_not_visited.remove(last_city)

    temp_states = {}
    distance, temp_states = get_distance_and_temp_states(first_visited, first_not_visited, temp_states)

    first_visited.clear()
    first_visited.update(temp_states)
    temp_states.clear()
    answer, answer_val = check_path()
    if answer != 0:
        print("the connection looks like: " + str(answer) + " with value: " +
              str(answer_val))
    else:
        distance, temp_states = get_distance_and_temp_states(last_visited, last_not_visited, temp_states)

        last_visited.clear()
        last_visited.update(temp_states)
        temp_states.clear()
        answer, answer_val = check_path()

        if answer != 0:
            print("the connection looks like: " + str(answer) + " with value: "
                  + str(answer_val))
        else:
            bidirectional()


create_cities()
#  fill_distances()
fill_distances_80percent()

print(cities)
print("")
print(np.matrix(list_of_distances))
print("")
print(letter_to_number)
print("")

all_states = {}
not_visited_cities = []
visited_cities = {}

# --------- here are searches -------
search_tree_bfs(all_states)
print("")

all_states = {}
search_tree_dfs(all_states)
print("")

#  all_states = {}
#  greedy_search(all_states)
#  print("")

#  for point in cities.keys():
#  not_visited_cities.append(point)
#  minimum_spanning_tree(not_visited_cities, visited_cities)
#  print("")

list_of_distances[0][city_count - 1] = math.inf
list_of_distances[city_count - 1][0] = math.inf
bidirectional()
