import math
from random import random
import random
import numpy

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

    def get_uct(self, time, c):
        ucb1 = self.value + c*math.sqrt(math.log(time) / self.number_of_visits)
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

    def depth(self):
        node = self
        depth = 0
        while node.parent is not None:
            depth += 1
            node = node.parent
        return depth


def resources_left(time, sims):
    return time <= sims


def monte_carlo_tree_search(problem, sims):
    root = Node(problem.initial)
    root.expand(problem)
    node = root
    time = 0
    ex_constsant = 1/(problem.get_expected_reward()**2)
    while resources_left(time, sims):
        leaf = traverse(problem, node, time, ex_constsant)
        simulation_result = rollout(leaf, problem)
        backpropagate(leaf, simulation_result * (problem.gamma ** (leaf.depth() - 1)), problem.gamma)
        time += 1
        print("Simulation", time)
    print()
    node = root
    while not node.is_terminal(problem):
        node = best_child(node)
    print('Number of simulations: ', sims)
    print('Number of drones: ', problem.num_of_drones)
    print('Number of swarms: ', problem.num_of_swarms)

    print(node.state)
    print("Expected value: ", node.value)


def pick_unvisited(children):
    for c in children:
        if not c.number_of_visits:
            return c
    return None


# function for node traversal
def traverse(problem, node, time, c):
    while node.fully_expanded():
        node = node.best_uct(time, c)
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
        action = get_best_immediate_action(state, problem, actions)
        state = problem.result(state, action)
    return problem.value(state)


def get_best_immediate_action(state, problem, actions):
    best_action = random.choice(actions)
    return best_action
    best_value = problem.value(problem.result(state, best_action))
    for action in actions:
        value = problem.value(problem.result(state, action))
        if value > best_value:
            best_action = action
            best_value = value
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
    return most_frequent_child
