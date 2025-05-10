from skimage.morphology import skeletonize
from skimage import data
import matplotlib.pyplot as plt
from skimage.util import invert
import numpy as np
from PIL import Image
import networkx as nx
from random import choice

#Literally all I had to do was add .convert("L") and remove the invert
image = (np.array(Image.open("maze_large.png").convert("L")))
# perform skeletonization
skeleton = skeletonize(image)
g = nx.Graph()
for i in range(len(skeleton)):
    for j in range(len(skeleton[i])):
        for n in [(i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i+1, j+1), (i-1, j+1), (i+1, j-1)]:
            if n[0] > 0 and n[1] > 0 and n[0] < len(skeleton) and n[1] < len(skeleton[i]):
                if skeleton[i][j] and skeleton[n[0]][n[1]]:
                    g.add_edge((i, j), n)
print()
clone = np.array(skeleton)
allowed_x = set()
allowed_y = set()
for node in g:
    if (node[0], node[1]+1) in g:
        allowed_x.add(node[0])
    if (node[0]+1, node[1]) in g:
        allowed_y.add(node[1])

for x in list(allowed_x):
    try:
        allowed_x.remove(x+1)
    except:
        pass
for y in list(allowed_y):
    try:
        allowed_y.remove(y+1)
    except:
        pass


allowed_x = sorted(list(allowed_x))
allowed_y = sorted(list(allowed_y))

print(allowed_x)
print(allowed_y)
#Compute average pixel distances in allowed_x and _y (for adding nodes to g2)
avg_dist = 0
for i in range(len(allowed_x)-1):
    avg_dist += allowed_x[i+1]-allowed_x[i]

for i in range(len(allowed_y)-1):
    avg_dist += allowed_y[i+1]-allowed_y[i]

avg_dist /= len(allowed_x)-1 + len(allowed_y)-1
print(avg_dist)

g2 = nx.Graph()

#Prepare g and g2
#Prevents nx.NodeNotFound in g in next step
for i in allowed_x:
    for j in allowed_y:
        g2.add_node((i, j))
        for n in [(i-1, j), (i+1, j), (i, j-1), (i, j+1), (i-1, j-1), (i+1, j+1), (i-1, j+1), (i+1, j-1)]:
            if n in g:
                g.add_edge((i, j), n)
#Add edges to g2 based on if they are connected in g with path length less than the pixel length of each edge (g is in pixels)
for i in range(len(allowed_x)):
    print(f"{i} x: {allowed_x[i]}")
    for j in range(len(allowed_y)):
        try:
            n1, n2 = (allowed_x[i],allowed_y[j]), (allowed_x[i-1],allowed_y[j])
            if nx.shortest_path_length(g, n1, n2) < avg_dist:
                g2.add_edge(n1, n2)
        except IndexError:
            pass
        except nx.NetworkXNoPath:
            pass
        try:
            n1, n2 = (allowed_x[i],allowed_y[j]), (allowed_x[i+1],allowed_y[j])
            if nx.shortest_path_length(g, n1, n2) < avg_dist:
                g2.add_edge(n1, n2)
        except IndexError:
            pass
        except nx.NetworkXNoPath:
            pass
        try:
            n1, n2 = (allowed_x[i],allowed_y[j]), (allowed_x[i],allowed_y[j-1])
            if nx.shortest_path_length(g, n1, n2) < avg_dist:
                g2.add_edge(n1, n2)
        except IndexError:
            pass
        except nx.NetworkXNoPath:
            pass
        try:
            n1, n2 = (allowed_x[i],allowed_y[j]), (allowed_x[i],allowed_y[j+1])
            if nx.shortest_path_length(g, n1, n2) < avg_dist:
                g2.add_edge(n1, n2)
        except IndexError:
            pass
        except nx.NetworkXNoPath:
            pass
        

print(g2)

"""
#g3 is for finding adjacent positions in g2 as it would be incredibly annoying
g3 = nx.Graph()
for i in range(len(allowed_x)):
    for j in range(len(allowed_y)):
        try:
            g3.add_edge((allowed_x[i],allowed_y[j]), (allowed_x[i-1],allowed_y[j]))
        except:
            pass
        try:
            g3.add_edge((allowed_x[i],allowed_y[j]), (allowed_x[i+1],allowed_y[j]))
        except:
            pass
        try:
            g3.add_edge((allowed_x[i],allowed_y[j]), (allowed_x[i],allowed_y[j-1]))
        except:
            pass
        try:
            g3.add_edge((allowed_x[i],allowed_y[j]), (allowed_x[i], allowed_y[j+1]))
        except:
            pass
        

print(g3)



for node1 in g2:
    for node2 in g3.adj[node1]:
        try:
            if nx.shortest_path_length(g, node1, node2) <= avg_dist:
                g2.add_edge(node1, node2)
        except nx.NetworkXNoPath:
            pass"""

while True:
    try:
        n1, n2 = (choice(sorted(list(g.nodes), key=lambda n: n[0] + n[1])[:100]), 
                  choice(sorted(list(g.nodes), key=lambda n: n[0] + n[1], reverse = True)[:100]))
        print(n1, n2)
        path = (nx.shortest_path(g, n1, n2))
        break
    except nx.NetworkXNoPath:
        pass

for node in g:
    if node not in path:
        clone[node[0]][node[1]] = 0

# display results
fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(8, 4), sharex=True, sharey=True)

ax = axes.ravel()

ax[0].imshow(image, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)

ax[1].imshow(invert(skeleton), cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('skeleton', fontsize=20)

ax[2].imshow(invert(clone), cmap=plt.cm.gray)
ax[2].axis('off')
ax[2].set_title('path', fontsize=20)


fig.tight_layout()
plt.show()
