import networkx as nx #Library used to work with GML files
import math

#GML Network name to be converted
#Has to be in same directory as .py file for now
#network = 'Arpanet196912'
network = 'Aarnet'
#network = 'Aconet'

#Initialising the GML reader
G = nx.read_gml(network + '.gml')
nodes = list(G.nodes(data=True))
edges = list(G.edges)

#TAPAAL Window Canva size
canvas_width = 2000
canvas_height = 1000

#Needed variables
labels = []
label_link = {}
lats = []
longs = []
transitions = []
transition_link = {}
#Sepparating Id, Lat and Long
for i in range (len(G.nodes)):
    labels.append(nodes[i][0]) #Label
    lats.append(nodes[i][1]['Latitude'])
    longs.append(nodes[i][1]['Longitude'])

#Formulas used to convert gps coordinates to x,y based on
#the size of your canvas
def long_to_x(long):
    return ((int)((canvas_width/360.0) * (180 + long) *10 - 2200))
def lat_to_y(lat):
    return ((int)((canvas_height/180.0) * (90 - lat) *10 - 2200))

#Small tweak to calculate the transition rotation
# #do it for the a e  s    t     h      e       t        h         i          c
def slope(x0, x1, y0, y1):
    return (int(math.degrees(math.atan2((y1-y0),(x1-x0)))))
    


#Writing to file
f = open(network + ".tapn", "w")
f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")
f.write("  <net active=\"true\" id=\"" + network + "\" type=\"P/T net\">\n")

##### PART I: NODES
#  Writing each node to file. Highly unoptimized/dirty/all that,
#will be fixed and made more pretty.
#  To have the names instead of P0 P1 etc..
#replace "T" + str(i) in id and name with:
#labels[i]
for i in range (len(G.nodes)): 
    f.write("    <place displayName=\"true\" id=\"" + "P" + str(i) + "\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"" + "P" + str(i) + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str(long_to_x(longs[i])) + "\" positionY=\"" + str(lat_to_y(lats[i])) + "\"/>\n")
    label_link[labels[i]] = "P" + str(i)


##### PART II: TRANSITIONS
#Generating transitions from edges, same remarks as above
for i in range(len(G.edges(data=True))):
    #Calculating the middle distance
    x0 = long_to_x(G.nodes(data=True)[edges[i][0]]['Longitude'])
    x1 = long_to_x(G.nodes(data=True)[edges[i][1]]['Longitude'])
    y0 = lat_to_y(G.nodes(data=True)[edges[i][0]]['Latitude'])
    y1 = lat_to_y(G.nodes(data=True)[edges[i][1]]['Latitude'])
    x = (x0 + x1) / 2
    y = (y0 + y1) / 2

    p0 = edges[i][0]
    p1 = edges[i][1]
    #To have the names instead of T0 T1 etc..
    #replace "T" + str(i) in id and name with:
    #str(edges[i][0] + "_" + edges[i][1])
    f.write("    <transition angle=\"" + str(slope(x0, x1, y0, y1)) + "\" displayName=\"true\" id=\"" + "T" + str(i) + "\" infiniteServer=\"false\" name=\"" + "T" + str(i) + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str(x) + "\" positionY=\"" + str(y) + "\" priority=\"0\" urgent=\"false\"/>\n")
    transition_link[(p0, p1)] = "T" + str(i)

##### PART III: ARCS
#Generating node-transition arcs, idem to previous
for i in G.edges(data=True):
    source = i[0]
    target = i[1]
    print(str(label_link[source]) + " to " + str(label_link[target]) + " through " + str(transition_link[(source, target)]))
    f.write("    <arc id=\"" + label_link[source] + " to " + transition_link[(source, target)] + "\" inscription=\"[0,inf)\" nameOffsetX=\"0.0\" nameOffsetY=\"0.0\" source=\"" + label_link[source] + "\" target=\"" + transition_link[(source, target)] + "\" type=\"timed\" weight=\"1\">\n")
    f.write("    </arc>\n")
    f.write("    <arc id=\"" + transition_link[(source, target)] + " to " + label_link[target] + "\" inscription=\"1\" nameOffsetX=\"0.0\" nameOffsetY=\"0.0\" source=\"" + transition_link[(source, target)] + "\" target=\"" + label_link[target] + "\" type=\"normal\" weight=\"1\">\n")
    f.write("    </arc>\n")

#File writing ending part
f.write("  </net>\n")
f.write("  <k-bound bound=\"3\"/>\n")
f.write("</pnml>")
f.close()

#Very nice success message
print("Done! " + network + " converted to .tpn!")
#No error message in case it doesn't work
#because that's not a posibility :^)
