import os
from PIL import Image
import glob
import matplotlib.pyplot as plt
import numpy as np


def create_image(folder: str, filename: str, points: list, size: int):
    fig, ax = plt.subplots()
    tick = np.arange(0, size)

    ax.set_xticks(tick)
    ax.set_yticks(tick)

    plt.xlim(0, size)
    plt.ylim(0, size)

    for point in points:
        ax.scatter(point[0], point[1])

    plt.savefig(folder + "/" + filename)
    plt.close(fig)


def create_gif():
    try:
        os.mkdir('Gif')
    except:
        print("Dossier existant")
    # Create the frames
    list_file = os.listdir()
    list_image_folder = []
    for e in list_file:
        if 'Images' in e:
            list_image_folder += [e]
    for folder in list_image_folder:
        frames = []
        imgs = glob.glob(folder + "/*.png")
        imgs.sort()
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)

        # Save into a GIF file that loops forever
        frames[0].save("Gif/" + folder + '.gif', format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=100, loop=0)


if __name__ == '__main__':
    create_gif()
