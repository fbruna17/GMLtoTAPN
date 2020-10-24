import networkx as nx

class Node:
    def __init__(self, id, notation):
        self.id = id
        self.notation = notation
        self.transition_count = None
        self.x = None
        self.y = None
    def to_file(self):
        return ("    <place displayName=\"true\" id=\"{}\" initialMarking=\"0\" invariant=\"&lt; inf\" name=\"{}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{}\" positionY=\"{}\"/>\n"
                .format(self.notation, self.notation, self.x, self.y))

    def info(self):
        print("ID: {}, Notation: {}, Transition count: {}, X Coord: {}, Y Coord: {}"
              .format(self.id, self.notation, self.transition_count, self.x, self.y))

class Transition:
    def __init__(self, id, source, target, notation):
        self.id = id
        self.source = source
        self.target = target
        self.notation = notation
        self.angle = None
        self.x = None
        self.y = None
        self.type = None
    def to_file(self):
        return ("    <transition angle=\"{}\" displayName=\"true\" id=\"{}\" infiniteServer=\"false\" name=\"{}\" nameOffsetX=\"-5.0\" nameOffsetY=\"35.0\" positionX=\"{}\" positionY=\"{}\" priority=\"0\" urgent=\"false\"/>\n"
                .format(self.angle, self.notation, self.notation, self.x, self.y))

    def info(self):
        print("ID: {}, Source: {}, Target: {},  Notation: {},  X Coord: {}, Y Coord: {}"
              .format(self.id, self.source, self.target, self.notation, self.x, self.y))

class Arc:
    def __init__(self, source, target, transition):
        self.source = source
        self.target = target
        self.transition = transition
    def to_file(self):
        if self.source is None:
            return ("    <arc id=\"{} to {}\" inscription=\"1\" nameOffsetX=\"0.0\" nameOffsetY=\"0.0\" source=\"{}\" target=\"{}\" type=\"normal\" weight=\"1\">\n"
                    .format(self.transition.notation, self.target.notation, self.transition.notation, self.target.notation)
                    + "    </arc>\n")
        else:
            return ("    <arc id=\"{} to {}\" inscription=\"[0,inf)\" nameOffsetX=\"0.0\" nameOffsetY=\"0.0\" source=\"{}\" target=\"{}\" type=\"timed\" weight=\"1\">\n"
                    .format(self.source.notation, self.transition.notation, self.source.notation, self.transition.notation)
                    + "    </arc>\n"
                    + "    <arc id=\"{} to {}\" inscription=\"1\" nameOffsetX=\"0.0\" nameOffsetY=\"0.0\" source=\"{}\" target=\"{}\" type=\"normal\" weight=\"1\">\n"
                    .format(self.transition.notation, self.target.notation, self.transition.notation, self.target.notation)
                    + "    </arc>\n")

    def info(self):
        print("Source: {}, Target: {}, Transition: {}"
              .format(self.source.notation, self.target.notation, self.transition.notation))

network = " "
G = nx.read_gml(network + '.gml', label = 'id')
nodes_raw = list(G.nodes(data=True))
edges_raw = list(G.edges)

nodes = []
transitions = []
arcs = []


def parse_nodes():
    for i in nodes_raw:
        n = Node(i[0], "P{}".format(i[0]))
        nodes.append(n)
def info_nodes():
    for i in nodes:
        i.info()

def parse_transitions():
    for i in edges_raw:
        t = Transition(edges_raw.index(i), i[0], i[1], "T{}_{}".format(i[0], i[1]))
        transitions.append(t)
def info_transitions():
    for i in transitions:
        i.info()

def make_arcs():
    for i in transitions:
        a = Arc(nodes[i.source], nodes[i.target], i)
        arcs.append(a)
def info_arcs():
    for i in arcs:
        i.info()

        
parse_nodes()
info_nodes()
parse_transitions()
info_transitions()
make_arcs()
info_arcs()


for i in nodes:
    print(i.to_file())
for i in transitions:
    print(i.to_file())
for i in arcs:
    print(i.to_file())
