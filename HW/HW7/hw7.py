import numpy as np
import pandas as pd
import scipy.io
import matplotlib.pyplot as plt
import community
import networkx as nx
loc = scipy.io.loadmat('data\XYZcoord1.mat')
loc = np.array(loc['XYZ1'])
distance = []
for i in range(len(loc)):
    for j in range(i+1,len(loc)):
        temp = 0
        for k in range(3):
            temp += (loc[i,k] - loc[j,k])**2
        distance.append(1/(temp**0.5 +1e-9)**0.5)
#%%
H = nx.Graph()
for i in range(len(loc)):
    for j in range(i+1,len(loc)):
        f = ( str(i),str(j), distance[j] )
        H.add_weighted_edges_from([(f)])
        #%%
partition2 = community.best_partition(H)
size = float(len(set(partition2.values())))
print("euc_community:", size)
mod = community.modularity(partition2,H)
print("euc_modularity:", mod)
#%%
for com2 in set(partition2.values()) :
    members2 = list_nodes2 = [nodes2 for nodes2 in partition2.keys() if partition2[nodes2] == com2]
values2 = [partition2.get(node2) for node2 in H.nodes()]
nx.draw_spring(H, cmap = plt.get_cmap('jet'), node_color = values2, node_size = 30, with_labels = False)
#%%
label2 = np.zeros((len(loc),1))
for j in set(partition2.values()) :
    for i in range(len(loc)) :
        if partition2[str(i)] == j :            
            label2[i] =  j
label2 = np.reshape(label2, len(loc))
fig = plt.figure()
ax = plt.axes(projection='3d')
x = loc[:,0]
y = loc[:,1]
z = loc[:,2]
ax1=ax.scatter(x, y, z, c = label2, cmap = plt.get_cmap('jet'))
ax.view_init(90, 0)
fig.colorbar(ax1)