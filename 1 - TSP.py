import math
import random
from heapq import *
import time
import matplotlib.pyplot as plt


VALUE = 0
INDEX = 1
FRONTIER = 0
EXPLORED = 1


class Node:
    def __init__(self, id=-1):
        self.f = 0
        self.g = 0
        self.h = 0
        self.state = []
        self._id = id

    def __lt__(self, other):
        return self.h < other.h

    def set_costs(self, g, h):
        self.g = g
        self.h = h
        self.f = g + h

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id


class PriorityQueue:
    def __init__(self):
        self.data = []

    def put(self, node):
        heappush(self.data, (node.f, node))

    def get(self):
        return heappop(self.data)[1]

    def is_empty(self):
        return len(self.data) == 0

    def update(self, updates):
        x = len(updates)
        for i in range(len(self.data)):
            if x == 0:
                break
            nodeID = self.data[i][1].id
            if nodeID in updates:
                x-=1
                if updates[nodeID][0] < self.data[i][0]:
                    self.data[i] = updates[nodeID]

        heapify(self.data)


class PriorityQueue_MST:
    def __init__(self):
        self.data = []

    def put(self, val, id):
        heappush(self.data, (val, id))

    def get(self):
        return heappop(self.data)

    def update(self, updates):
        x = len(updates)
        for i in range(len(self.data)):
            if x == 0:
                break
            nodeID = self.data[i][1]
            if nodeID in updates:
                x-=1
                self.data[i] = updates[nodeID]

        heapify(self.data)


def get_distance(a, b):
    return math.pow(math.pow((a[0] - b[0]), 2) + math.pow((a[1] - b[1]), 2), 0.5)


def valid_node(newNode, coords):
    epsilon = 0.05
    for c in coords:
        if c == newNode:
            continue
        if get_distance(coords[newNode], coords[c]) < epsilon:
            return False
    return True


def add_distances(newNode, distances, coordinates):
    for i in range(len(coordinates)):
        if i == newNode:
            distances[i].append(0)
            continue
        d = get_distance(coordinates[newNode], coordinates[i])
        distances[i].append(d)
        distances[newNode].append(d)


def generateTSP(num_cities):
    distances = {0: [0]}
    coordinates = {0: [random.uniform(0,1), random.uniform(0,1)]}
    i = 1
    while i < num_cities:
        coordinates[i] = [random.uniform(0,1), random.uniform(0,1)]
        if valid_node(i, coordinates):
            distances[i] = []
            add_distances(i, distances, coordinates)
            i+=1

    return distances


def set_initial_values(unvisited):
    pq = PriorityQueue_MST()
    node_vals = {}
    root_id = next(iter(unvisited))
    for n in unvisited:
        if n == root_id:
            MST_val = 0
        else:
            MST_val = 10
        pq.put(MST_val, n)
        node_vals[n] = MST_val

    return pq, node_vals


def MST_prims(unvisited_ids):
    if not unvisited_ids:
        return 0
    mstSet = set()
    MST_cost = 0
    pq_unvisited, node_vals = set_initial_values(unvisited_ids)
    while len(mstSet) < len(unvisited_ids):
        minNode = pq_unvisited.get()
        mstSet.add(minNode[1])
        MST_cost += minNode[0]
        new_node_neighbour_distances = graph[minNode[1]]
        pq_updates = {}
        for i in unvisited_ids:
            if i in mstSet:
                continue
            if new_node_neighbour_distances[i] < node_vals[i]:
                node_vals[i] = new_node_neighbour_distances[i]
                pq_updates[i] = (node_vals[i], i)

        pq_unvisited.update(pq_updates)

    return MST_cost


def heuristic(child_node_id, unvisited_set, MST):
    minD1, minD2 = 10, 10
    for i in range(num_cities):
        if i in unvisited_set:
            if graph[child_node_id][i] < minD1:
                minD1 = graph[child_node_id][i]
            if graph[root_node_id][i] < minD2:
                minD2 = graph[root_node_id][i]

    if minD1 == 10:
        minD1 = 0
    if minD2 == 10:
        minD2 = graph[root_node_id][child_node_id]
    return minD1 + minD2 + MST


def TSP_goal_test(solution):
    if (len(solution) == num_cities+1) and solution[0] == solution[-1] and solution[0] == root_node_id:
        return True
    return False


def get_unvisited_ids(current_state):
    unvisited_ids = set(range(num_cities))
    for n in current_state:
        unvisited_ids.remove(n)

    if len(unvisited_ids) == 0:
        return [current_state[0]]

    return list(unvisited_ids)


def a_star():
    root_node = Node(id=root_node_id)
    root_node.state = [root_node_id]
    frontier = PriorityQueue()
    frontier.put(root_node)

    # Set membership: Boolean [frontier, explored]
    membership = {tuple(root_node.state): [True, False]}
    explored_count = 0

    while True:
        if frontier.is_empty():
            return False

        parent_node = frontier.get()

        # print(parent_node.f, parent_node.g, parent_node.h, parent_node.state)
        current_state = parent_node.state
        if TSP_goal_test(current_state):
            return explored_count, parent_node

        membership[tuple(current_state)][FRONTIER] = False
        membership[tuple(current_state)][EXPLORED] = True
        explored_count += 1

        unvisited_ids = get_unvisited_ids(parent_node.state)
        unvisited_set = set(unvisited_ids)

        pq_updates = {}
        for child_city_id in unvisited_ids:
            unvisited_set.remove(child_city_id)
            MST_cost = MST_prims(unvisited_set)

            child_state = tuple(current_state + [child_city_id])
            if child_state not in membership:
                membership[child_state] = [False, False]

            if not membership[child_state][EXPLORED] and not membership[child_state][FRONTIER]:
                newNode = Node(id=child_city_id)
                newNode.set_costs(
                    g=parent_node.g + graph[parent_node.id][child_city_id],
                    h=heuristic(child_city_id, unvisited_set, MST_cost)
                )
                newNode.state = list(child_state)

                frontier.put(newNode)
                membership[child_state][FRONTIER] = True

            elif membership[child_state][FRONTIER]:
                newNode = Node(id=child_city_id)
                newNode.set_costs(
                    g=parent_node.g + graph[parent_node.id][child_city_id],
                    h=heuristic(child_city_id, unvisited_set, MST_cost)
                )
                newNode.state = list(child_state)
                pq_updates[child_city_id] = (newNode.f, newNode)

            unvisited_set.add(child_city_id)

        frontier.update(pq_updates)


# Change these parameters if needed
root_node_id = 0
num_problems = 5
max_cities = 10

nodes_expanded_numCX = []
nodes_expanded_numCY = []
time_numCX = []
time_numCY = []

for i in range(3,max_cities+1):
    for j in range(num_problems):
        num_cities = i
        graph = generateTSP(num_cities)

        s = time.time()
        res1, res2 = a_star()
        total = time.time() - s

        nodes_expanded_numCX.append(i)
        nodes_expanded_numCY.append(res1)

        time_numCX.append(i)
        time_numCY.append(total)

print('Run successfully')

# Uncomment to plot graphs
# plt.grid(True)
# plt.scatter(nodes_expanded_numCX, nodes_expanded_numCY, s=3)
# plt.figure()
# plt.grid(True)
# plt.scatter(time_numCX, time_numCY, s=3)
# plt.show()
