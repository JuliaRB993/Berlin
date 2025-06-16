import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from ant_colony import AntColony

def load_berlin52():
    coords = []
    with open("data/berlin52.tsp") as f:
        for line in f:
            if line.strip().isdigit() or line.startswith("NODE_COORD_SECTION"):
                continue
            if "EOF" in line:
                break
            parts = line.strip().split()
            coords.append((float(parts[1]), float(parts[2])))
    return coords

def calc_dist_matrix(coords):
    size = len(coords)
    matrix = [[0.0]*size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            if i != j:
                matrix[i][j] = np.linalg.norm(np.array(coords[i]) - np.array(coords[j]))
    return matrix

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ACO - Problem Komiwojażera")
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.params = {"Ants": tk.IntVar(value=10),
                       "Best": tk.IntVar(value=5),
                       "Iterations": tk.IntVar(value=100),
                       "Decay": tk.DoubleVar(value=0.95),
                       "Alpha": tk.DoubleVar(value=1.0),
                       "Beta": tk.DoubleVar(value=2.0)}

        for i, (key, var) in enumerate(self.params.items()):
            ttk.Label(self.frame, text=key).grid(row=i, column=0, sticky="e")
            ttk.Entry(self.frame, textvariable=var).grid(row=i, column=1)

        ttk.Button(self.frame, text="Start", command=self.run_aco).grid(row=len(self.params), column=0, columnspan=2)

        self.canvas = None

    def run_aco(self):
        coords = load_berlin52()
        dist_matrix = calc_dist_matrix(coords)
        aco = AntColony(dist_matrix,
                        n_ants=self.params["Ants"].get(),
                        n_best=self.params["Best"].get(),
                        n_iterations=self.params["Iterations"].get(),
                        decay=self.params["Decay"].get(),
                        alpha=self.params["Alpha"].get(),
                        beta=self.params["Beta"].get())
        path, dist = aco.run()
        self.plot(coords, path, dist)

    def plot(self, coords, path, dist):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        fig, ax = plt.subplots()
        x = [coords[i][0] for i in range(len(coords))]
        y = [coords[i][1] for i in range(len(coords))]
        ax.scatter(x, y, color='red')
        for i, txt in enumerate(range(len(coords))):
            ax.annotate(txt, (x[i], y[i]))
        for frm, to in path:
            x0, y0 = coords[frm]
            x1, y1 = coords[to]
            ax.plot([x0, x1], [y0, y1], 'b')
        ax.set_title(f"Dystans: {dist:.2f}")
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()