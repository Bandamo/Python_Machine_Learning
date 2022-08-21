import objects
import copy


def find_c(c1: objects.Connection, list_c: list):
    index = 0
    for c2 in list_c:
        if c1.inputs == c2.inputs and c1.outputs == c2.outputs:
            return index
        index += 1
    return None


def crossover(b1: objects.Brain, b2: objects.Brain):
    b_children = copy.deepcopy(b1)

    # Crossover connections
    c1 = copy.deepcopy(b1.connections)
    c2 = copy.deepcopy(b2.connections)

    c_children = []

    curseur = 0
    while curseur < len(c1):
        index = find_c(c1[curseur], c2)
        if index != None:
            if objects.bernoulli_bool(0.5):
                c_children += [c1[curseur]]
            else:
                c_children += [c2[index]]
            c1.pop(curseur)
            c2.pop(index)
        else:
            curseur += 1
