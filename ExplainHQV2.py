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
                    mask[i]=False
                    break
    return mask

regions=[]
cur=X_sig.copy()
while len(cur)>0:
    mp=is_pareto(cur)
    Xp=cur[mp]
    regions.append(Xp)
    rem=np.ones(len(cur),bool)
    for r in Xp:
        cond=(cur[:,0]>=r[0])&(cur[:,1]<=r[1])&(cur[:,2]<=r[2])
        rem &= ~cond
    cur=cur[rem]

# =============================================
# 3. Global limits (requested)
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

point_x=[]
point_y=[]
point_z=[]
point_color=[]
point_label=[]

for i, reg in enumerate(regions):
    col = colors[i % len(colors)]
    fig.add_trace(go.Scatter3d(
        x=reg[:,0], y=reg[:,1], z=reg[:,2],
        mode="markers",
        marker=dict(size=4, color=col),
        name=f"HQ_{i+1}"
    ))
    for xi,yi,zi in reg:
        point_x.append(xi)
        point_y.append(yi)
        point_z.append(zi)
        point_color.append(col)
        point_label.append(f"{xi}_{yi}_{zi}")

# Hidden cub initially
fig.add_trace(go.Mesh3d(
    x=[0], y=[0], z=[0],
    i=[], j=[], k=[],
    color="#000000",
    opacity=0.25,
    visible=False,
    name="Cube"
))
CUBE_INDEX = len(fig.data)-1

# =============================================
# 5. Add buttons to choose point and toggle cube
# =============================================

buttons=[]
buttons.append(dict(
    label="Hide cube",
    method="restyle",
    args=[{"visible":[True]*(len(fig.data)-1) + [False]}]
))

# One button per point
for idx,(x0,y0,z0,col) in enumerate(zip(point_x,point_y,point_z,point_color)):

    # Cube vertices
    X = [x0, XRAY_MAX, XRAY_MAX, x0, x0, XRAY_MAX, XRAY_MAX, x0]
    Y = [SPIRAL_MIN, SPIRAL_MIN, y0, y0, SPIRAL_MIN, SPIRAL_MIN, y0, y0]
    Z = [SLICE_MIN, SLICE_MIN, SLICE_MIN, SLICE_MIN, z0, z0, z0, z0]

    I=[0,0,0,1,1,2,4,4,5,2,3,6]
    J=[1,2,3,2,5,3,5,6,4,6,7,7]
    K=[2,3,1,5,2,1,6,7,1,3,6,4]

    buttons.append(dict(
        label=f"Cube {point_label[idx]}",
        method="restyle",
        args=[
            {
            "x":[*[]]*1 + [X],  # update only cube
            "y":[*[]]*1 + [Y],
            "z":[*[]]*1 + [Z],
            "i":[*[]]*1 + [I],
            "j":[*[]]*1 + [J],
            "k":[*[]]*1 + [K],
            "color":[*[]]*1 + [col],
            "visible":[True]*(len(fig.data)-1) + [True]
            },
            [CUBE_INDEX]
        ]
    ))

fig.update_layout(
    title="Inequality Cubes (Select a point below)",
    updatemenus=[
        dict(type="dropdown",
             buttons=buttons,
             x=1.2, y=0.7)
    ],
    scene=dict(
        xaxis=dict(title="Xray", range=[0, 800]),
        yaxis=dict(title="Spiral Pitch", range=[0, 1.6]),
        zaxis=dict(title="Slice Thickness", range=[0, 2])
    ),
)


fig.write_html("HQ_ParetoCubesV2.html", include_plotlyjs="cdn")
print("Generated HQ_ParetoCubesV2.html")