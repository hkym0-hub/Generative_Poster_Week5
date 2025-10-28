# app.py
# Generative Abstract Poster with Full CSV Palette
import os
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# --- Streamlit UI ---
st.set_page_config(page_title="Generative Abstract Poster", layout="centered")
st.title("🎨 Generative Abstract Poster")
st.caption("Week 2 • Arts & Advanced Big Data")

# --- Sidebar Controls ---
st.sidebar.header("🎛️ Controls")
n_layers = st.sidebar.slider("Number of Layers", 3, 20, 8)
random_seed = st.sidebar.number_input("Random Seed (for reproducibility)", value=0, step=1)

wobble_min = st.sidebar.slider("Minimum Wobble", 0.0, 0.5, 0.05, 0.01)
wobble_max = st.sidebar.slider("Maximum Wobble", 0.0, 0.5, 0.25, 0.01)
radius_min = st.sidebar.slider("Minimum Radius", 0.05, 0.5, 0.15, 0.01)
radius_max = st.sidebar.slider("Maximum Radius", 0.05, 0.5, 0.45, 0.01)

generate = st.sidebar.button("🎲 Generate Poster")

# --- Palette CSV ---
PALETTE_FILE = "palette.csv"

# Initialize palette.csv with your colors if not exists
if not os.path.exists(PALETTE_FILE):
    df_init = pd.DataFrame([
        {"Name":"sky","R":0.4,"G":0.7,"B":1.0},
        {"Name":"sun","R":1.0,"G":0.8,"B":0.2},
        {"Name":"forest","R":0.2,"G":0.6,"B":0.3},
        {"Name":"ocean","R":0.1,"G":0.4,"B":0.75},
        {"Name":"sand","R":0.9,"G":0.75,"B":0.5},
        {"Name":"cloud","R":0.95,"G":0.95,"B":0.95},
        {"Name":"fire","R":0.9,"G":0.3,"B":0.1},
        {"Name":"ruby","R":0.8,"G":0.05,"B":0.2},
        {"Name":"gold","R":1.0,"G":0.85,"B":0.0},
        {"Name":"twilight","R":0.3,"G":0.15,"B":0.5},
        {"Name":"grass","R":0.4,"G":0.85,"B":0.15},
        {"Name":"brick","R":0.65,"G":0.2,"B":0.15},
        {"Name":"metal","R":0.6,"G":0.65,"B":0.7},
        {"Name":"grape","R":0.5,"G":0.2,"B":0.7},
        {"Name":"dawn","R":0.95,"G":0.6,"B":0.5},
        {"Name":"snow","R":1.0,"G":1.0,"B":1.0},
        {"Name":"coal","R":0.1,"G":0.1,"B":0.1},
        {"Name":"mint","R":0.6,"G":0.9,"B":0.8},
        {"Name":"berry","R":0.8,"G":0.3,"B":0.5},
        {"Name":"shadow","R":0.3,"G":0.3,"B":0.35}
    ])
    df_init.to_csv(PALETTE_FILE, index=False)

def read_palette():
    return pd.read_csv(PALETTE_FILE)

def get_palette_from_csv(k=6):
    df = read_palette()
    colors = df.sample(n=min(k, len(df)))
    return [(row.R, row.G, row.B) for idx, row in colors.iterrows()]

# --- Blob Function ---
def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    angles = np.linspace(0, 2 * math.pi, points)
    radii = r * (1 + wobble * (np.random.rand(points) - 0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- Generate Artwork ---
if generate or random_seed >= 0:
    random.seed(random_seed)
    np.random.seed(random_seed)
    plt.figure(figsize=(7,10))
    plt.axis('off')
    plt.gca().set_facecolor((0.98, 0.98, 0.97))

    palette = get_palette_from_csv(k=6)
    for i in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(radius_min, radius_max)
        x, y = blob(center=(cx, cy), r=rr, wobble=random.uniform(wobble_min, wobble_max))
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        plt.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0))

    # Text labels
    plt.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=plt.gca().transAxes)
    plt.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=plt.gca().transAxes)

    plt.xlim(0,1)
    plt.ylim(0,1)

    st.pyplot(plt)
