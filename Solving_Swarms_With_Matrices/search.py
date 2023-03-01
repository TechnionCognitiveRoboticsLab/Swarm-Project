import sys
from collections import deque

from utils import *
import itertools


class Problem:
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value. Hill Climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


# ______________________________________________________________________________


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node. Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        children = [self.child_node(problem, action)
            for action in problem.actions(self.state)]
        return children

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path()[1:]]

    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # We want for a queue of nodes in breadth_first_graph_search or
    # astar_search to have no duplicated states, so we treat nodes
    # with the same state as equal. [Problem: this may not be what you
    # want in other contexts.]

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        # We use the hash value of the state
        # stored in the node instead of the node
        # object itself to quickly search a node
        # with the same state in a Hash matrix
        return hash(self.state)


# ______________________________________________________________________________



def best_first_graph_search(problem, f, display=False):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
            print('Best path is:')
            print(str(node))
            print('Path value (max_reward - expected value):')
            print(f(node))
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    print('Did not find any!')
    return None


def astar_search(problem, h=None, display=False):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

class SingleSwarmProblem(Problem):
    def __init__(self, HOR, size_x, size_y, pests, probs, max_reward, num_of_drones):
        super().__init__(tuple(['X'] * HOR))
        self.HOR = HOR
        self.size_x = size_x
        self.size_y = size_y
        self.pests = pests
        self.probs = probs
        self.max_reward = max_reward
        self.num_of_drones = num_of_drones

    def get_x(self, state):
        rights = 0
        lefts = 0
        for i in range(self.HOR):
            if state[i] == 'Left':
                lefts += 1
            if state[i] == 'Right':
                rights += 1
            if state[i] == 'X':
                break
        return rights - lefts

    def get_y(self, state):
        ups = 0
        downs = 0
        for i in range(self.HOR):
            if state[i] == 'Up':
                ups += 1
            if state[i] == 'Down':
                downs += 1
            if state[i] == 'X':
                break
        return ups - downs

    def actions(self, state):
        """Up, Down, Left, Right minus boundaries"""
        if state[-1] != 'X':
            return []  # All columns filled; no successors
        else:
            acts = []#['No-op']
            x = self.get_x(state)
            y = self.get_y(state)
            if x < self.size_x-1:
                acts.append('Right')
            if x >= 1:
                acts.append('Left')
            if y < self.size_y-1:
                acts.append('Up')
            if y >= 1:
                acts.append('Down')
            return acts

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return 0

    def result(self, state, act):
        """Place the next queen at the given row."""
        now = state.index('X')
        new = list(state[:])
        new[now] = act
        return tuple(new)

    def actions_to_areas(self, state):
        areas = ['X' for t in self.HOR]
        latest = 'a11'
        for time in range(self.HOR):
            areas[time] = latest
            match state[time]:
                case 'Up':
                    latest = list(latest)
                    latest[2] = str(int(latest[2])+1)
                    latest = ''.join(latest)
                case 'Down':
                    latest = list(latest)
                    latest[2] = str(int(latest[2])-1)
                    latest = ''.join(latest)
                case 'Right':
                    latest = list(latest)
                    latest[1] = str(int(latest[1])+1)
                    latest = ''.join(latest)
                case 'Left':
                    latest = list(latest)
                    latest[1] = str(int(latest[1])-1)
                    latest = ''.join(latest)
                case 'No-op':
                    latest = latest
                case other:  # ('X')
                    break
        return areas

    def get_prob_of_subset(self, subset, probs):
        '''Taking a look on every possible combination of pests that can be on an area we count
         the probability of that combination of pests being there. Using the old matrix and the data we have. '''
        p = 1
        for t in self.pests:
            if t in subset:
                p *= probs[t]
            else:
                p *= 1 - probs[t]
        return p

    def count_prob(self, num_of_drones, reward, matrix, area):
        """We want to count probability of being in square [num of drones][reward]. We do so by finding all squares that
         we may have been in, in the previous round. In order to do so we look at possible subsets of pests we may have
         eliminated in this round. After that we count the probabilities of arriving into the current square from those
         squares. Then we sum over all of these probabilities """
        all_subsets = self.get_all_subsets_of_pests()
        p_tot = 0
        for subset in all_subsets:
            p = 1
            reward_for_subset = 0
            for pest in subset:
                reward_for_subset += self.pests[pest]
            prev_reward = reward - reward_for_subset
            prev_num_of_drones = num_of_drones + len(subset) # or + 1
            if prev_reward < 0 or prev_num_of_drones >= len(matrix):
                p = 0
            else:
                p = self.get_prob_of_subset(subset, self.probs[area]) * (matrix[prev_num_of_drones][prev_reward])
            p_tot += p
        if num_of_drones == 0:
            return matrix[num_of_drones][reward] + (1 - matrix[num_of_drones][reward])*p_tot
        else:
            return p_tot

    def get_all_subsets_of_pests(self):
        all_subsets = []
        for n in range(len(self.pests) + 1):
            for subset in list(itertools.combinations(self.pests, n)):
                all_subsets.append(subset)
        return all_subsets

    def update_matrix(self, matrix, area):
        matrix = matrix
        max_d = len(matrix[0])
        max_r = len(matrix)
        new_matrix = [[0 for d in range(max_d)] for r in range(max_r)]
        for d in range(max_r):
            for r in range(max_d):
                new_matrix[d][r] = self.count_prob(d, r, matrix, area)
        return new_matrix

    def get_matrix(self, state):
        """ We create an empty (all zeros) matrix of probabilities. Each number in it represents the probability of
        the swarm having x drones while gaining y rewards. For our every action we update the matrix unless there are
        no more actions in which case we stop or if we make no action or land on a square we have already been on in
        which case the matrix doesn't change. """
        areas = self.actions_to_areas(state)
        matrix = [[0 for col in range(self.max_reward)] for row in range(self.num_of_drones+1)]
        matrix[self.num_of_drones][0] = 1
        for i in range(len(areas)):
            if areas[i] == 'X':
                break
            been_here = areas.index(areas[i]) != i
            if been_here:
                continue
            area = areas[i]
            matrix = self.update_matrix(matrix, area)
