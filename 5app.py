# app.py
# Generative Abstract Poster with CSV Palette
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

if not os.path.exists(PALETTE_FILE):
    df_init = pd.DataFrame([
        {"name":"sky", "r":0.4, "g":0.7, "b":1.0},
        {"name":"sun", "r":1.0, "g":0.8, "b":0.2},
        {"name":"forest", "r":0.2, "g":0.6, "b":0.3}
    ])
    df_init.to_csv(PALETTE_FILE, index=False)

def read_palette():
    return pd.read_csv(PALETTE_FILE)

def add_color(name, r, g, b):
    df = read_palette()
    df = pd.concat([df, pd.DataFrame([{"name":name,"r":r,"g":g,"b":b}])], ignore_index=True)
    df.to_csv(PALETTE_FILE, index=False)

def update_color(name, r=None, g=None, b=None):
    df = read_palette()
    if name in df["name"].values:
        idx = df.index[df["name"]==name][0]
        if r is not None: df.at[idx,"r"] = r
        if g is not None: df.at[idx,"g"] = g
        if b is not None: df.at[idx,"b"] = b
        df.to_csv(PALETTE_FILE, index=False)

def delete_color(name):
    df = read_palette()
    df = df[df["name"]!=name]
    df.to_csv(PALETTE_FILE, index=False)

# --- Functions ---
def get_palette_from_csv(k=6):
    df = read_palette()
    colors = df.sample(n=min(k,len(df)))
    return [(row.r, row.g, row.b) for idx, row in colors.iterrows()]

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

    # Add text labels
    plt.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=plt.gca().transAxes)
    plt.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=plt.gca().transAxes)

    plt.xlim(0,1)
    plt.ylim(0,1)

    st.pyplot(plt)
