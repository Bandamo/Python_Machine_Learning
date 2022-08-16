import numpy as np
import warnings
import time
import os
import matplotlib.pyplot as plt
import tqdm


def sigmoid(arr: np.ndarray):
    return 1 / (1 + np.exp(-arr))


def randfloat(a: float, b: float, shape: tuple):
    np.random.seed(time.time_ns()%(2**31-1))
    return (b - a) * np.random.random(shape) + a


def clear():
    input()
    for _ in range(100):
        print("\n")


class Layer:
    def __init__(self, nb_input, nb_neurone, weights=randfloat(-10, 10, (10, 10)),
                 have_predefined_weights=False):
        self.nb_input = nb_input
        self.nb_neurone = nb_neurone
        self.list_activity = np.zeros((nb_neurone, 1))
        if not have_predefined_weights:
            self.list_weight = randfloat(-10, 10, (nb_input, nb_neurone))
        else:
            self.list_weight = weights
            try:
                if not (self.list_weight.shape == (nb_input, nb_neurone)):
                    raise AttributeError
            except AttributeError:
                raise AttributeError

    def process(self, input_array):
        self.list_activity = sigmoid(np.dot(input_array, self.list_weight))
        return self.list_activity

    def mutate(self):
        # Multiply every weight by a factor generally between 0.75 and 1.25
        for x in range(len(self.list_weight)):
            for y in range(len(self.list_weight[0])):
                self.list_weight[x][y] = self.list_weight[x][y] * np.random.normal(1, 0.25)


class Brain:
    def __init__(self, nb_input, nb_output, nb_hl, nb_neurone_hl, parent_brain=None, have_parent=False):

        if have_parent:
            # Inherit from their traits
            self.layers = parent_brain.layers
            self.nb_input = parent_brain.nb_input
            self.nb_output = parent_brain.nb_output
            self.nb_hl = parent_brain.nb_hl
            self.nb_neurone_hl = parent_brain.nb_neurone_hl
        else:
            # Create new brain
            self.layers = []
            self.nb_input = nb_input
            self.nb_output = nb_output
            self.nb_hl = nb_hl
            self.nb_neurone_hl = nb_neurone_hl

            # Create layers
            # Layers format [HL_1,HL_2,...,HL_(nb_hl),output]

            if nb_hl > 0:  # If there is hidden layers create the first of them
                self.layers += [Layer(nb_input=nb_input, nb_neurone=nb_neurone_hl)]
                for _ in range(1, nb_hl):
                    self.layers += [Layer(nb_input=(self.layers[-1]).nb_neurone, nb_neurone=nb_hl)]
                # Last layer (output layer)
                self.layers += [Layer(nb_input=(self.layers[-1]).nb_neurone, nb_neurone=nb_output)]
            else:
                self.layers = [Layer(nb_input=nb_input, nb_neurone=nb_output)]

    def mutate(self):
        for layer in self.layers:
            layer.mutate()

    def think(self, input_array: np.ndarray, decision=False):
        """
        Use the different layer to make a decision based on the output
        :param input_array:
        :return:
        """
        activity_of_previous_layer = input_array
        for layer in self.layers:
            activity_of_previous_layer = layer.process(activity_of_previous_layer)
        output = activity_of_previous_layer[0]
        if len(output) != self.nb_output:
            warnings.warn("Problème de shape : expected len " + str(self.nb_output) + " got len " + str(len(output)))
        if decision:
            return max(range(len(output)), key=output.__getitem__)  # Index of the maximum
        else:
            return output


