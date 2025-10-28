
PALETTE_FILE = "palette.csv"

# Initialize palette.csv if not exists
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
    print(f"Added {name}")

def update_color(name, r=None, g=None, b=None):
    df = read_palette()
    if name in df["name"].values:
        idx = df.index[df["name"]==name][0]
        if r is not None: df.at[idx,"r"] = r
        if g is not None: df.at[idx,"g"] = g
        if b is not None: df.at[idx,"b"] = b
        df.to_csv(PALETTE_FILE, index=False)
        print(f"Updated {name}")
    else:
        print(f"{name} not found")

def delete_color(name):
    df = read_palette()
    df = df[df["name"]!=name]
    df.to_csv(PALETTE_FILE, index=False)
    print(f"Deleted {name}")
