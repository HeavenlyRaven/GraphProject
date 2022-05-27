import random
import timeit

import matplotlib.pyplot as plt
import networkx as nx

from src.graph import Graph
from src.landmarks import Landmarks

Gnx = nx.read_edgelist('testGraph.txt', comments='#')
G = Graph("testGraph.txt")

rang = range(1, 10)

rTime = []
hdTime = []
bcTime = []

missBasicR = []
missLcaR = []

timeBasicR = []
timeLcaR = []

missBasicHd = []
missLcaHd = []

timeBasicHd = []
timeLcaHd = []

missBasicBc = []
missLcaBc = []

timeBasicBc = []
timeLcaBc = []

for i in range(1, 10):
    print(i)
    start_time = timeit.default_timer()
    r = Landmarks(G, i, method='r')
    rTime.append(timeit.default_timer() - start_time)

    start_time = timeit.default_timer()
    hd = Landmarks(G, i, method='hd')
    hdTime.append(timeit.default_timer() - start_time)

    start_time = timeit.default_timer()
    bc = Landmarks(G, i, method='bc')
    bcTime.append(timeit.default_timer() - start_time)

    missBasic = 0
    missLca = 0

    timeBasic = 0
    timeLca = 0

    for i in range(1, 1000):
        vertices = G.vertices()
        num_to_select = 2
        list_of_random_items = random.sample(vertices, num_to_select)
        first_random_item = list_of_random_items[0]
        second_random_item = list_of_random_items[1]

        start_time = timeit.default_timer()
        path_basic = r.landmarks_basic(first_random_item, second_random_item)
        timeBasic = timeBasic + (timeit.default_timer() - start_time)

        start_time = timeit.default_timer()
        path_lca = r.landmarks_lca(first_random_item, second_random_item)
        timeLca = timeLca + (timeit.default_timer() - start_time)

        actual_path = nx.dijkstra_path_length(Gnx, first_random_item, second_random_item)

        if (actual_path != path_basic):
            missBasic = missBasic + 1

        if (actual_path != path_lca):
            missLca = missLca + 1

    missBasicR.append(missBasic)
    missLcaR.append(missLca)

    timeBasicR.append(timeBasic / 1000)
    timeLcaR.append(timeLca / 1000)

    missBasic = 0
    missLca = 0

    timeBasic = 0
    timeLca = 0

    for i in range(1, 1000):
        vertices = G.vertices()
        num_to_select = 2
        list_of_random_items = random.sample(vertices, num_to_select)
        first_random_item = list_of_random_items[0]
        second_random_item = list_of_random_items[1]

        start_time = timeit.default_timer()
        path_basic = hd.landmarks_basic(first_random_item, second_random_item)
        timeBasic = timeBasic + (timeit.default_timer() - start_time)

        start_time = timeit.default_timer()
        path_lca = hd.landmarks_lca(first_random_item, second_random_item)
        timeLca = timeLca + (timeit.default_timer() - start_time)

        actual_path = nx.dijkstra_path_length(Gnx, first_random_item, second_random_item)

        if (actual_path != path_basic):
            missBasic = missBasic + 1

        if (actual_path != path_lca):
            missLca = missLca + 1

    missBasicHd.append(missBasic)
    missLcaHd.append(missLca)

    timeBasicHd.append(timeBasic / 1000)
    timeLcaHd.append(timeLca / 1000)

    missBasic = 0
    missLca = 0

    timeBasic = 0
    timeLca = 0

    for i in range(1, 1000):
        vertices = G.vertices()
        num_to_select = 2
        list_of_random_items = random.sample(vertices, num_to_select)
        first_random_item = list_of_random_items[0]
        second_random_item = list_of_random_items[1]

        start_time = timeit.default_timer()
        path_basic = bc.landmarks_basic(first_random_item, second_random_item)
        timeBasic = timeBasic + (timeit.default_timer() - start_time)

        start_time = timeit.default_timer()
        path_lca = bc.landmarks_lca(first_random_item, second_random_item)
        timeLca = timeLca + (timeit.default_timer() - start_time)

        actual_path = nx.dijkstra_path_length(Gnx, first_random_item, second_random_item)

        if (actual_path != path_basic):
            missBasic = missBasic + 1

        if (actual_path != path_lca):
            missLca = missLca + 1

    missBasicBc.append(missBasic)
    missLcaBc.append(missLca)

    timeBasicBc.append(timeBasic / 1000)
    timeLcaBc.append(timeLca / 1000)

plt.plot(rang, missBasicBc)
plt.plot(rang, missLcaBc)
plt.xlabel("Количество лэндмарок")
plt.ylabel("Количество промахов")
plt.show()
