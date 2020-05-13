# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:39:34 2020

@author: smcmlab
"""

import networkx as nx


import numpy as np


gg=[[1,2,3],[4,5,6]]


G = nx.Graph()
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 1)
G.add_edge(1, 4)
G.add_edge(4, 5)
G.add_edge(5, 6)
G.add_edge(4, 6)
nx.draw(G, pos=nx.spring_layout(G))
def modu(gg):
    nm=len(gg)
    
    G = nx.Graph()
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 1)
    G.add_edge(1, 4)
    G.add_edge(4, 5)
    G.add_edge(5, 6)
    G.add_edge(4, 6)
    l=7
    q=0
    for i in range(nm):
         H=G.subgraph(gg[i])
         ii=H.number_of_edges()
         dd=np.array(list(G.degree(gg[i])))[:,1].sum()
         q+=ii/l-(dd/2/l)**2
    
    
    return q


print(modu([list(range(1,7))]))

print(modu([[1],[2],[3],[4],[5],[6]]))
print(modu([[1,2,3,6],[4,5]]))
print(modu([[1,2,3,4],[5,6]]))
print(modu([[1,5],[2,3,4,6]]))
print(modu([[1,3,4,6],[2,5]]))
print(modu([[3,4,5,6],[2,1]]))
print(modu([[2,3,5,6],[1,4]]))
print(modu([[2,3,5,6],[1,4]]))





