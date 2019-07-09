import pyglet
from pyglet import *
from pyglet.gl import *
from shaders import ShapeShader

# graph class
class CouplingPath:
    def __init__(self, color=[0.5,0.5,0.5,1.0] ):
        self.nodes = {}
        self.edges = []
        self.color = color
        self.datanodes = {}

    def shift_paths(self, move_vector):
        for pos in self.nodes:
            self.nodes[pos].coor += move_vector
        for edge in self.edges:
            edge.reset_shape()

    def add_node(self, coor, data=None): #create a new node and automatically connect nodes with matching coors
        if tuple(coor) in self.nodes:
            return self.nodes[tuple(coor)]
        newnode = CouplingPathNode(coor, data)
        self.nodes[tuple(coor)] = newnode
        if data is not None:
            self.datanodes[data] = newnode
        return newnode

    def add_edge(self, node1, node2): #the node1 and node2 can be node object or coordinate
        if type(node1) != CouplingPathNode:
            if tuple(node1) in self.nodes:
                node1 = self.nodes[tuple(node1)]
            else:
                node1 = self.add_node(tuple(node1))
        if type(node2) != CouplingPathNode:
            if tuple(node2) in self.nodes:
                node2 = self.nodes[tuple(node2)]
            else:
                node2 = self.add_node(tuple(node2))
        newedge = CouplingPathEdge(node1, node2)
        self.edges.append(newedge)
        return newedge

    def neighbors(self, node):
        neighbor = []
        for edge in self.edges:
            if edge.node1 == node:
                neighbor.append([edge.node2, edge])
            elif edge.node2 == node:
                neighbor.append([edge.node1, edge])
        return neighbor

    def __distance(self, coor1, coor2):
        return sum((coor1-coor2)**2)**0.5

    def search_path(self, data1, data2):
        startnode = self.datanodes[data1]
        endnode = self.datanodes[data2]
        queue = [[startnode, []]]
        possiblepaths = []
        visited = []
        while len(queue)>0:
            expand_node = queue.pop()
            if expand_node[0] == endnode:
                possiblepaths.append(expand_node[1])
            else:
                visited.append(expand_node[0])
                next_nodes = [node for node in self.neighbors(expand_node[0]) if node[0] not in visited]
                queue += [[node[0], expand_node[1]+[node[1]]] for node in next_nodes]
        
        try:
            return min(possiblepaths, key=lambda x: len(x))
        except: # no path found
            return []

    def draw(self, data1, data2, debug=False, direct_draw=True):
        ShapeShader.use_color(self.color)
        
        path = self.search_path(data1, data2)
        
        for edge in path:
            if direct_draw:
                edge.draw()
            else:
                if edge not in self.to_be_drawn:
                    self.to_be_drawn.append(edge)

    def draw_all_paths(self, pair_list):
        self.to_be_drawn = []
        for pair in pair_list:
            self.draw(pair[0], pair[1], direct_draw=False)
        for edge in self.to_be_drawn:
            edge.draw()

class CouplingPathNode:
    def __init__(self, coor, data=None):
        self.data = data
        self.coor = coor


class CouplingPathEdge:
    PATH_WIDTH = 4.0
    def __init__(self, node1, node2):
        self.node1 = node1
        coor1 = node1.coor
        self.node2 = node2
        coor2 = node2.coor
        if coor1[0] < coor2[0] or coor1[2] < coor2[2]:
            coor1, coor2 = coor2, coor1
        
        if coor1[2] != coor2[2]:
            self.set_drawn_path(coor1,coor2, True)
        else:
            self.set_drawn_path(coor1,coor2, False)

    def reset_shape(self):
        coor1 = self.node1.coor
        coor2 = self.node2.coor
        if coor1[0] < coor2[0] or coor1[2] < coor2[2]:
            coor1, coor2 = coor2, coor1
        
        if coor1[2] != coor2[2]:
            self.set_drawn_path(coor1,coor2, True)
        else:
            self.set_drawn_path(coor1,coor2, False)

    def set_drawn_path(self, coor1, coor2, vertical=True):
        self.coor1 = coor1
        self.coor2 = coor2
        width = CouplingPathEdge.PATH_WIDTH
        if vertical:
            self.drawn_path = graphics.vertex_list(4, ('v3f',(
                coor1[0], coor1[1], coor1[2],
                coor1[0]+width, coor1[1], coor1[2],
                coor2[0]+width, coor2[1], coor2[2]-width,
                coor2[0], coor2[1], coor2[2]-width
            )))
        else:
            self.drawn_path = graphics.vertex_list(4, ('v3f',(
                coor1[0]+width, coor1[1], coor1[2],
                coor1[0]+width, coor1[1], coor1[2]-width,
                coor2[0], coor2[1], coor2[2]-width,
                coor2[0], coor2[1], coor2[2]
            )))
        
    def draw(self): #draw path from node with data1 to node with data2
        self.drawn_path.draw(GL_QUADS)