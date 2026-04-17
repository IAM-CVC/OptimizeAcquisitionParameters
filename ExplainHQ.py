import numpy as np
import pandas as pd
import plotly.graph_objects as go

# =============================================
# 1. Load data
# =============================================
df = pd.read_csv("Radiolung3Param.csv")

X = df[["XrayTh", "spiralTh", "sliceTh"]].values
p = df["p_val"].values
f = df["Freq"].values

mask = (p <= 0.05) & (f > 0)
X_sig = X[mask]

# =============================================
# 2. Pareto layers
# =============================================
def is_pareto(X):
    n=len(X)
    mask=np.ones(n,bool)
    for i in range(n):
        for j in range(n):
            if i!=j:
                if (X[j,0]>=X[i,0]) and (X[j,1]<=X[i,1]) and (X[j,2]<=X[i,2]) and \
                   ((X[j,0]>X[i,0]) or (X[j,1]<X[i,1]) or (X[j,2]<X[i,2])):
                    mask[i]=False; break
    return mask

regions=[]
cur=X_sig.copy()
num_regions = 1
while len(cur)>0:
    mp=is_pareto(cur)
    Xp=cur[mp]
    regions.append(Xp)
    rem=np.ones(len(cur),bool)
    print(f"HQ {num_regions}")
    print(f"--------------------------")
    for r in Xp:
        print(f"XrayTh  >= {r[0]}")
        print(f"SpiralTh <= {r[1]}")
        print(f"SliceTh <= {r[2]}")
        print(f"-----")
        cond=(cur[:,0]>=r[0])&(cur[:,1]<=r[1])&(cur[:,2]<=r[2])
        rem &= ~cond
    cur=cur[rem]
    num_regions += 1

# =============================================
# 3. Fixed limits
# =============================================
XRAY_MAX   = 800
SPIRAL_MIN = 0
SLICE_MIN  = 0

# =============================================
# 4. Build figure (points only)
# =============================================
colors = [
    "#D62728","#1F77B4","#2CA02C","#9467BD","#8C564B",
    "#E377C2","#7F7F7F","#BCBD22","#17BECF","#FF7F0E"
]

fig = go.Figure()

# Add all HQ point clouds
for i, reg in enumerate(regions):
    fig.add_trace(go.Scatter3d(
        x=reg[:, 0], y=reg[:, 1], z=reg[:, 2],
        mode="markers",
        marker=dict(size=4, color=colors[i % len(colors)], opacity=1.0),
        name=f"HQ_{i + 1}",
        hovertemplate="Xray>=%{x}<br>Spiral<=%{y}<br>Slice<=%{z}",
        visible=True
    ))

# =============================================
# 5. Generate ALL cubes but keep them hidden
# =============================================

cube_traces = []        # list of traces per HQ
hq_cube_trace_indices = []  # list of index lists

for ri, reg in enumerate(regions):
    col = colors[ri % len(colors)]
    group_indices = []   # cube traces belonging to HQ_ri

    for (x0,y0,z0) in reg:
        # cube vertices
        X = [x0, XRAY_MAX, XRAY_MAX, x0, x0, XRAY_MAX, XRAY_MAX, x0]
        Y = [SPIRAL_MIN, SPIRAL_MIN, y0, y0, SPIRAL_MIN, SPIRAL_MIN, y0, y0]
        Z = [SLICE_MIN, SLICE_MIN, SLICE_MIN, SLICE_MIN, z0, z0, z0, z0]

        I=[0,0,0,1,1,2,4,4,5,2,3,6]
        J=[1,2,3,2,5,3,5,6,4,6,7,7]
        K=[2,3,1,5,2,1,6,7,1,3,6,4]

        fig.add_trace(go.Mesh3d(
            x=X, y=Y, z=Z,
            i=I, j=J, k=K,
            color=col,
            opacity=0.2,
            visible=False,
            name=f"CUBE_HQ_{ri+1}"
        ))
        group_indices.append(len(fig.data)-1)

    hq_cube_trace_indices.append(group_indices)


# =============================================
# 6. MULTI-TOGGLE MENU FOR HQ CUBES
# =============================================

# Visibility initial:
# - Points always visible (len(regions) traces)
# - All cubes hidden
initial_visibility = [True]*len(regions)
for group in hq_cube_trace_indices:
    initial_visibility.extend([False]*len(group))

# Apply initial visibility
fig.update_traces(visible=True, selector=dict(type="scatter3d"))
fig.update_traces(visible=False, selector=dict(type="mesh3d"))

# Build buttons list
buttons = []

# 1) BUTTON: HIDE ALL CUBES
buttons.append(dict(
    label="Hide cubes",
    method="restyle",
    args=[{"visible": initial_visibility}]
))

# 2) ONE TOGGLE BUTTON PER HQ
#    Each button toggles only traces belonging to that HQ
for hi, group in enumerate(hq_cube_trace_indices):

    # indices of cube traces for this HQ
    cube_idxs = group

    buttons.append(dict(
        label=f"Toggle HQ_{hi+1}",
        method="restyle",
        args=[
            {"visible": None},   # required by Plotly API
            cube_idxs            # traces to toggle
        ],
        execute=True
    ))

# =============================================
# 7. LAYOUT: vertical button menu
# =============================================
fig.update_layout(
    title="Inequality Cubes — Multi HQ Selection",
    updatemenus=[
        dict(
            type="buttons",
            direction="down",
            showactive=True,
            buttons=buttons,
            x=1.20,
            y=0.75
        )
    ],
    scene=dict(
        xaxis=dict(title="Xray", range=[0,800]),
        yaxis=dict(title="Spiral", range=[0.5,1.6]),
        zaxis=dict(title="Slice", range=[0,2])
    )
)


# 8. Export
# =============================================
fig.write_html("HQ_ParetoCubes.html", include_plotlyjs="cdn")
print("Generated HQ_ParetoCubes.html")
