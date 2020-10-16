#Library used to work with GML files
import networkx as nx

#GML Network name to be converted
#Has to be in same directory as .py file for now
network = 'Arpanet196912'

#Initialising the GML reader
G = nx.read_gml(network + '.gml')
nodes = list(G.nodes(data=True))

#TAPAAL Window Canva size
canvas_width = 3000
canvas_height = 1000

#Needed arrays
labels = []
lats = []
longs = []

#Sepparating Id, Lat and Long
i = 0
for i in range (len(G.nodes)):
    labels.append(nodes[i][0]) #Label
    lats.append(nodes[i][1]['Latitude'])
    longs.append(nodes[i][1]['Longitude'])


#Writing to file
f = open(network + ".tapn", "w")

f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")
f.write("  <net active=\"true\" id=\"" + network + "\" type=\"P/T net\">\n")

for i in range (len(G.nodes)): 
    #  Writing each node to file. Highly unoptimized/dirty/all that,
    #will be fixed and made more pretty.
    f.write("    <place displayName=\"true\" id=\"" + labels[i] + "\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"" + labels[i] + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str((int)((canvas_width/360.0) * (180 + longs[i]) *5 - 2000)) + "\" positionY=\"" + str((int)((canvas_height/180.0) * (90 - lats[i]) *5-1200)) + "\"/>\n")

f.write("  </net>\n")
f.write("  <k-bound bound=\"3\"/>\n")
f.write("</pnml>")
f.close()
