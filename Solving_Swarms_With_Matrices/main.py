import search
import mcts

'''
Results:

instance_1:

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

'''


# instance_1:
def get_instance_1():
    horizon_1 = 8
    probs_1 = {'a11': {'M': 0.0, 'L': 0},
               'a12': {'M': 0.0, 'L': 0.3},
               'a13': {'M': 0.4, 'L': 0.0},
               'a14': {'M': 0.2, 'L': 0.1},
               'a21': {'M': 0.0, 'L': 0.3},
               'a22': {'M': 0.0, 'L': 0.0},
               'a23': {'M': 0.6, 'L': 0.0},
               'a24': {'M': 0.3, 'L': 0.5},
               'a31': {'M': 0.0, 'L': 0.0},
               'a32': {'M': 0.5, 'L': 0.2},
               'a33': {'M': 0.0, 'L': 0.3},
               'a34': {'M': 0.0, 'L': 0.0},
               'a41': {'M': 0.1, 'L': 0.0},
               'a42': {'M': 0.0, 'L': 0.2},
               'a43': {'M': 0.8, 'L': 0.2},
               'a44': {'M': 0.0, 'L': 0.0}
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
    probs_2 = {'a11': {'L': 0},
               'a12': {'L': 0},
               'a13': {'L': 0},
               'a14': {'L': 0},
               'a15': {'L': 0.05},
               'a16': {'L': 0.2},
               'a17': {'L': 0.05},
               'a21': {'L': 0.2},
               'a22': {'L': 0.05},
               'a23': {'L': 0.0},
               'a24': {'L': 0.0},
               'a25': {'L': 0.2},
               'a26': {'L': 0.5},
               'a27': {'L': 0.2},
               'a31': {'L': 0.5},
               'a32': {'L': 0.2},
               'a33': {'L': 0.05},
               'a34': {'L': 0.2},
               'a35': {'L': 0.1},
               'a36': {'L': 0.2},
               'a37': {'L': 0.05},
               'a41': {'L': 0.2},
               'a42': {'L': 0.05},
               'a43': {'L': 0.2},
               'a44': {'L': 0.5},
               'a45': {'L': 0.2},
               'a46': {'L': 0},
               'a47': {'L': 0},
               'a51': {'L': 0},
               'a52': {'L': 0},
               'a53': {'L': 0.05},
               'a54': {'L': 0.2},
               'a55': {'L': 0.05},
               'a56': {'L': 0},
               'a57': {'L': 0},
               'a61': {'L': 0},
               'a62': {'L': 0.05},
               'a63': {'L': 0.2},
               'a64': {'L': 0.05},
               'a65': {'L': 0},
               'a66': {'L': 0.05},
               'a67': {'L': 0.2},
               'a71': {'L': 0},
               'a72': {'L': 0.2},
               'a73': {'L': 0.5},
               'a74': {'L': 0.2},
               'a75': {'L': 0},
               'a76': {'L': 0.2},
               'a77': {'L': 0.5}

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
    probs = {"a11": {'L': 0},
             "a12": {'L': 0},
             "a13": {'L': 0.3},
             "a14": {'L': 0.7},
             "a15": {'L': 0},
             "a16": {'L': 0},
             "a17": {'L': 0},
             "a18": {'L': 0},
             "a19": {'L': 0},
             "a110": {'L': 0},
             "a111": {'L': 0},
             "a112": {'L': 0},
             "a21": {'L': 0},
             "a22": {'L': 0},
             "a23": {'L': 0},
             "a24": {'L': 0},
             "a25": {'L': 0},
             "a26": {'L': 0},
             "a27": {'L': 0},
             "a28": {'L': 0},
             "a29": {'L': 0},
             "a210": {'L': 0},
             "a211": {'L': 0},
             "a212": {'L': 0.3},
             "a31": {'L': 0},
             "a32": {'L': 0},
             "a33": {'L': 0},
             "a34": {'L': 0},
             "a35": {'L': 0},
             "a36": {'L': 0},
             "a37": {'L': 0.7},
             "a38": {'L': 0},
             "a39": {'L': 0},
             "a310": {'L': 0.7},
             "a311": {'L': 0.7},
             "a312": {'L': 0},
             "a41": {'L': 0},
             "a42": {'L': 0},
             "a43": {'L': 0.5},
             "a44": {'L': 0},
             "a45": {'L': 0},
             "a46": {'L': 0.5},
             "a47": {'L': 0},
             "a48": {'L': 0},
             "a49": {'L': 0},
             "a410": {'L': 0},
             "a411": {'L': 0.3},
             "a412": {'L': 0},
             "a51": {'L': 0},
             "a52": {'L': 0},
             "a53": {'L': 0},
             "a54": {'L': 0},
             "a55": {'L': 0.3},
             "a56": {'L': 0},
             "a57": {'L': 0},
             "a58": {'L': 0},
             "a59": {'L': 0},
             "a510": {'L': 0},
             "a511": {'L': 0},
             "a512": {'L': 0},
             "a61": {'L': 0},
             "a62": {'L': 0},
             "a63": {'L': 0},
             "a64": {'L': 0},
             "a65": {'L': 0.3},
             "a66": {'L': 0},
             "a67": {'L': 0},
             "a68": {'L': 0},
             "a69": {'L': 0},
             "a610": {'L': 0},
             "a611": {'L': 0},
             "a612": {'L': 0},
             "a71": {'L': 0},
             "a72": {'L': 0},
             "a73": {'L': 0},
             "a74": {'L': 0},
             "a75": {'L': 0},
             "a76": {'L': 0.7},
             "a77": {'L': 0.3},
             "a78": {'L': 0},
             "a79": {'L': 0},
             "a710": {'L': 0},
             "a711": {'L': 0},
             "a712": {'L': 0},
             "a81": {'L': 0},
             "a82": {'L': 0},
             "a83": {'L': 0},
             "a84": {'L': 0},
             "a85": {'L': 0},
             "a86": {'L': 0},
             "a87": {'L': 0},
             "a88": {'L': 0},
             "a89": {'L': 0.5},
             "a810": {'L': 0},
             "a811": {'L': 0},
             "a812": {'L': 0},
             "a91": {'L': 0},
             "a92": {'L': 0},
             "a93": {'L': 0},
             "a94": {'L': 0},
             "a95": {'L': 0},
             "a96": {'L': 0},
             "a97": {'L': 0},
             "a98": {'L': 0},
             "a99": {'L': 0},
             "a910": {'L': 0},
             "a911": {'L': 0.3},
             "a912": {'L': 0},
             "a101": {'L': 0.5},
             "a102": {'L': 0},
             "a103": {'L': 0},
             "a104": {'L': 0},
             "a105": {'L': 0},
             "a106": {'L': 0},
             "a107": {'L': 0},
             "a108": {'L': 0},
             "a109": {'L': 0},
             "a1010": {'L': 0},
             "a1011": {'L': 0},
             "a1012": {'L': 0},
             "a111": {'L': 0},
             "a112": {'L': 0},
             "a113": {'L': 0},
             "a114": {'L': 0.7},
             "a115": {'L': 0},
             "a116": {'L': 0},
             "a117": {'L': 0},
             "a118": {'L': 0},
             "a119": {'L': 0},
             "a1110": {'L': 0},
             "a1111": {'L': 0},
             "a1112": {'L': 0},
             "a121": {'L': 0},
             "a122": {'L': 0},
             "a123": {'L': 0},
             "a124": {'L': 0},
             "a125": {'L': 0.7},
             "a126": {'L': 0},
             "a127": {'L': 0.3},
             "a128": {'L': 0.3},
             "a129": {'L': 0},
             "a1210": {'L': 0.5},
             "a1211": {'L': 0},
             "a1212": {'L': 0}
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
problem = search.MultiSwarmProblem(*get_instance_3())

mcts.monte_carlo_tree_search(problem, 50000)
# search.astar_search(problem, problem.h)
