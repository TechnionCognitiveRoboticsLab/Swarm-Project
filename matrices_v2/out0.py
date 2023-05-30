import Instance 
import MCTS
vertex0 = Instance.Vertex("v0")
vertex0.probability = {0: 1.0}
vertex1 = Instance.Vertex("v1")
vertex1.probability = {0: 0.33776022517918536, 4: 0.19847197999208482, 3: 0.11911134931775633, 2: 0.34465644551097346}
vertex2 = Instance.Vertex("v2")
vertex2.probability = {0: 0.226534776167442, 5: 0.4541014453022051, 3: 0.2820358098991651, 1: 0.03732796863118779}
vertex3 = Instance.Vertex("v3")
vertex3.probability = {0: 0.25511786073063725, 1: 0.376779487961202, 4: 0.09219292787086474, 3: 0.10507556330350007, 2: 0.170834160133796}
vertex4 = Instance.Vertex("v4")
vertex4.probability = {0: 1.0}
vertex5 = Instance.Vertex("v5")
vertex5.probability = {0: 1.0}
vertex6 = Instance.Vertex("v6")
vertex6.probability = {0: 0.2669184265330796, 4: 0.17717558917855084, 3: 0.22761045784073805, 6: 0.012476344086483527, 5: 0.3127830631003814, 1: 0.0030361192607665276}
vertex7 = Instance.Vertex("v7")
vertex7.probability = {0: 0.23331137092161114, 5: 0.2551770195622843, 6: 0.32012932945730954, 1: 0.007772589633797031, 4: 0.18360969042499795}
vertex8 = Instance.Vertex("v8")
vertex8.probability = {0: 0.12439272557819292, 4: 0.5969222320172958, 2: 0.04986168589570532, 6: 0.22882335650880598}
vertex9 = Instance.Vertex("v9")
vertex9.probability = {0: 1.0}
vertex10 = Instance.Vertex("v10")
vertex10.probability = {0: 0.38918103154141653, 5: 0.6108189684585834}
vertex11 = Instance.Vertex("v11")
vertex11.probability = {0: 0.47677732400354933, 6: 0.14870429524382364, 5: 0.3745183807526269}
vertex12 = Instance.Vertex("v12")
vertex12.probability = {0: 0.7075052364706764, 2: 0.2924947635293236}
vertex13 = Instance.Vertex("v13")
vertex13.probability = {0: 0.4637972458436169, 6: 0.30574686492002734, 3: 0.08378193837610248, 4: 0.1466739508602533}
vertex14 = Instance.Vertex("v14")
vertex14.probability = {0: 0.6083986582899477, 1: 0.39160134171005234}
vertex15 = Instance.Vertex("v15")
vertex15.probability = {0: 0.30084792636472785, 6: 0.12328896023424656, 5: 0.27878959135179376, 1: 0.2970735220492319}
vertex16 = Instance.Vertex("v16")
vertex16.probability = {0: 0.4750559519239985, 1: 0.1335491338617789, 2: 0.20796650817899773, 4: 0.18342840603522492}
vertex17 = Instance.Vertex("v17")
vertex17.probability = {0: 0.6185480381646372, 4: 0.3814519618353628}
vertex18 = Instance.Vertex("v18")
vertex18.probability = {0: 0.1335951562617648, 6: 0.49835810469953745, 3: 0.26353540376928125, 5: 0.01149503252710951, 2: 0.09301630274230704}
vertex19 = Instance.Vertex("v19")
vertex19.probability = {0: 0.2196433718572148, 4: 0.6381355065786668, 2: 0.1422211215641185}
vertex20 = Instance.Vertex("v20")
vertex20.probability = {0: 0.5016240216803185, 1: 0.24511870018799284, 2: 0.21721404257101054, 3: 0.036043235560678205}
vertex21 = Instance.Vertex("v21")
vertex21.probability = {0: 0.12674943884256543, 6: 0.432129518468543, 1: 0.32302581496342675, 4: 0.09976910677023694, 5: 0.01832612095522794}
vertex22 = Instance.Vertex("v22")
vertex22.probability = {0: 0.24298168602397607, 1: 0.22963399827241354, 2: 0.38799423363913443, 6: 0.13939008206447617}
vertex23 = Instance.Vertex("v23")
vertex23.probability = {0: 0.28632644451329053, 1: 0.19323655253538527, 4: 0.1629694256304588, 2: 0.35746757732086537}
vertex24 = Instance.Vertex("v24")
vertex24.probability = {0: 0.6562431177682162, 2: 0.3437568822317838}
vertex0.neighbours = [vertex5, vertex1]
vertex1.neighbours = [vertex0, vertex6, vertex2]
vertex2.neighbours = [vertex1, vertex7, vertex3]
vertex3.neighbours = [vertex2, vertex8, vertex4]
vertex4.neighbours = [vertex3, vertex9]
vertex5.neighbours = [vertex0, vertex10, vertex6]
vertex6.neighbours = [vertex1, vertex5, vertex11, vertex7]
vertex7.neighbours = [vertex2, vertex6, vertex12, vertex8]
vertex8.neighbours = [vertex3, vertex7, vertex13, vertex9]
vertex9.neighbours = [vertex4, vertex8, vertex14]
vertex10.neighbours = [vertex5, vertex15, vertex11]
vertex11.neighbours = [vertex6, vertex10, vertex16, vertex12]
vertex12.neighbours = [vertex7, vertex11, vertex17, vertex13]
vertex13.neighbours = [vertex8, vertex12, vertex18, vertex14]
vertex14.neighbours = [vertex9, vertex13, vertex19]
vertex15.neighbours = [vertex10, vertex20, vertex16]
vertex16.neighbours = [vertex11, vertex15, vertex21, vertex17]
vertex17.neighbours = [vertex12, vertex16, vertex22, vertex18]
vertex18.neighbours = [vertex13, vertex17, vertex23, vertex19]
vertex19.neighbours = [vertex14, vertex18, vertex24]
vertex20.neighbours = [vertex15, vertex21]
vertex21.neighbours = [vertex16, vertex20, vertex22]
vertex22.neighbours = [vertex17, vertex21, vertex23]
vertex23.neighbours = [vertex18, vertex22, vertex24]
vertex24.neighbours = [vertex19, vertex23]
agent0 = Instance.Agent()
agent0.location = vertex15
agent0.movement_budget = 5
agent0.utility_budget = 10
map1 = [vertex0,vertex1,vertex2,vertex3,vertex4,vertex5,vertex6,vertex7,vertex8,vertex9,vertex10,vertex11,vertex12,vertex13,vertex14,vertex15,vertex16,vertex17,vertex18,vertex19,vertex20,vertex21,vertex22,vertex23,vertex24]
agents = [agent0]
instance1 = Instance.Instance(map1, agents, 5, 5)