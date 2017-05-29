from pymystem3 import Mystem
import re
import networkx as nx
import matplotlib.pyplot as plt

mystem = Mystem()
G = nx.Graph()

f = open('comments_all.txt', 'r', encoding = 'utf-8')
a = f.read()
r = '[a-z]'
s = re.sub(r, '', a)
lemma = mystem.lemmatize(s)
analysis = mystem.analyze(s)

reg = 'PR=|CONJ=|APRO=*|PART='

t = 0
p = []
for item in analysis:
    if type(analysis[t]) == dict:
        analysis_key = 'analysis' in analysis[t]
        if analysis_key == True and analysis[t]['analysis'] != []:
            if not re.search(reg, analysis[t]['analysis'][0]['gr']):
                p.append(analysis[t]['analysis'][0]['lex'])
    t += 1

#creating a graph

G.add_nodes_from(p)

y = 0
while y < len(p)-3:
    G.add_edges_from([(p[y],p[y+1]),(p[y],p[y+2]),(p[y],p[y+3])], size=500)
    y += 1

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color = "red", node_size = 20)
nx.draw_networkx_edges(G, pos, edge_color = "yellow")
nx.draw_networkx_labels(G,pos,font_size = 10)
plt.axis("off")
plt.show()
plt.savefig("comment_graph.png")

#printing charachteristicsc
print('radius',nx.radius(G))
print('diameter',nx.diameter(G))
print('nodes#',G.number_of_nodes())
print('edges#',G.number_of_edges())
print('density',nx.density(G))
print('pearson',nx.degree_pearson_correlation_coefficient(G))

deg = nx.degree_centrality(G)
for nodeid in sorted(deg, key=deg.get, reverse=True):
    print(nodeid)

print('clust',nx.average_clustering(G))
print('trans',nx.transitivity(G))

