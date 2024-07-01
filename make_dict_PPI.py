import os
import sys
import pandas as pd
import numpy as np
import networkx as nx
import multiprocessing
import itertools
from functools import partial
sys.path.append('./utils/')

from guney_code import wrappers
from guney_code import network_utilities
from guney_code import network_utils
import separation as tools

###计算两个node的最短距离
def calculate_closest_distance(network, from_to_list):
    node_from = from_to_list[0]
    node_to = from_to_list[1]
    val = network_utilities.get_shortest_path_length_between(network, node_from, node_to)
###写入文件函数
    with open(filename,'a') as f:
        f.write(str(node_from) + '\t'+ str(node_to)+ '\t' + str(val) + "\n")

###读取network
network_file = 'data/DatasetS2.csv'

df = pd.read_csv(network_file)
#del df['databases']
#dt = np.unique(np.append(df['proteinA_entrezid'].unique(),df['proteinB_entrezid'].unique()))
G = tools.read_network(network_file)

# filter for nodes in lcc of G
components = nx.connected_components(G)
lcclist = sorted(list(components), key = len, reverse=True)
G1 = nx.subgraph(G, lcclist[0])
all_nodes = list(G1.nodes)
combinations = list(itertools.combinations(all_nodes, 2))
#test = combinations[0:10]
filename= 'DatasetS2_shortest_distance.txt'
###创建线程
pool = multiprocessing.Pool()
func = partial(calculate_closest_distance,G1)
res = pool.map(func,combinations)

pool.close()
