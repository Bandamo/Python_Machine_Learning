import os
from PIL import Image
import glob

def create_gif():
    try:
        os.mkdir('Gif')
    except:
        print("Dossier existant")
    # Create the frames
    list_file=os.listdir()
    list_image_folder=[]
    for e in list_file:
        if 'Images' in e:
            list_image_folder+=[e]
    for folder in list_image_folder:
        frames = []
        imgs = glob.glob(folder+"/*.png")
        imgs.sort()
        for i in imgs:
            new_frame = Image.open(i)
            frames.append(new_frame)

        # Save into a GIF file that loops forever
        frames[0].save("Gif/"+folder+'.gif', format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=300, loop=0)
if __name__=='__main__':
    create_gif()