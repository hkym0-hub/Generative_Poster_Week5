# app.py
import random
import math
import numpy as np
import matplotlib.pyplot as plt
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

# --- Full Palette with Names ---
PALETTE = {
    "sky": (0.4,0.7,1.0), "sun": (1.0,0.8,0.2), "forest": (0.2,0.6,0.3), "ocean": (0.1,0.4,0.75),
    "sand": (0.9,0.75,0.5), "cloud": (0.95,0.95,0.95), "fire": (0.9,0.3,0.1), "ruby": (0.8,0.05,0.2),
    "gold": (1.0,0.85,0.0), "twilight": (0.3,0.15,0.5), "grass": (0.4,0.85,0.15), "brick": (0.65,0.2,0.15),
    "metal": (0.6,0.65,0.7), "grape": (0.5,0.2,0.7), "dawn": (0.95,0.6,0.5), "snow": (1.0,1.0,1.0),
    "coal": (0.1,0.1,0.1), "mint": (0.6,0.9,0.8), "berry": (0.8,0.3,0.5), "shadow": (0.3,0.3,0.35)
}

color_names = list(PALETTE.keys())
selected_color_name = st.sidebar.selectbox("Select a Base Color", color_names)
selected_color = PALETTE[selected_color_name]

generate = st.sidebar.button("🎲 Generate Poster")

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

    for i in range(n_layers):
        cx, cy = random.random(), random.random()
        rr = random.uniform(radius_min, radius_max)
        x, y = blob(center=(cx, cy), r=rr, wobble=random.uniform(wobble_min, wobble_max))
        # Use the selected color for all blobs
        plt.fill(x, y, color=selected_color, alpha=random.uniform(0.25, 0.6), edgecolor=(0,0,0,0))

    # Text labels
    plt.text(0.05, 0.95, f"Generative Poster • {selected_color_name}", fontsize=18, weight='bold', transform=plt.gca().transAxes)
    plt.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=plt.gca().transAxes)

    plt.xlim(0,1)
    plt.ylim(0,1)

    st.pyplot(plt)
