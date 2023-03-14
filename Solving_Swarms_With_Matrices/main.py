import search
import mcts

'''
Results:

instance_1:
2000
('Up', 'Up', 'Right', 'Right', 'Right', 'Left', 'Down', 'Right'),
('Up', 'Up', 'Up', 'Right', 'Down', 'Down', 'Down', 'Right')
Expected value:  5.237529720703139

('Up', 'Up', 'Up', 'Right', 'Right', 'Left', 'Right', 'Right'), 
('Up', 'Up', 'Right', 'Right', 'Right', 'Left', 'Down', 'Right')
Expected value:  5.028028531875003

10000
('Up', 'Right', 'Right', 'Up', 'Right', 'Down', 'Left', 'Right'),
('Up', 'Up', 'Right', 'Up', 'Left', 'Right', 'Right', 'Right')
Expected value:  5.16769599109375

100000
('Up', 'Up', 'Right', 'Up', 'Left', 'Right', 'Right', 'Right'),
('Right', 'Up', 'Right', 'Up', 'Right', 'Down', 'Down', 'Left')
Expected value:  5.516864639140242


instance_2:

50000
('Right', 'Up', 'Up', 'Up', 'Up', 'Right', 'Right', 'Left', 'Down', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right'), 
('Right', 'Up', 'Up', 'Up', 'Up', 'Up', 'Up', 'Down', 'Left', 'Right', 'Right', 'Up', 'Left', 'Left', 'Right'), 
('Right', 'Right', 'Up', 'Right', 'Right', 'Right', 'Right', 'Up', 'Left', 'Left', 'Left', 'Left', 'Left', 'Right', 'Right'), 
('Right', 'Right', 'Up', 'Right', 'Up', 'Up', 'Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Left', 'Down', 'Right')
Expected value:  4.597215842996902

100000
('Up', 'Down', 'Right', 'Right', 'Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Left', 'Down', 'Up', 'Right', 'Right'),
('Up', 'Up', 'Up', 'Up', 'Up', 'Right', 'Up', 'Right', 'Down', 'Down', 'Down', 'Down', 'Down', 'Right', 'Right'),
('Up', 'Right', 'Right', 'Up', 'Right', 'Up', 'Right', 'Right', 'Right', 'Down', 'Down', 'Down', 'Up', 'Left', 'Right'),
('Up', 'Up', 'Up', 'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Up', 'Up', 'Right', 'Down', 'Left', 'Right')
Expected value:  4.747944231291881


instance 3:
200000
(('Up', 'Down', 'Up', 'Up', 'Up', 'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Up', 'Right', 'Right', 'Right', 'Left'),
('Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Up', 'Right', 'Right', 'Left', 'Right', 'Up', 'Down', 'Right', 'Right', 'Right', 'Left'),
('Up', 'Down', 'Right', 'Up', 'Right', 'Up', 'Up', 'Right', 'Left', 'Up', 'Right', 'Left', 'Down', 'Right', 'Right', 'Right', 'Right'),
('Up', 'Up', 'Up', 'Up', 'Right', 'Up', 'Right', 'Up', 'Left', 'Right', 'Left', 'Up', 'Left', 'Up', 'Right', 'Right', 'Right'),
('Up', 'Up', 'Up', 'Up', 'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Right', 'Right', 'Left'))
Expected value:  4.086997301255402
'''


# instance_1:
def get_instance_1():
    horizon_1 = 8
    probs_1 = {(0, 0): {'M': 0.0, 'L': 0},
               (0, 1): {'M': 0.0, 'L': 0.3},
               (0, 2): {'M': 0.4, 'L': 0.0},
               (0, 3): {'M': 0.2, 'L': 0.1},
               (1, 0): {'M': 0.0, 'L': 0.3},
               (1, 1): {'M': 0.0, 'L': 0.0},
               (1, 2): {'M': 0.6, 'L': 0.0},
               (1, 3): {'M': 0.3, 'L': 0.5},
               (2, 0): {'M': 0.0, 'L': 0.0},
               (2, 1): {'M': 0.5, 'L': 0.2},
               (2, 2): {'M': 0.0, 'L': 0.3},
               (2, 3): {'M': 0.0, 'L': 0.0},
               (3, 0): {'M': 0.1, 'L': 0.0},
               (3, 1): {'M': 0.0, 'L': 0.2},
               (3, 2): {'M': 0.8, 'L': 0.2},
               (3, 3): {'M': 0.0, 'L': 0.0}
               }
    width_1 = 4
    height_1 = 4
    pests_1 = {'M': 2, 'L': 1}
    num_of_drones_1 = 7
    num_of_swarms_1 = 2
    max_reward_1 = num_of_swarms_1 * num_of_drones_1 * sum(pests_1[p] for p in pests_1)
    requirement_1 = 150  # for A*
    gamma_1 = 0.95
    return width_1, height_1, horizon_1, pests_1, probs_1, num_of_drones_1, num_of_swarms_1, max_reward_1, \
           requirement_1, gamma_1


