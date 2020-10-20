import networkx as nx #Library used to work with GML files
import math

#GML Network name to be converted
#Has to be in same directory as .py file for now
#network = 'Arpanet196912'
network = 'Aarnet'
#network = 'Aconet'

#Initialising the GML reader
G = nx.read_gml(network + '.gml')
nodes_count = len(G.nodes)
edges_count = len(G.edges)
nodes_raw = list(G.nodes(data = True))
edges_raw = list(G.edges)


#x,y offset/center, spacing and ray size
xs = 600
ys = 600
r = 500
tspace = 50

#Needed variables
nodes = []
nodes_label = {}
nodes_cords = {}
transitions = []
transitions_label = {}
ntc = {}

for i in range(nodes_count):
    nodes.append(nodes_raw[i][0])
    nodes_label[nodes_raw[i][0]] = "P" + str(i)
    ntc["P" + str(i)] = 0

for i in range(edges_count):
    source, target = nodes_label[edges_raw[i][0]], nodes_label[edges_raw[i][1]]
    transitions.append((source, target))
    transitions_label[(source, target)] = "T" + str(i)

def rgen(x, ray):
    alpha = 2 * math.pi * x / nodes_count
    return (int(math.cos(alpha) * ray) + xs, int(math.sin(alpha) * ray) + ys)

for x in range(nodes_count):
    nodes_cords[nodes_label[nodes[x]]] = rgen(x, r)

#Transition rotation
def slope(x0, x1, y0, y1):
    return (int(math.degrees(math.atan2((y1-y0),(x1-x0)))))

def tran_locator(x, y, t):
    ntc[t] +=1
    print(ntc[t], " ", r, " ", ntc[t]*tspace)
    #x0 = int(int((x - xs) / r) * (r - ntc[t]*tspace)) + xs
    #y0 = int(int((y - ys) / r) * (r - ntc[t]*tspace)) + ys
    a, b = rgen(int(t[1:]), r-ntc[t]*tspace)
    return (a, b)
    
#Writing to file
f = open(network + "_v3.tapn", "w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")
f.write("  <net active=\"true\" id=\"" + network + "\" type=\"P/T net\">\n")

##### PART I: NODES
for i in range (nodes_count):
    x, y = nodes_cords[nodes_label[nodes[i]]]
    f.write("    <place displayName=\"true\" id=\"" + nodes_label[nodes[i]] + "\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"" + nodes_label[nodes[i]] + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str(x) + "\" positionY=\"" + str(y) + "\"/>\n")

#### PART II: TRANSITIONS

for i in range (edges_count):
    source, target = transitions[i]
    x0, y0 = nodes_cords[source]
    x, y = tran_locator(x0, y0, source)
    print(x, " ", y)
    f.write("    <transition angle=\"" + str(slope(x0, xs, y0, ys)) + "\" displayName=\"true\" id=\"" + "T" + str(i) + "\" infiniteServer=\"false\" name=\"" + "T" + str(i) + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str(x) + "\" positionY=\"" + str(y) + "\" priority=\"0\" urgent=\"false\"/>\n")


print(ntc)
#File writing ending part
f.write("  </net>\n")
f.write("  <k-bound bound=\"3\"/>\n")
f.write("</pnml>")
f.close()

#Very nice success message
print("Done! " + network + " converted to " + network + "_v3.tpn!")
#No error message in case it doesn't work
#because that's not a posibility :^)
