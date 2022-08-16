import numpy as np
import warnings
import time
import os
import utils


def sigmoid(arr: np.ndarray):
    """
    Simple function going from R to [-1;1]
    :param arr: input in R
    :return: output in [-1;1]
    """
    return 2 / (1 + np.exp(-arr))


def randfloat(a: float, b: float, shape: tuple):
    np.random.seed(time.time_ns() % (2 ** 31 - 1))
    return (b - a) * np.random.random(shape) + a


def bernoulli_proba(p=0.5):
    result = np.random.random()
    if result < p:
        return True
    else:
        return False


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

    def mutate(self, mutating_rate: float):
        # Multiply every weight by a factor generally between 0.75 and 1.25
        for x in range(len(self.list_weight)):
            for y in range(len(self.list_weight[0])):
                if bernoulli_proba(mutating_rate): self.list_weight[x][y] = randfloat(-10, 10, (1, 1))[0][0]


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

    def mutate(self, mutating_rate: float):
        for layer in self.layers:
            layer.mutate(mutating_rate=mutating_rate)

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
    def __init__(self, shape=(20, 20)):
        real_shape = (shape[0] + 2, shape[1] + 2)
        self.value = np.zeros(shape=real_shape)
        self.apple_pos = []

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

    def generate_apple(self, proportion):
        """
        Generate a batch of apple in the grid
        :param proportion:
        :return:
        """
        for x in range(len(self.value)):
            for y in range(len(self.value[0])):
                if bernoulli_proba(proportion):
                    self.apple_pos += [[x, y]]
                    self.add_elem((x, y), 2)

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
    def __init__(self, brain=Brain(10, 5, 0, 5), grid=Grid(), position="Default"):
        """

        :param energy: Energy of the animal
        :param brain: Neural Network of the animal
        :param position: Position of the animal in the world
        :param grid: grid where the animal can move
        """
        self.species = 1  # 1 is the type of Animal
        self.score = 0
        self.brain = brain
        self.grid = grid
        if position == "Default":
            self.position = [self.grid.value.shape[0] // 2, self.grid.value.shape[1] // 2]
        elif position == "Random":
            self.position = [np.random.randint(0, self.grid.value.shape[0]),
                             np.random.randint(0, self.grid.value.shape[1])]
        else:
            self.position = position
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

    def get_input(self):
        """
        get input for the brain, take all case in a 3 case radius:
         0  1  2  3  4  5  6
         7  8  9 10 11 12 13
        14 15 16 17 18 19 20
        21 22 23 XX 24 25 26
        27 28 29 30 31 32 33
        34 35 36 37 38 39 40
        41 42 43 44 45 46 47
        :return:
        """
        input_arr = []
        for k in range(-3, 4):
            for i in range(-3, 4):
                try:
                    if (k, i) != (0, 0) and k >= 0 and i >= 0:
                        input_arr += [self.grid.value[k][i]]
                    elif k < 0 or i < 0:
                        input_arr += [-1]
                except IndexError:
                    input_arr += [-1]
        return input_arr

    def take_decision(self, input_arr):
        output = self.brain.think(input_arr, decision=True)
        self.move(output)
        return output


if __name__ == '__main__':
    # noinspection PyTypeChecker
    anim = Animal(position=(0,0))
    anim.grid.display()
    print(anim.get_input())

