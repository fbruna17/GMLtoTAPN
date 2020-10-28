import networkx as nx  # Library used to work with GML files
import math

# GML Network name to be converted
# Has to be in same directory as .py file for now
# network = 'Arpanet196912'
network = 'GtsCe'
# network = 'Aarnet'
# network = 'Aconet'

# Initialising the GML reader
G = nx.read_gml(network + '.gml', label='id')

nodes_count = len(G.nodes)
edges_count = len(G.edges)
nodes_raw = list(G.nodes(data=True))
edges_raw = list(G.edges)

# Starting point of the drawing and spacing between places
xs = 200
ys = 200
pad = 200

# Needed variables
nodes = []
nodes_label = {}
nodes_cords = {}
transitions = []
transitions_label = {}

for i in range (nodes_count):
    nodes.append(nodes_raw[i][0])
    if nodes_raw[i][1]['label'] == "None":
        nodes_raw[i][1]['label'] = "P" + str(i)

for i in range(nodes_count):
    nodes.append(nodes_raw[i][0])
    nodes_label[nodes_raw[i][0]] = nodes_raw[i][1]['label'].upper().replace(",", "").replace(" ", "")

for i in range(edges_count):
    source, target = nodes_label[edges_raw[i][0]], nodes_label[edges_raw[i][1]]
    transitions.append((source, target))
    transitions_label[(source, target)] = "T" + str(i)

row_max = math.ceil(math.sqrt(nodes_count)) + 1

for x in range(nodes_count):
    nodes_cords[nodes_label[nodes[x]]] = (xs + int(x % row_max) * pad, ys + int(x / row_max) * pad)


# Transition rotation
# #do it for the a e  s    t     h      e       t        h         i          c
def slope(x0, x1, y0, y1):
    return (int(math.degrees(math.atan2((y1 - y0), (x1 - x0)))))


def tran_locator(x0, x1, y0, y1):
    ab = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    x = ab / (math.sqrt(3 / 2))
    alpha = math.degrees(math.atan2((y1 - y0), (x1 - x0)))
    return (int(x0 + x * math.cos(alpha + 30)), int(y0 + x * math.sin(alpha + 30)))


# Writing to file
f = open(network + "_v2.tapn", "w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")
f.write("  <net active=\"true\" id=\"" + network + "\" type=\"P/T net\">\n")

##### PART I: NODES
for i in range(nodes_count):
    x, y = nodes_cords[nodes_label[nodes[i]]]
    f.write("    <place displayName=\"true\" id=\"" + nodes_label[
        nodes[i]] + "\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"" + nodes_label[
                nodes[i]] + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str(
        x) + "\" positionY=\"" + str(y) + "\"/>\n")

#### PART II: TRANSITIONS

for i in range(edges_count):
    source, target = transitions[i]
    x0, y0 = nodes_cords[source]
    x1, y1 = nodes_cords[target]
    x2 = (x0 + x1) / 2
    y2 = (y0 + y1) / 2

    x, y = tran_locator(x2, x1, y2, y1)
    # print(x0, " ", y0)
    # print(x1, " ", y1)
    # print(x2, " ", y2)
    # print(x, " ", y)
    f.write("    <transition angle=\"" + str(slope(x0, x1, y0, y1)) + "\" displayName=\"true\" id=\"" + "T" + str(
        i) + "\" infiniteServer=\"false\" name=\"" + "T" + str(
        i) + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str(x) + "\" positionY=\"" + str(
        y) + "\" priority=\"0\" urgent=\"false\"/>\n")

##### PART III: ARCS
# Generating node-transition arcs, idem to previous
for i in range(edges_count):
    source, target = transitions[i]
    print(source + " to " + target + " through " + transitions_label[(source, target)])
    f.write("    <arc id=\"" + source + " to " + transitions_label[(source,
                                                                    target)] + "\" inscription=\"[0,inf)\" nameOffsetX=\"0.0\" nameOffsetY=\"0.0\" source=\"" + source + "\" target=\"" +
            transitions_label[(source, target)] + "\" type=\"timed\" weight=\"1\">\n")
    f.write("    </arc>\n")
    f.write("    <arc id=\"" + transitions_label[
        (source, target)] + " to " + target + "\" inscription=\"1\" nameOffsetX=\"0.0\" nameOffsetY=\"0.0\" source=\"" +
            transitions_label[(source, target)] + "\" target=\"" + target + "\" type=\"normal\" weight=\"1\">\n")
    f.write("    </arc>\n")

# File writing ending part
f.write("  </net>\n")
f.write("  <k-bound bound=\"3\"/>\n")
f.write("</pnml>")
f.close()

# Very nice success message
print("Done! " + network + " converted to " + network + "_v2.tpn!")
# No error message in case it doesn't work
# because that's not a posibility :^)
