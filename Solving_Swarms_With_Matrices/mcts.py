import math
from random import random
import random
import numpy

import search

'''The code is implementing the Monte Carlo Tree Search algorithm to find an optimal path for a given problem. The 
Node class represents a node in the tree with its state, children, value, number_of_visits, parent, and action. It 
also contains methods to expand the node, get the best child based on UCT (Upper Confidence Bound for Trees) 
calculation, and check if the node is fully expanded or is a terminal node. '''


class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.children = []
        self.value = 0
        self.number_of_visits = 0
        self.parent = parent
        self.action = action

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action)
        return next_node

    def expand(self, problem):
        self.children = [self.child_node(problem, action) for action in problem.actions(self.state)]
        return self.children

    def get_uct(self, time, c):
        ucb1 = self.value + c * math.sqrt(math.log(time) / self.number_of_visits)
        return ucb1

    def best_uct(self, time, problem):
        best_uct_child = self.children[0]
        best_uct = best_uct_child.get_uct(time, problem)
        for c in self.children:
            child_uct = c.get_uct(time, problem)
            if child_uct > best_uct:
                best_uct_child = c
                best_uct = child_uct
        return best_uct_child

    def is_fully_expanded(self):
        if not self.children:
            return False
        for child in self.children:
            if child.number_of_visits == 0:
                return False
        return True

    def is_terminal(self, problem):
        return problem.goal_test(self.state)

    def depth(self):
        node = self
        depth = 0
        while node.parent is not None:
            depth += 1
            node = node.parent
        return depth


def resources_left(time, sims):
    return time <= sims


def pick_unvisited(children):
    for c in children:
        if not c.number_of_visits:
            return c
    return None


def traverse(problem, node, time, c):
    while node.is_fully_expanded():
        node = node.best_uct(time, c)
    if node.is_terminal(problem):
        return node
    if len(node.children) == 0:
        node.expand(problem)
    unvisited_child = pick_unvisited(node.children)
    return unvisited_child


def get_area_value(area, probs, pests):
    return sum(probs[area][p] * pests[p] for p in pests)


def rollout(node, problem):
    state = node.state
    while not problem.goal_test(state):
        actions = problem.actions(state)
        action = choose_action(actions)
        state = problem.result(state, action)
    return problem.value(state)


def choose_action(actions):
    best_action = random.choice(actions)
    return best_action


def is_root(node):
    return node.parent is None


# function for backpropagation
def update_stats(node, result):
    node.value = (node.value * node.number_of_visits + result) / (node.number_of_visits + 1)
    node.number_of_visits += 1


def backpropagate(node, result, gamma):
    update_stats(node, result)
    if is_root(node):
        return
    backpropagate(node.parent, result / gamma, gamma)


def get_best_child(node):
    most_frequent_child = node.children[0]
    highest_number_of_visits = most_frequent_child.number_of_visits
    for c in node.children:
        if c.number_of_visits > highest_number_of_visits:
            most_frequent_child = c
            highest_number_of_visits = c.number_of_visits
    return most_frequent_child


def monte_carlo_tree_search(problem, number_of_simulations):
    root = Node(problem.initial)
    root.expand(problem)
    node = root
    time = 0
    exploration_constsant = 1 / (problem.get_expected_reward() ** 2)
    while resources_left(time, number_of_simulations):
        leaf = traverse(problem, node, time, exploration_constsant)
        simulation_result = rollout(leaf, problem)
        backpropagate(leaf, simulation_result * (problem.gamma ** (leaf.depth() - 1)), problem.gamma)
        time += 1
        print("Simulation", time)
    print()
    node = root
    while not node.is_terminal(problem):
        if node.number_of_visits == 0:
            break
            print("The tree has no terminal leaves. Try more simulations or smaller exploration rate.")
        node = get_best_child(node)
    print('Number of simulations: ', number_of_simulations)
    print('Number of drones: ', problem.num_of_drones)
    print('Number of swarms: ', problem.num_of_swarms)
    print(node.state)
    print("Expected value: ", node.value)


def get_area_neighbours(area, probs):
    x = area[1]
    y = area[2]
    neighbours = []
    maybe_neighbours = [None for _ in range(4)]
    maybe_neighbours[0] = 'a' + x + str(int(y) + 1)
    maybe_neighbours[1] = 'a' + x + str(int(y) - 1)
    maybe_neighbours[2] = 'a' + str(int(x) + 1) + y
    maybe_neighbours[3] = 'a' + str(int(x) - 1) + y
    for neighbour in maybe_neighbours:
        if neighbour in probs:
            neighbours.append(neighbour)
    return neighbours


def get_best_neighbour_direction(area, best_neighbours):
    best_neighbour = best_neighbours[area]
    if int(best_neighbour[1]) == int(area[1]) + 1:
        return 'Up'
    if int(best_neighbour[1]) == int(area[1]) - 1:
        return 'Down'
    if int(best_neighbour[2]) == int(area[2]) + 1:
        return 'Right'
    if int(best_neighbour[2]) == int(area[2]) - 1:
        return 'Left'
    else:
        return None


def get_best_neighbours_cheatsheet(probs, pests):
    best_neighbours = {}
    for a in probs:
        neighbours = get_area_neighbours(a, probs)
        neighbours_values = {n: get_area_value(n, probs, pests) for n in neighbours}
        best_neighbours[a] = max(neighbours_values, key=neighbours_values.get)
    return best_neighbours

