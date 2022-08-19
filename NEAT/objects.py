import time

import numpy as np
import copy

def randpm1():
    return 2 * (np.random.random() - 0.5)


class Node:
    def __init__(self, id_node: int, variety: int):
        self.id_node = id_node
        # Different varieties : 1 input, 2 hidden, 3 output
        self.variety = variety

        self.value = 0

        self.bias=randpm1()

        self.inputs=0

        self.activated=False


    def reset(self):
        self.value=0
        self.inputs=0
        self.activated=False

    def activate(self):
        self.value=np.tanh(self.value)


class Connection:
    def __init__(self, inputs, outputs, weight: float, innovation: int, enabling: bool):
        self.inputs = inputs
        self.outputs = outputs
        self.weight = weight
        self.enabling = enabling
        self.innovation = innovation


class Brain:
    def __init__(self, nb_input, nb_output):
        self.nb_node = 0
        self.innovation = 0

        # Creating input and output node and connections
        self.inputs = [Node(id_node, 1) for id_node in range(nb_input)]
        self.nb_node = nb_input
        self.outputs = [Node(id_node, 3) for id_node in range(self.nb_node, self.nb_node + nb_output)]

        self.hl_node = []

        self.connections = []

        # Connections:
        for k in range(len(self.inputs)):
            for i in range(len(self.outputs)):
                self.connections += [Connection(self.inputs[k].id_node, self.outputs[i].id_node, randpm1(), self.innovation, True)]
                self.innovation += 1
    def activate_input(self,inputs : list):
        for k in range(len(self.inputs)):
            self.inputs[k].value=inputs[k]
            self.inputs[k].activated=True
    def find_node(self,id_search):
        for n in self.inputs:
            if n.id_node==id_search:
                return n
        for n in self.hl_node:
            if n.id_node==id_search:
                return n
        for n in self.outputs:
            if n.id_node==id_search:
                return n
        raise Exception

    def think(self):
        connection_left=copy.deepcopy(self.connections)
        node_list=self.inputs+self.hl_node+self.outputs
        for conn in connection_left:
            if conn.enabling==False:
                connection_left.remove(conn)
        while len(connection_left)>0:
            for conn in connection_left:
                if self.find_node(conn.inputs).activated:
                    self.find_node(conn.outputs).value+=self.find_node(conn.inputs).value * conn.weight
                    connection_left.remove(conn)
            for n in node_list:
                if not(n.id_node in [connection_left[k].outputs for k in range(len(connection_left))]):
                    n.activate()
                    n.activated=True
    def reset(self):
        node_list=self.inputs+self.hl_node+self.outputs
        for n in node_list:
            n.reset()







if __name__ == '__main__':
    t=time.time()
    for _ in range(5):
        b = Brain(100, 5)
        b.activate_input(np.random.randint(-10,10,(100,1)))
        b.think()
        print([b.outputs[k].value for k in range(len(b.outputs))])
    print(time.time()-t)