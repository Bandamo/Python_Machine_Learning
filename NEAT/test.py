import tkinter as tk
import objects
import numpy as np

b = objects.Brain(10, 5)

root = tk.Tk()
root.title("Testing title")
root.geometry("1000x1000")

my_canvas = tk.Canvas(root, width=700, height=500, bg="white")
my_canvas.pack(pady=20)

nb_input = len(b.inputs)
posy_input = np.array([[np.linspace(50, 450, nb_input)[k], b.inputs[k].id_node] for k in range(nb_input)])

for k in range(len(posy_input)):
    my_canvas.create_oval(40, posy_input[k][0] + 10, 60, posy_input[k][0] - 10, fill="red")

nb_output = len(b.outputs)
posy_output = np.array([[np.linspace(50, 450, nb_output)[k], b.outputs[k].id_node] for k in range(nb_output)])

for k in range(len(posy_output)):
    my_canvas.create_oval(640, posy_output[k][0] + 10, 660, posy_output[k][0] - 10, fill="green")

for c in b.connections:
    i = np.where(posy_input[:, 1] == c.inputs)[0][0]
    k = np.where(posy_output[:, 1] == c.outputs)[0][0]
    my_canvas.create_line(50,posy_input[i][0],650,posy_output[k][0])

root.mainloop()

b.create_connection()

root = tk.Tk()
root.title("Testing title")
root.geometry("1000x1000")

my_canvas = tk.Canvas(root, width=700, height=500, bg="white")
my_canvas.pack(pady=20)

nb_input = len(b.inputs)
posy_input = np.array([[np.linspace(50, 450, nb_input)[k], b.inputs[k].id_node] for k in range(nb_input)])

for k in range(len(posy_input)):
    my_canvas.create_oval(40, posy_input[k][0] + 10, 60, posy_input[k][0] - 10, fill="red")

nb_output = len(b.outputs)
posy_output = np.array([[np.linspace(50, 450, nb_output)[k], b.outputs[k].id_node] for k in range(nb_output)])

for k in range(len(posy_output)):
    my_canvas.create_oval(640, posy_output[k][0] + 10, 660, posy_output[k][0] - 10, fill="green")

for c in b.connections:
    i = np.where(posy_input[:, 1] == c.inputs)[0][0]
    k = np.where(posy_output[:, 1] == c.outputs)[0][0]
    my_canvas.create_line(50,posy_input[i][0],650,posy_output[k][0])

root.mainloop()