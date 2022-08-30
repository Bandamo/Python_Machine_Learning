import time
import random
import numpy as np
import copy


def randpm1():
    return 2 * (np.random.random() - 0.5)


def bernoulli_bool(p):
    return np.random.random() <= p


class Node:
    def __init__(self, id_node: int, layer: int):
        self.id_node = id_node
        # Different varieties : -1 input, 1-... layer of the hidden, 0 output
        self.layer = layer

        self.value = 0

        self.bias = randpm1()

        self.inputs = 0

        self.activated = False

    def reset(self):
        self.value = 0
        self.inputs = 0
        self.activated = False

    def activate(self):
        self.value = np.tanh(self.inputs + self.bias)


class Connection:
    def __init__(self, inputs, outputs, weight: float, enabling: bool):
        self.inputs = inputs
        self.outputs = outputs
        self.weight = weight
        self.enabling = enabling
        self.innovation = inputs * 1000 + outputs


class Brain:
    def __init__(self, nb_input, nb_output):
        self.nb_node = 0
        self.innovation = 0

        # Creating input and output node and connections
        self.inputs = [Node(id_node, -1) for id_node in range(nb_input)]
        self.nb_node = nb_input
        self.outputs = [Node(id_node, 0) for id_node in range(self.nb_node, self.nb_node + nb_output)]
        self.nb_node += nb_output

        self.hl_node = np.array([[]], dtype=Node)

        self.connections = []

        # Connections:
        for k in range(len(self.outputs)):
            list_inputs = list(range(nb_input))
            random.shuffle(list_inputs)
            connected = False
            for i in list_inputs[:-1]:
                if bernoulli_bool(1 / nb_output):
                    self.connections += [
                        Connection(self.inputs[i].id_node, self.outputs[k].id_node, randpm1(), True)]
                    self.innovation += 1
                    connected = True
            if not connected:
                self.connections += [
                    Connection(self.inputs[list_inputs[-1]].id_node, self.outputs[k].id_node, randpm1(), True)]
                self.innovation += 1

    def activate_input(self, inputs: list):
        for k in range(len(self.inputs)):
            self.inputs[k].value = inputs[k]
            self.inputs[k].activated = True

    def find_node(self, id_search):
        for n in self.inputs:
            if n.id_node == id_search:
                return n
        for l in self.hl_node:
            for n in l:
                if n.id_node == id_search:
                    return n
        for n in self.outputs:
            if n.id_node == id_search:
                return n
        raise Exception

    def think(self):
        connection_left = copy.deepcopy(self.connections)
        print(type(self.hl_node))
        node_list = self.inputs + list(self.hl_node.flatten()) + self.outputs
        for conn in connection_left:
            if not conn.enabling:
                connection_left.remove(conn)
        while len(connection_left) > 0:
            for conn in connection_left:
                if self.find_node(conn.inputs).activated:
                    self.find_node(conn.outputs).inputs += self.find_node(conn.inputs).value * conn.weight
                    connection_left.remove(conn)
            for n in node_list:
                if not (n.id_node in [connection_left[k].outputs for k in range(len(connection_left))]):
                    n.activate()
                    n.activated = True

    def reset(self):
        node_list = self.inputs + self.hl_node.flatten() + self.outputs
        for n in node_list:
            n.reset()

    def valid_connection(self, init, end):
        if init in [self.inputs[k].id_node for k in range(len(self.inputs))] and end in [self.inputs[k].id_node for k in
                                                                                         range(len(self.inputs))]:
            return False
        elif init in [self.inputs[k].id_node for k in range(len(self.inputs))]:
            return True
        elif init in [self.outputs[k].id_node for k in range(len(self.outputs))]:
            return False
        else:
            i = self.find_node(init)
            e = self.find_node(end)

            if i.layer < e.layer:
                return True
            else:
                return False

    def create_connection(self):
        init_node = np.random.randint(0, self.nb_node)
        while init_node in [self.outputs[k].id_node for k in range(len(self.outputs))]:
            init_node = np.random.randint(0, self.nb_node)
        end_node = np.random.randint(0, self.nb_node)
        print("Creating random connection")
        while not self.valid_connection(init_node, end_node):
            end_node = np.random.randint(0, self.nb_node)
        self.connections += [Connection(init_node, end_node, randpm1(), True)]

    def increment_hidden_layer(self, rank):
        np.append(self.hl_node, [self.hl_node[-1]], axis=0)
        for k in range(len(self.hl_node) - 2, rank, -1):
            self.hl_node[k] = self.hl_node[k - 1]

    def create_node(self):
        connection_parent = self.connections[np.random.randint(0, len(self.connections))]
        if connection_parent.inputs in [inputs.id_node for inputs in self.inputs]:
            if len(self.hl_node[0]) == 0:
                self.hl_node = np.array([[Node(self.nb_node, 0)]])
                print(self.hl_node[0])
            else:
                np.append(self.hl_node[0], [Node(self.nb_node, self.nb_node)], axis=0)
            print(self.hl_node)
            target_output = connection_parent.outputs
            connection_parent.outputs = self.nb_node
            self.connections += [Connection(self.nb_node, target_output, randpm1(), True)]
            self.nb_node += 1

    def show_network(self):
        pass


if __name__ == '__main__':
    b = Brain(5, 10)
    b.create_node()
    b.create_node()
    b.activate_input([1,2,3,4,5])
    b.think()
    print([out.value for out in b.outputs])
