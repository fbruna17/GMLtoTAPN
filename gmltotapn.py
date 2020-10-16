#Library used to work with GML files
import networkx as nx

#GML Network name to be converted
#Has to be in same directory as .py file for now
network = 'Arpanet196912'

#Initialising the GML reader
G = nx.read_gml(network + '.gml')
nodes = list(G.nodes(data=True))
edges = list(G.edges)

#TAPAAL Window Canva size
canvas_width = 3000
canvas_height = 1000

#Needed arrays
labels = []
lats = []
longs = []
transitions = []
conv_lats = []
conv_longs = []

#Sepparating Id, Lat and Long
for i in range (len(G.nodes)):
    labels.append(nodes[i][0]) #Label
    lats.append(nodes[i][1]['Latitude'])
    longs.append(nodes[i][1]['Longitude'])

#Formulas used to convert gps coordinates to x,y based on
#the size of your canvas
def long_to_x(long):
    return ((int)((canvas_width/360.0) * (180 + long) *5 - 2000))
def lat_to_y(lat):
    return ((int)((canvas_height/180.0) * (90 - lat) *5 - 1200))
    


#Writing to file
f = open(network + ".tapn", "w")

f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")
f.write("  <net active=\"true\" id=\"" + network + "\" type=\"P/T net\">\n")

for i in range (len(G.nodes)): 
    #  Writing each node to file. Highly unoptimized/dirty/all that,
    #will be fixed and made more pretty.
    f.write("    <place displayName=\"true\" id=\"" + labels[i] + "\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"" + labels[i] + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str(long_to_x(longs[i])) + "\" positionY=\"" + str(lat_to_y(lats[i])) + "\"/>\n")

#Generating transitions from edges, same remarks as above
for i in range(len(G.edges(data=True))):
    #Calculating the middle distance
    x0 = long_to_x(G.nodes(data=True)[edges[i][0]]['Longitude'])
    x1 = long_to_x(G.nodes(data=True)[edges[i][1]]['Longitude'])
    y0 = lat_to_y(G.nodes(data=True)[edges[i][0]]['Latitude'])
    y1 = lat_to_y(G.nodes(data=True)[edges[i][1]]['Latitude'])
    x = (x0 + x1) / 2
    y = (y0 + y1) / 2
    f.write("    <transition angle=\"0\" displayName=\"true\" id=\"" + str(edges[i][0] + "_" + edges[i][1]) + "\" infiniteServer=\"false\" name=\"" + edges[i][0] + "_" + edges[i][1] + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str(x) + "\" positionY=\"" + str(y) + "\" priority=\"0\" urgent=\"false\"/>\n")
    


f.write("  </net>\n")
f.write("  <k-bound bound=\"3\"/>\n")
f.write("</pnml>")
f.close()

print("Done! " + network + " converted to .tpn!")