def get_instance_2():
    horizon_2 = 15
    probs_2 = {(0, 0): {'L': 0},
               (0, 1): {'L': 0},
               (0, 2): {'L': 0},
               (0, 3): {'L': 0},
               (0, 4): {'L': 0.05},
               (0, 5): {'L': 0.2},
               (0, 6): {'L': 0.05},
               (1, 0): {'L': 0.2},
               (1, 1): {'L': 0.05},
               (1, 2): {'L': 0.0},
               (1, 3): {'L': 0.0},
               (1, 4): {'L': 0.2},
               (1, 5): {'L': 0.5},
               (1, 6): {'L': 0.2},
               (2, 0): {'L': 0.5},
               (2, 1): {'L': 0.2},
               (2, 2): {'L': 0.05},
               (2, 3): {'L': 0.2},
               (2, 4): {'L': 0.1},
               (2, 5): {'L': 0.2},
               (2, 6): {'L': 0.05},
               (3, 0): {'L': 0.2},
               (3, 1): {'L': 0.05},
               (3, 2): {'L': 0.2},
               (3, 3): {'L': 0.5},
               (3, 4): {'L': 0.2},
               (3, 5): {'L': 0},
               (3, 6): {'L': 0},
               (4, 0): {'L': 0},
               (4, 1): {'L': 0},
               (4, 2): {'L': 0.05},
               (4, 3): {'L': 0.2},
               (4, 4): {'L': 0.05},
               (4, 5): {'L': 0},
               (4, 6): {'L': 0},
               (5, 0): {'L': 0},
               (5, 1): {'L': 0.05},
               (5, 2): {'L': 0.2},
               (5, 3): {'L': 0.05},
               (5, 4): {'L': 0},
               (5, 5): {'L': 0.05},
               (5, 6): {'L': 0.2},
               (6, 0): {'L': 0},
               (6, 1): {'L': 0.2},
               (6, 2): {'L': 0.5},
               (6, 3): {'L': 0.2},
               (6, 4): {'L': 0},
               (6, 5): {'L': 0.2},
               (6, 6): {'L': 0.5}

               }
    width_2 = 7
    height_2 = 7
    pests_2 = {'L': 1}
    num_of_drones_2 = 10
    num_of_swarms_2 = 4
    max_reward_2 = num_of_swarms_2 * num_of_drones_2 * sum(pests_2[p] for p in pests_2)
    requirement_2 = 150  # for A*
    gamma_2 = 0.98
    return width_2, height_2, horizon_2, pests_2, probs_2, num_of_drones_2, num_of_swarms_2, max_reward_2, \
           requirement_2, gamma_2


