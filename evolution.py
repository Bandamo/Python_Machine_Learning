import time
import numpy as np
import os
import shutil
import natural_selection_neurone as neuro
import pickle


def setup_new_gen(gen):
    os.mkdir("Gen" + str(gen).zfill(3))
    os.chdir("Gen" + str(gen).zfill(3))
    os.mkdir("Brains")
    os.mkdir("Animals")


def save_brains(liste_brains: list):
    for k in range(len(liste_brains)):
        f = open("Brains/Brain_" + str(k).zfill(3) + ".pkl", "wb")
        pickle.dump(liste_brains[k], f)
        f.close()


def save_animals(liste_animals: list):
    for k in range(len(liste_animals)):
        f = open("Animals/Animal_" + str(k).zfill(3) + ".pkl", "wb")
        pickle.dump(liste_animals[k], f)
        f.close()


if __name__ == '__main__':
    if os.path.isdir("Save"):
        rep = input("Supprimer le dossier de sauvegarde ? [o]/n\t")
        if rep != "n":
            shutil.rmtree("Save")
    os.mkdir("Save")
    os.chdir("Save")
    print("Démarrage")
    n_generation = 1

    liste_brain = [neuro.Brain(48, 5, 1, 50) for _ in range(100)]  # Initial list of brain

    while n_generation <= 1:
        print("Génération numéro : " + str(n_generation))
        setup_new_gen(n_generation)
        save_brains(liste_brain)
        liste_animal = [neuro.Animal(brain=liste_brain[k]) for k in range(len(liste_brain))]
        save_animals(liste_animal)

        liste_score=[]
        for k in range(len(liste_animal)):
            animal = liste_animal[k]
            animal.grid.generate_apple(0.25)
            for _ in range(100):
                input_arr = animal.get_input()
                animal.take_decision(input_arr=input_arr)
            liste_score+=[(k,animal.score)]
            np.save("fitness.npy",liste_score)

        os.chdir("..")
        n_generation += 1  # Nouvelle génération
