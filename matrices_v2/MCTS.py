import math
from random import random
import random
from decimal import *
'''The code is implementing the Monte Carlo Tree Search algorithm to find an optimal path for a given problem. The 
Node class represents a node in the tree with its path, children, value, number_of_visits, parent, and action. It 
also contains methods to expand the node, get the best child based on UCT (Upper Confidence Bound for Trees) 
calculation, and check if the node is fully expanded or is a terminal node. '''


class Node:
    def __init__(self, path, parent=None, action=None):
        self.path = path
        self.children = []
        self.value = 0
        self.number_of_visits = 0
        self.parent = parent
        self.action = action

    def child_node(self, instance, action):
        next_path = instance.result(action, self.path.copy())
        next_node = Node(next_path, self, action)
        return next_node

    def expand(self, instance):
        self.children = [self.child_node(instance, action) for action in instance.actions(self.path)]
        return self.children

    def get_uct(self, time, c):
        ucb1 = self.value + c * math.sqrt(math.log(time) / self.number_of_visits)
        return ucb1

    def best_uct(self, time, instance):
        best_uct_child = self.children[0]
        best_uct = best_uct_child.get_uct(time, instance)
        for c in self.children:
            child_uct = c.get_uct(time, instance)
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

    def is_terminal(self, instance):
        return instance.goal_test(self.path)

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
    raise Exception("No unvisited children!")


def traverse(instance, node, time, c):
    while node.is_fully_expanded():
        node = node.best_uct(time, c)
    if node.is_terminal(instance):
        return node
    if len(node.children) == 0:
        node.expand(instance)
    unvisited_child = pick_unvisited(node.children)
    return unvisited_child


def rollout(node, instance, dumb):
    path = node.path
    while not instance.goal_test(path):
        actions = instance.actions(path)
        action = choose_action(actions)
        path = instance.result(action, path)
    value = instance.value(path, dumb)
    return value


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
    backpropagate(node.parent, result / Decimal(gamma), gamma)


def get_best_child(node):
    most_frequent_child = node.children[0]
    highest_number_of_visits = most_frequent_child.number_of_visits
    for c in node.children:
        if c.number_of_visits > highest_number_of_visits:
            most_frequent_child = c
            highest_number_of_visits = c.number_of_visits
    return most_frequent_child


def monte_carlo_tree_search(instance, number_of_simulations, dumb, jump):
    exploration_constsant = 1
    values = []
    time = 0
    root = Node(instance.path)

    node = root

    node.expand(instance)

    while resources_left(time, number_of_simulations):
        leaf_d = traverse(instance, node, time, exploration_constsant)

        simulation_reward_d = rollout(leaf_d, instance, dumb)

        discounted_value_d = Decimal(simulation_reward_d) * Decimal(instance.gamma ** (leaf_d.depth() - 1))

        backpropagate(leaf_d, discounted_value_d, instance.gamma)

        time += 1

        if time > 0 and time % jump == 0:
            node1 = root
            while not node.is_terminal(instance) and len(node1.children) != 0:
                node1 = get_best_child(node1)
            value = instance.value(node1.path, True, 30)
            values.append(value)
            #print(time)
    #print([[(node1.path[t][a][0].name, node1.path[t][a][1]) for a in range(len(node1.path[0]))] for t in
    #           range(len(node1.path))])
    return values
