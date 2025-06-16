import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from ant_colony import AntColony

def load_berlin52():
    coords = []
    reading_coords = False
    with open("data/berlin52.tsp") as f:
        for line in f:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                reading_coords = True
                continue
            if "EOF" in line:
                break
            if reading_coords and line:
                parts = line.split()
                if len(parts) >= 3:
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

def plot_path(coords, path, dist):
    fig, ax = plt.subplots()
    x = [p[0] for p in coords]
    y = [p[1] for p in coords]
    ax.scatter(x, y, color='red')
    for i, (xi, yi) in enumerate(coords):
        ax.annotate(str(i+1), (xi, yi))
    for frm, to in path:
        x0, y0 = coords[frm]
        x1, y1 = coords[to]
        ax.plot([x0, x1], [y0, y1], 'b')
    ax.set_title(f"Dystans: {dist:.2f}")
    st.pyplot(fig)

def main():
    st.title("ACO – Problem Komiwojażera (berlin52)")
    coords = load_berlin52()
    dist_matrix = calc_dist_matrix(coords)

    st.sidebar.header("Parametry algorytmu")
    ants = st.sidebar.slider("Liczba mrówek", 5, 100, 20)
    best = st.sidebar.slider("Liczba najlepszych mrówek", 1, ants, 5)
    iterations = st.sidebar.slider("Liczba iteracji", 10, 500, 100)
    decay = st.sidebar.slider("Parowanie feromonów", 0.1, 1.0, 0.95)
    alpha = st.sidebar.slider("Wpływ feromonów (α)", 0.1, 5.0, 1.0)
    beta = st.sidebar.slider("Wpływ odległości (β)", 0.1, 5.0, 2.0)

    if st.button("Uruchom ACO"):
        with st.spinner("Obliczanie trasy..."):
            aco = AntColony(dist_matrix, ants, best, iterations, decay, alpha, beta)
            path, dist = aco.run()
            plot_path(coords, path, dist)

if __name__ == "__main__":
    main()