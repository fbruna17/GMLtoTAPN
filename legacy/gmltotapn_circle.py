import networkx as nx #Library used to work with GML files
import math
import random
from collections import defaultdict

### TODO:
#   - ?different spacing between transitions based on how many outgoings a node has
#   - ?rotate somehow the transitions so that the lines don't seem to overlap
##  - ~automatically change settings based on network size
###########

#GML Network to be converted
#### HAS TO BE IN SAME DIRECTORY AS PY FILE FOR NOW
## INPUT ITS NAME BELLOW
network = 'Arpanet196912'
#network = 'Aarnet'
#network = 'Aconet'
#network = 'GtsCe'
#network = 'UniC'

#Initialising the GML reader
G = nx.read_gml(network + '.gml', label = 'id')
nodes_count = len(G.nodes)
edges_count = len(G.edges)
nodes_raw = list(G.nodes(data = True))
edges_raw = list(G.edges)


### SETTINGS ###
xs = 600 #x offset
ys = 600 #y offset
r = 500  #circle ray, has to be smaller than offset
tspace = 60 #spacing between transitions


################

#Needed variables
nodes = []
nodes_label = {}
nodes_cords = {}
transitions = []
transitions_label = {}
ntc = {}

#Extracting information from GML
for i in range(nodes_count):
    nodes.append(nodes_raw[i][0])
    nodes_label[nodes_raw[i][0]] = "P" + str(i)
    ntc["P" + str(i)] = 0
for i in range(edges_count):
    source, target = nodes_label[edges_raw[i][0]], nodes_label[edges_raw[i][1]]
    transitions.append((source, target))
    transitions_label[(source, target)] = "T" + str(i)

waypointcount = int(input("Input a number of desired waypoints between 1 and " + str(nodes_count) + " :  "))
waypoints = random.sample(list(nodes_label), waypointcount)

#Generates a set of (x,y) coordinates in the "nth slice"
#of the circle at a certain radius
def rgen(n, radius):
    alpha = 2 * math.pi * n / nodes_count
    return (int(math.cos(alpha) * radius) + xs, int(math.sin(alpha) * radius) + ys)

#For each node, its circle coordinates are generated here
#by using the method above
for x in range(nodes_count):
    nodes_cords[nodes_label[nodes[x]]] = rgen(x, r)

#Calculates the angle between 2 points
def slope(x0, x1, y0, y1):
    return (int(math.degrees(math.atan2((y1-y0),(x1-x0)))))

#Generates the coordinate of a transition
#Each node is tracked to see how many outputs it has
#With each output, the radius of the circle is decreased
def tran_locator(x, y, t):
    ntc[t] +=1
    a, b = rgen(int(t[1:]), r-ntc[t]*tspace)
    return (a, b)
    
#Writing to file
f = open(network + "_v4.tapn", "w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")
for i in range(edges_count):
    f.write("    <shared-transition name=\"T" + str(i) + "\" urgent=\"false\"/>\n")

visited = defaultdict(list)
for i in waypoints:
    source0, wp = transitions[i]
    for j in transitions:
        source, target = j
        if target == wp:
            visited[wp].append(j)
        




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
    f.write("    <transition angle=\"" + str(slope(x0, xs, y0, ys)) + "\" displayName=\"true\" id=\"" + "T" + str(i) + "\" infiniteServer=\"false\" name=\"" + "T" + str(i) + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str(x) + "\" positionY=\"" + str(y) + "\" priority=\"0\" urgent=\"false\"/>\n")

##### PART III: ARCS
for i in range(edges_count):
    source, target = transitions[i]
    print(source + " to " + target + " through " + transitions_label[(source, target)])
    f.write("    <arc id=\"" + source + " to " + transitions_label[(source, target)] + "\" inscription=\"[0,inf)\" nameOffsetX=\"0.0\" nameOffsetY=\"0.0\" source=\"" + source + "\" target=\"" + transitions_label[(source, target)] + "\" type=\"timed\" weight=\"1\">\n")
    f.write("    </arc>\n")
    f.write("    <arc id=\"" + transitions_label[(source, target)] + " to " + target + "\" inscription=\"1\" nameOffsetX=\"0.0\" nameOffsetY=\"0.0\" source=\"" + transitions_label[(source, target)] + "\" target=\"" + target + "\" type=\"normal\" weight=\"1\">\n")
    f.write("    </arc>\n")

f.write("  </net>\n")


#### PART IV COMPONENTS
print("\n\nWaypoints:")
print(waypoints)
for i in waypoints:
    wp_id = nodes_label[nodes[i]] + "_visited" #Waypoint ID
    print(wp_id, ":")
    f.write("  <net active=\"true\" id=\"" + wp_id + "\" type=\"P/T net\">\n")
    f.write("    <place displayName=\"true\" id=\"" + wp_id + "\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"" + wp_id + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + "100" + "\" positionY=\"" + "100" + "\"/>\n")
    c_wp = visited[nodes_label[nodes[i]]] #Current waypoint
    y_diff = 50 #Pixel difference for y coord
    cnt = 0     #Counter for positioning
    for j in c_wp:
        source, target = j
        f.write("    <transition angle=\"0\" displayName=\"true\" id=\"" + str(transitions_label[(source, target)]) + "\" infiniteServer=\"false\" name=\"" + str(transitions_label[(source, target)]) + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + "200" + "\" positionY=\"" + str( 100 + y_diff*cnt ) + "\" priority=\"0\" urgent=\"false\"/>\n")
        cnt += 1
    cnt = 0
    for j in c_wp:
        source, target = j
        f.write("    <arc id=\"" + str(transitions_label[(source, target)]) + " to " + wp_id + "\" inscription=\"1\" nameOffsetX=\"0.0\" nameOffsetY=\"0.0\" source=\"" + str(transitions_label[(source, target)]) + "\" target=\"" + wp_id + "\" type=\"normal\" weight=\"1\">\n")
        f.write("    </arc>\n")
        cnt += 1
        
        print(str(transitions_label[(source, target)]) + " to " + wp_id)
        
    f.write("  </net>\n")

    
    
f.write("  <k-bound bound=\"3\"/>\n")
f.write("</pnml>")
f.close()

#Very nice success message
print("Done! " + network + " converted to " + network + "_v4.tpn!")
#No error message in case it doesn't work
#because that's not a posibility :^)