def get_instance_3():
    horizon = 17
    probs = {
                (0, 0): {'L': 0},
                (0, 1): {'L': 0},
                (0, 2): {'L': 0.3},
                (0, 3): {'L': 0.7},
                (0, 4): {'L': 0},
                (0, 5): {'L': 0},
                (0, 6): {'L': 0},
                (0, 7): {'L': 0},
                (0, 8): {'L': 0},
                (0, 9): {'L': 0},
                (0, 10): {'L': 0},
                (0, 11): {'L': 0},
                (1, 0): {'L': 0},
                (1, 1): {'L': 0},
                (1, 2): {'L': 0},
                (1, 3): {'L': 0},
                (1, 4): {'L': 0},
                (1, 5): {'L': 0},
                (1, 6): {'L': 0},
                (1, 7): {'L': 0},
                (1, 8): {'L': 0},
                (1, 9): {'L': 0},
                (1, 10): {'L': 0},
                (1, 11): {'L': 0.3},
                (2, 0): {'L': 0},
                (2, 1): {'L': 0},
                (2, 2): {'L': 0},
                (2, 3): {'L': 0},
                (2, 4): {'L': 0},
                (2, 5): {'L': 0},
                (2, 6): {'L': 0.7},
                (2, 7): {'L': 0},
                (2, 8): {'L': 0},
                (2, 9): {'L': 0.7},
                (2, 10): {'L': 0.7},
                (2, 11): {'L': 0},
                (3, 0): {'L': 0},
                (3, 1): {'L': 0},
                (3, 2): {'L': 0.5},
                (3, 3): {'L': 0},
                (3, 4): {'L': 0},
                (3, 5): {'L': 0.5},
                (3, 6): {'L': 0},
                (3, 7): {'L': 0},
                (3, 8): {'L': 0},
                (3, 9): {'L': 0},
                (3, 10): {'L': 0.3},
                (3, 11): {'L': 0},
                (4, 0): {'L': 0},
                (4, 1): {'L': 0},
                (4, 2): {'L': 0},
                (4, 3): {'L': 0},
                (4, 4): {'L': 0.3},
                (4, 5): {'L': 0},
                (4, 6): {'L': 0},
                (4, 7): {'L': 0},
                (4, 8): {'L': 0},
                (4, 9): {'L': 0},
                (4, 10): {'L': 0},
                (4, 11): {'L': 0},
                (5, 0): {'L': 0},
                (5, 1): {'L': 0},
                (5, 2): {'L': 0},
                (5, 3): {'L': 0},
                (5, 4): {'L': 0.3},
                (5, 5): {'L': 0},
                (5, 6): {'L': 0},
                (5, 7): {'L': 0},
                (5, 8): {'L': 0},
                (5, 9): {'L': 0},
                (5, 10): {'L': 0},
                (5, 11): {'L': 0},
                (6, 0): {'L': 0},
                (6, 1): {'L': 0},
                (6, 2): {'L': 0},
                (6, 3): {'L': 0},
                (6, 4): {'L': 0},
                (6, 5): {'L': 0.7},
                (6, 6): {'L': 0.3},
                (6, 7): {'L': 0},
                (6, 8): {'L': 0},
                (6, 9): {'L': 0},
                (6, 10): {'L': 0},
                (6, 11): {'L': 0},
                (7, 0): {'L': 0},
                (7, 1): {'L': 0},
                (7, 2): {'L': 0},
                (7, 3): {'L': 0},
                (7, 4): {'L': 0},
                (7, 5): {'L': 0},
                (7, 6): {'L': 0},
                (7, 7): {'L': 0},
                (7, 8): {'L': 0.5},
                (7, 9): {'L': 0},
                (7, 10): {'L': 0},
                (7, 11): {'L': 0},
                (8, 0): {'L': 0},
                (8, 1): {'L': 0},
                (8, 2): {'L': 0},
                (8, 3): {'L': 0},
                (8, 4): {'L': 0},
                (8, 5): {'L': 0},
                (8, 6): {'L': 0},
                (8, 7): {'L': 0},
                (8, 8): {'L': 0},
                (8, 9): {'L': 0},
                (8, 10): {'L': 0.3},
                (8, 11): {'L': 0},
                (9, 0): {'L': 0.5},
                (9, 1): {'L': 0},
                (9, 2): {'L': 0},
                (9, 3): {'L': 0},
                (9, 4): {'L': 0},
                (9, 5): {'L': 0},
                (9, 6): {'L': 0},
                (9, 7): {'L': 0},
                (9, 8): {'L': 0},
                (9, 9): {'L': 0},
                (9, 10): {'L': 0},
                (9, 11): {'L': 0},
                (10, 0): {'L': 0},
                (10, 1): {'L': 0},
                (10, 2): {'L': 0},
                (10, 3): {'L': 0.7},
                (10, 4): {'L': 0},
                (10, 5): {'L': 0},
                (10, 6): {'L': 0},
                (10, 7): {'L': 0},
                (10, 8): {'L': 0},
                (10, 9): {'L': 0},
                (10, 10): {'L': 0},
                (10, 11): {'L': 0},
                (11, 0): {'L': 0},
                (11, 1): {'L': 0},
                (11, 2): {'L': 0},
                (11, 3): {'L': 0},
                (11, 4): {'L': 0.7},
                (11, 5): {'L': 0},
                (11, 6): {'L': 0.3},
                (11, 7): {'L': 0.3},
                (11, 8): {'L': 0},
                (11, 9): {'L': 0.5},
                (11, 10): {'L': 0},
                (11, 11): {'L': 0}
             }
    width = 9
    height = 9
    pests = {'L': 1}
    num_of_drones = 10
    num_of_swarms = 5
    max_reward = round(sum(probs[a]['L'] for a in probs)+0.99)
    print(max_reward)
    requirement = 150  # for A*
    gamma = 0.99
    return width, height, horizon, pests, probs, num_of_drones, num_of_swarms, max_reward, \
           requirement, gamma


# problem = search.SingleSwarmProblem(HOR, size_x, size_y, pests_1, probs3, max_reward, num_of_drones)
problem = search.MultiSwarmProblem(*get_instance_2())

mcts.monte_carlo_tree_search(problem, 200000)
# search.astar_search(problem, problem.h)
