import math
from random import random

import search


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

    def get_uct(self, time, problem):
        ucb1 = self.value/self.number_of_visits + math.sqrt(2 * math.log(time) / self.number_of_visits)
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

    def fully_expanded(self):
        if len(self.children) != 0:
            for c in self.children:
                if not c.number_of_visits:
                    return False
            return True
        return False

    def is_terminal(self, problem):
        return problem.goal_test(self.state)


def resources_left(time, sims):
    return time <= sims


def monte_carlo_tree_search(problem, sims):
    root = Node(problem.initial)
    root.expand(problem)
    node = root
    time = 0
    while resources_left(time, sims):
        leaf = traverse(problem, node, time)
        simulation_result = rollout(leaf, problem)
        backpropagate(leaf, simulation_result * (problem.gamma ** (problem.HOR-1)), problem.gamma)
        time += 1
        print("Simulation", time)
    node = root
    while not node.is_terminal(problem):
        node = best_child(node)


def pick_unvisited(children):
    for c in children:
        if not c.number_of_visits:
            return c
    return None


# function for node traversal
def traverse(problem, node, time):
    while node.fully_expanded():
        node = node.best_uct(time, problem)
    # in case no children are present / node is terminal
    if node.is_terminal(problem):
        return node
    else:
        if len(node.children) == 0:
            node.expand(problem)
        unvisited_child = pick_unvisited(node.children)
        if unvisited_child is None:
            print()
        return unvisited_child


# function for the result of the simulation
def rollout(node, problem):
    state = node.state
    while not problem.goal_test(state):
        actions = problem.actions(state)
        action = actions[0]
        state = problem.result(state, action)
    return problem.value(state)


# function for randomly selecting a child node
def rollout_policy(node, problem):
    return node.expand(problem)[0]


def is_root(node):
    return node.parent is None


# function for backpropagation
def update_stats(node, result):
    node.value += result
    node.number_of_visits += 1


def backpropagate(node, result, gamma):
    update_stats(node, result)
    if is_root(node):
        return
    backpropagate(node.parent, result/gamma, gamma)


# function for selecting the best child
# node with highest number of visits
def best_child(node):
    most_frequent_child = node.children[0]
    highest_number_of_visits = most_frequent_child.number_of_visits
    for c in node.children:
        if c.number_of_visits > highest_number_of_visits:
            most_frequent_child = c
            highest_number_of_visits = c.number_of_visits
    print(most_frequent_child.state)
    print(most_frequent_child.value)
    return most_frequent_child
