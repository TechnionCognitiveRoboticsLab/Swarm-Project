import random
import time

import Averaging


def bernoulli(probability):
    return random.random() < probability


class Vertex:
    def __init__(self, name):
        self.name = name
        self.neighbours = None  # list of vertices
        self.probability = None  # dictionary from reward to probability
        self.reward = None
        self.is_emptied = False

    def get_avg_reward(self):
        avg = 0
        for p in self.probability:
            avg += p*self.probability[p]
        return avg
    def det_reward(self):
        p = random.random()
        sum_p = 0
        for r in self.probability:
            sum_p += self.probability[r]
            if sum_p > p:
                return r

    def toString(self):

        output = ("Vertex: " + self.name + '\n')
        output += '**********\n'
        # output += ("Neighbours: "+str([v. name for v in self.neighbours])+'\n')
        output += ("Reward: " + str(self.reward) + '\n')
        output += ("Is emptied: " + str(self.is_emptied) + '\n')

        return output


class Agent:
    def __init__(self):
        self.location = None
        self.movement_budget = None
        self.utility_budget = None
        self.utility_used = 0

    def toString(self):
        return "utility budget: " + str(self.utility_budget) + "\nutility used: " + str(self.utility_used) + '\n'


class Instance:
    def __init__(self, map, agents, passes=True, x_size = 0, y_size = 0):
        self.gamma = 0.9
        self.map = map
        self.agents = agents
        self.passes = passes
        self.x_size = x_size
        self.y_size = y_size
        self.path = [[(agent.location, True) for agent in self.agents]]

    def get_horizon(self):
        return max([a.movement_budget for a in self.agents]) + 1

    def toString(self, path):
        output = ''
        for t in range(len(path)):
            output += ('****** Time' + str(t) + ' ****** \n')
            for a in range(len(path[t])):
                output += ("Agent " + str(a + 1) + ": " + path[t][a].name + " " + str(path[t][a].probability) + '\n')
        return output

    def actions(self, path):
        t = len(path) - 1
        actions = [[]]
        for agent_index in range(len(self.agents)):
            old_actions = actions.copy()
            actions = []
            agent_location = path[t][agent_index][0]
            # print('agent ', agent_index, ' at ', agent_location.name)
            if self.agents[agent_index].movement_budget <= t:
                for action in old_actions:
                    new_action = action.copy()
                    new_action.append((agent_location, False))
                    actions.append(new_action)
            else:
                for action in old_actions:
                    for neighbour in agent_location.neighbours:
                        new_action = action.copy()
                        if self.passes:
                            new_action.append((neighbour, True))
                            actions.append(new_action)
                        new_action = action.copy()
                        new_action.append((neighbour, False))
                        actions.append(new_action)
        return actions

    def result(self, action, path):
        path.append(action)
        return path

    def initiate_deterministic_instance(self):
        for v in self.map:
            v.is_emptied = False
            v.reward = v.det_reward()
        for a in self.agents:
            a.utility_used = 0

    def value(self, path, is_dumb, number_of_simulations=1):
        if is_dumb:
            reward_sum = 0
            for i in range(number_of_simulations):
                reward_sum += self.play_simulation(path)
            return reward_sum / number_of_simulations
        else:
            return Averaging.get_expected_value_of_path(self, path)

    def play_simulation(self, path):
        reward = 0
        self.initiate_deterministic_instance()
        horizon = min(self.get_horizon(), len(path))
        for t in range(min(horizon, len(path))):
            for a in range(len(self.agents)):
                agent = self.agents[a]
                '''print("---------------")
                print("Agent:", a)
                print(agent.toString())'''
                vertex = path[t][a][0]
                passes = path[t][a][1]
                '''print("Passes:", passes)
                print(vertex.toString())'''
                reward += self.make_movement(vertex, agent, passes)
                #print("Total reward: ", reward)
        return reward

    def make_movement(self, vertex, agent, passes):
        if (not vertex.is_emptied) and (agent.utility_budget > agent.utility_used) \
                and (vertex.reward > 0) and not passes:
            return self.take_reward(agent, vertex)
        return 0

    def take_reward(self, agent, vertex):
        if vertex.reward != 0:
            agent.utility_used += 1
        vertex.is_emptied = True
        return vertex.reward

    def return_random_path(self):
        path = self.path
        for t in range(self.get_horizon()): 
            action = random.choice(self.actions(path))
            path = self.result(action, path)
        return path

    def goal_test(self, path):
        return len(path) >= self.get_horizon()