#        print(areas)

        # DEBUG

        sum = 0

        for d in matrix:
            for r in range(len(d)):
                if d[r] != 0:
                    sum += d[r]*r
 #       print(sum)


        '''
        # PRINT matrix:
        for row in matrix:
            strow = []
            for c in row:
                strow.append(round(c, 3))
             print(strow)
        print()'''
        return matrix

    def h(self, node):
        matrix = self.get_matrix(node.state)
        max_d = len(matrix)
        max_r = len(matrix[0])
        sum = 0
        for d in range(max_d):
            for r in range(max_r):
                sum += matrix[d][r]*r
        return self.max_reward - sum

    def goal_test(self, state):
         return state[- 1] != 'X'
'''
        matrix = self.get_matrix(state)
        max_d = len(matrix)
        max_r = len(matrix[0])
        sum = 0
        for d in range(max_d):
            for r in range(max_r):
                sum += matrix[d][r]*r
        return self.requirement - sum <= 0
        '''


class MultiSwarmProblem(Problem):
    def __init__(self, size_x, size_y, HOR, pests, probs, num_of_drones, num_of_swarms, max_reward, requirement, gamma):
        super().__init__(tuple(tuple('X' for k in range(HOR)) for j in range(num_of_swarms)))
        self.HOR = HOR
        self.size_x = size_x
        self.size_y = size_y
        self.pests = pests
        self.probs = probs
        self.max_reward = max_reward
        self.num_of_drones = num_of_drones
        self.num_of_swarms = num_of_swarms
        self.requirement = requirement
        self.gamma = gamma

    def get_x(self, state):
        rights = 0
        lefts = 0
        for i in range(self.HOR):
            if state[i] == 'Left':
                lefts += 1
            if state[i] == 'Right':
                rights += 1
            if state[i] == 'X':
                break
        return rights - lefts

    def get_y(self, state):
        ups = 0
        downs = 0
        for i in range(self.HOR):
            if state[i] == 'Up':
                ups += 1
            if state[i] == 'Down':
                downs += 1
            if state[i] == 'X':
                break
        return ups - downs

    def actions(self, full_state):
        """Up, Down, Left, Right minus boundaries"""
        actions_for_swarm = [[] for swarm in range(self.num_of_swarms)]
        for swarm in range(self.num_of_swarms):
            if full_state[swarm][-1] == 'X':
                x = self.get_x(full_state[swarm])
                y = self.get_y(full_state[swarm])
                if x < self.size_x-1:
                    actions_for_swarm[swarm].append('Right')
                if x >= 1:
                    actions_for_swarm[swarm].append('Left')
                if y < self.size_y-1:
                    actions_for_swarm[swarm].append('Up')
                if y >= 1:
                    actions_for_swarm[swarm].append('Down')
        actions = list(itertools.product(*actions_for_swarm))
        return actions

    def path_cost(self, c, state1, action, state2):
        return 1

    def result(self, full_state, act):
        new_full_state = []
        now = full_state[0].index('X')
        for s in range(self.num_of_swarms):
            new_full_state.append(list(full_state[s]))
            new_full_state[s][now] = act[s]
            new_full_state[s] = tuple(new_full_state[s])
        return tuple(new_full_state)

    def actions_to_areas(self, full_state):
        full_areas = [['X' for k in range(self.HOR)]for s in range(self.num_of_swarms)]
        latest = ['a11' for s in range(self.num_of_swarms)]
        for swarm in range(self.num_of_swarms):
            for time in range(self.HOR):
                full_areas[swarm][time] = latest[swarm]
                match full_state[swarm][time]:
                    case 'Up':
                        latest[swarm] = list(latest[swarm])
                        latest[swarm][2] = str(int(latest[swarm][2])+1)
                        latest[swarm] = ''.join(latest[swarm])
                    case 'Down':
                        latest[swarm] = list(latest[swarm])
                        latest[swarm][2] = str(int(latest[swarm][2])-1)
                        latest[swarm] = ''.join(latest[swarm])
                    case 'Right':
                        latest[swarm] = list(latest[swarm])
                        latest[swarm][1] = str(int(latest[swarm][1])+1)
                        latest[swarm] = ''.join(latest[swarm])
                    case 'Left':
                        latest[swarm] = list(latest[swarm])
                        latest[swarm][1] = str(int(latest[swarm][1])-1)
                        latest[swarm] = ''.join(latest[swarm])
                    case 'No-op':
                        latest[swarm] = latest[swarm]
                    case other:  # ('X')
                        break

        return full_areas

    def get_prob_of_subset(self, subset, probs):
        '''Taking a look on every possible combination of pests that can be on an area we count
         the probability of that combination of pests being there. Using the old matrix and the data we have. '''
        p = 1
        for t in self.pests:
            if t in subset:
                p *= probs[t]
            else:
                p *= 1 - probs[t]
        return p

    def count_prob(self, num_of_drones, reward, matrix, area):
        """We want to count probability of being in square [num of drones][reward]. We do so by finding all squares that
         we may have been in, in the previous round. In order to do so we look at possible subsets of pests we may have
         eliminated in this round. After that we count the probabilities of arriving into the current square from those
         squares. Then we sum over all of these probabilities """
        all_subsets = self.get_all_subsets_of_pests()
        p_tot = 0
        for subset in all_subsets:
            p = 1
            reward_for_subset = 0
            for pest in subset:
                reward_for_subset += self.pests[pest]
            prev_reward = reward - reward_for_subset
            prev_num_of_drones = num_of_drones + 1# len(subset)
            if prev_reward < 0 or prev_num_of_drones >= len(matrix):
                p = 0
            else:
                p = self.get_prob_of_subset(subset, self.probs[area]) * (matrix[prev_num_of_drones][prev_reward])
            p_tot += p
        if num_of_drones == 0:
            return matrix[num_of_drones][reward] + (1 - matrix[num_of_drones][reward])*p_tot
        else:
            return p_tot

    def get_all_subsets_of_pests(self):
        all_subsets = []
        for n in range(len(self.pests) + 1):
            for subset in list(itertools.combinations(self.pests, n)):
                all_subsets.append(subset)
        return all_subsets

    def update_matrix(self, matrix, area):
        max_d = len(matrix[0])
        max_r = len(matrix)
        new_matrix = [[0 for d in range(max_d)] for r in range(max_r)]
        for d in range(max_r):
            for r in range(max_d):
                new_matrix[d][r] = self.count_prob(d, r, matrix, area)
        return new_matrix

    def get_matrices(self, full_state):
        """ We create an empty (all zeros) matrix of probabilities. Each number in it represents the probability of
        the swarm having x drones while gaining y rewards. For our every action we update the matrix unless there are
        no more actions in which case we stop or if we make no action or land on a square we have already been on in
        which case the matrix doesn't change. """
        areas = self.actions_to_areas(full_state)
        matrices = [[[0 for r in range(self.max_reward+1)] for d in range(self.num_of_drones+1)] for s in range(self.num_of_swarms)]
        for swarm in range(self.num_of_swarms):
            matrices[swarm][self.num_of_drones][0] = 1

        for time in range(self.HOR):
            if areas[0][time] == 'X':
                break
            for swarm in range(self.num_of_swarms):
                # checking for already visited areas
                area = areas[swarm][time]
                if self.is_visited(areas, swarm, time):
                    continue
                matrices[swarm] = self.update_matrix(matrices[swarm], area)
        return matrices

    def is_visited(self, areas, swarm, time):
        for t in range(time+1):
            for s in range(self.num_of_swarms):
                if t == time and s == swarm:
                    return False
                if areas[s][t] == areas[swarm][time]:
                    return True
        return False

    def get_matrix_value(self, matrix):
        value = 0
        for d in range(self.num_of_drones+1):
            for r in range(self.max_reward+1):
                value += r*matrix[d][r]
        return value

    def value(self, state):
        matrices = self.get_matrices(state)
        matrix_values = [0 for s in range(self.num_of_swarms)]
        for s in range(self.num_of_swarms):
            matrix_values[s] = self.get_matrix_value(matrices[s])
        return sum(matrix_values)

    def h(self, node):
        matrices = self.get_matrices(node.state)
        matrix_values = [0 for s in range(self.num_of_swarms)]
        for s in range(self.num_of_swarms):
            matrix_values[s] = self.get_matrix_value(matrices[s])
        h = self.max_reward - sum(matrix_values)
        return h

    def goal_test(self, state):
        for s in range(self.num_of_swarms):
            if state[s][- 1] == 'X':
                return False
        return True

        '''
        matrices = self.get_matrices(state)
        matrix_values = [0 for s in range(self.num_of_swarms)]
        for s in range(self.num_of_swarms):
            matrix_values[s] = self.get_matrix_value(matrices[s])
        tot_value = self.max_reward - sum(matrix_values)
        return tot_value < self.requirement'''