class Grid:
    def __init__(self, shape=(20, 30)):
        self.value = np.zeros(shape=shape)

    def verif_move(self, position, dir):
        """
        Return an int corresponding to the possibility of moving
           1
        2  0  3
           4
        :param position: position of the moving thing
        :param dir: direction of the movement
        :return:-1 -> There is a wall
                0  -> There is nothing
        """
        if dir == 0:
            return 0
        elif dir == 1:
            try:
                object_in_new_case = self.value[position[0]][position[1] + 1]
                return object_in_new_case
            except IndexError:
                return -1
        elif dir == 2:
            try:
                object_in_new_case = self.value[position[0] - 1][position[1]]
                if position[0] - 1 < 0:
                    return -1
                else:
                    return object_in_new_case
            except IndexError:
                return -1
        elif dir == 3:
            try:
                object_in_new_case = self.value[position[0] + 1][position[1]]
                return object_in_new_case
            except IndexError:
                return -1
        elif dir == 4:
            try:
                object_in_new_case = self.value[position[0]][position[1] - 1]
                if position[1] - 1 < 0:
                    return -1
                else:
                    return object_in_new_case
            except IndexError:
                return -1

    def add_elem(self, position, species):
        """
        Add an element in the array
        :param species: type of the element
        :param position: position of the element
        :return:
        """
        try:
            self.value[position[0]][position[1]] = species
        except IndexError:
            warnings.warn("IndexError : Veuillez ressaisir la position, rien n'a été changé")

    def move_object(self, pos1, pos2):
        """
        Move an object from pos1 to pos2, overwriting pos2
        :param pos1: Initial position
        :param pos2: Final position
        """
        nothing = 0
        element_to_move = self.value[pos1[0]][pos1[1]]
        self.add_elem(pos1, nothing)
        self.add_elem(pos2, element_to_move)

    def display(self):
        """
        Display the array
        """
        printable = np.rot90(self.value)
        print(printable.view())


class Animal():
    def __init__(self, brain=Brain(10, 5, 0, 5), energy=100, grid=Grid(), position="Default"):
        """

        :param energy: Energy of the animal
        :param brain: Neural Network of the animal
        :param position: Position of the animal in the world
        :param grid: grid where the animal can move
        """
        self.species = 1  # 1 is the type of Animal
        self.energy = energy
        self.brain = brain
        self.grid = grid
        if position == "Default":
            self.position = [np.random.randint(0, self.grid.value.shape[0]),
                             np.random.randint(0, self.grid.value.shape[1])]
        self.grid.add_elem(self.position, self.species)

    def move(self, dir):
        """
        move the animal to one of the four case around it
           1
        2  0  3
           4
        :param dir: Direction of the movement

        """
        if dir == 1 and self.grid.verif_move(self.position, dir) == 0:
            new_pos = [self.position[0], self.position[1] + 1]
            self.grid.move_object(self.position, new_pos)
            self.position = new_pos
        elif dir == 2 and self.grid.verif_move(self.position, dir) == 0:
            new_pos = [self.position[0] - 1, self.position[1]]
            self.grid.move_object(self.position, new_pos)
            self.position = new_pos
        elif dir == 3 and self.grid.verif_move(self.position, dir) == 0:
            new_pos = [self.position[0] + 1, self.position[1]]
            self.grid.move_object(self.position, new_pos)
            self.position = new_pos
        elif dir == 4 and self.grid.verif_move(self.position, dir) == 0:
            new_pos = [self.position[0], self.position[1] - 1]
            self.grid.move_object(self.position, new_pos)
            self.position = new_pos

    def take_decision(self, input_arr):
        output = self.brain.think(input_arr, decision=True)
        self.move(output)
        return output


if __name__ == '__main__':
    for k in range(10):

        os.mkdir("Images_"+str(k).zfill(3))

        shape_grid=(20,20)

        world = Grid(shape=shape_grid)
        animal=Animal(grid=world)
        bar=tqdm.tqdm(total=100)
        for i in range(100):
            bar.update()

            input_arr=np.random.random((1,10))
            animal.take_decision(input_arr)

            fig, ax = plt.subplots(figsize=(12, 12))

            tick=np.arange(0,20,1)
            ax.set_xticks(tick)
            ax.set_yticks(tick)
            ax.grid(which='major', alpha=0.5)

            ax.scatter(animal.position[0],animal.position[1])
            plt.xlim([0,20])
            plt.ylim([0,20])
            plt.savefig("Images_"+str(k).zfill(3)+"/Im_"+str(i).zfill(3)+".png")
            plt.close(fig)
        bar.close()

