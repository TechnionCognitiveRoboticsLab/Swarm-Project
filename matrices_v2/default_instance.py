import Instance
import MCTS
import Averaging

vertex1 = Instance.Vertex("v1")
vertex2 = Instance.Vertex("v2")
vertex3 = Instance.Vertex("v3")
vertex4 = Instance.Vertex("v4")
vertex5 = Instance.Vertex("v5")
vertex6 = Instance.Vertex("v6")
vertex7 = Instance.Vertex("v7")
vertex8 = Instance.Vertex("v8")
vertex9 = Instance.Vertex("v9")
vertex10 = Instance.Vertex("v10")
vertex11 = Instance.Vertex("v11")
vertex12 = Instance.Vertex("v12")
vertex13 = Instance.Vertex("v13")
vertex14 = Instance.Vertex("v14")
vertex15 = Instance.Vertex("v15")

vertex1.neighbours = [vertex2, vertex5, vertex6]
vertex1.probability = {0: 1}  # {0: 0.8, 1: 0.2}

vertex2.neighbours = [vertex1, vertex3, vertex8]
vertex2.probability = {2: 1}  # {2: 0.6, 1: 0.3, 0: 0.1}

vertex3.neighbours = [vertex4, vertex2, vertex10]
vertex3.probability = {4: 0.7, 2: 0.2, 1: 0.05, 0: 0.05}

vertex4.neighbours = [vertex12, vertex3, vertex5]
vertex4.probability = {3: 0.6, 0: 0.2, 1: 0.1, 2: 0.1}

vertex5.neighbours = [vertex1, vertex4, vertex14]
vertex5.probability = {0: 0.7, 4: 0.15, 3: 0.1, 5: 0.05}

vertex6.neighbours = [vertex15, vertex7, vertex1]
vertex6.probability = {1: 0.6, 2: 0.2, 4: 0.1, 5: 0.1}

vertex7.neighbours = [vertex6, vertex8]
vertex7.probability = {0: 0.5, 3: 0.25, 5: 0.15, 2: 0.1}

vertex8.neighbours = [vertex7, vertex2, vertex9]
vertex8.probability = {1: 0.4, 5: 0.2, 3: 0.2, 0: 0.2}

vertex9.neighbours = [vertex10, vertex8]
vertex9.probability = {3: 0.5, 1: 0.2, 0: 0.15, 5: 0.15}

vertex10.neighbours = [vertex11, vertex3, vertex9]
vertex10.probability = {4: 0.5, 2: 0.3, 1: 0.15, 0: 0.05}

vertex11.neighbours = [vertex10, vertex12]
vertex11.probability = {2: 0.5, 4: 0.2, 0: 0.15, 1: 0.15}

vertex12.neighbours = [vertex4, vertex13, vertex11]
vertex12.probability = {5: 0.5, 3: 0.25, 1: 0.1, 0: 0.15}

vertex13.neighbours = [vertex12, vertex14]
vertex13.probability = {4: 0.5, 3: 0.2, 2: 0.15, 1: 0.15}

vertex14.neighbours = [vertex13, vertex5, vertex15]
vertex14.probability = {0: 0.45, 1: 0.3, 4: 0.15, 5: 0.1}

vertex15.neighbours = [vertex14, vertex6]
vertex15.probability = {5: 0.5, 4: 0.15, 2: 0.15, 1: 0.2}

agent1 = Instance.Agent()
agent1.location = vertex1
agent1.movement_budget = 3
agent1.utility_budget = 6

agent2 = Instance.Agent()
agent2.location = vertex1
agent2.movement_budget = 3
agent2.utility_budget = 6

map1 = [vertex1, vertex2, vertex3, vertex4, vertex5, vertex6, vertex7, vertex8, vertex9, vertex10, vertex11, vertex12,
        vertex13, vertex14, vertex15]
agents = [agent1]

instance15 = Instance.Instance(map1, agents)

path = [[vertex1, vertex1], [vertex6, vertex2], [vertex7, vertex3], [vertex8, vertex4], [vertex9, vertex3],
        [vertex10, vertex10]]

path1 = [[vertex1, vertex1], [vertex2, vertex2], [vertex3, vertex3], [vertex10, vertex10]]

path2 = [[vertex1, vertex1], [vertex2, vertex5], [vertex7, vertex3], [vertex8, vertex4]]

path3 = [[vertex1, vertex1], [vertex6, vertex2], [vertex7, vertex3], [vertex8, vertex4], [vertex9, vertex3]]

c_path = path3
