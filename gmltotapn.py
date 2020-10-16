import pandas
import networkx as nx

network = 'Arpanet196912'

G = nx.read_gml(network + '.gml')
nodes = list(G.nodes(data=True))

canvas_minx = 80
canvas_miny = 80
canvas_maxx = 1400
canvas_maxy = 700
canvas_width = 3000
canvas_height = 1000

labels = []
lats = []
longs = []

i = 0
for i in range (len(G.nodes)):
    labels.append(nodes[i][0]) #Label
    lats.append(nodes[i][1]['Latitude'])
    longs.append(nodes[i][1]['Longitude'])


print(labels)
print(lats)
print(longs)
minlat = min(lats)
minlong = min(longs)
maxlat = max(lats)
maxlong = max(longs)


f = open(network + ".tapn", "w")

f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n")
f.write("<pnml xmlns=\"http://www.informatik.hu-berlin.de/top/pnml/ptNetb\">\n")
f.write("  <net active=\"true\" id=\"" + network + "\" type=\"P/T net\">\n")

for i in range (len(G.nodes)):
    f.write("    <place displayName=\"true\" id=\"" + labels[i] + "\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"" + labels[i] + "\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"" + str((int)((canvas_width/360.0) * (180 + longs[i]) *5 - 2000)) + "\" positionY=\"" + str((int)((canvas_height/180.0) * (90 - lats[i]) *5-1200)) + "\"/>\n")

f.write("  </net>\n")
f.write("  <k-bound bound=\"3\"/>\n")
f.write("</pnml>")
f.close()
#list(G.nodes(data=True))[1][2]['Longitude']
#list(G.nodes(data=True))[1][2]['Latitude']
