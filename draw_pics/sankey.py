import plotly.graph_objects as go

labels = ["Content: Human", "Content: Animal",
          "Style: Line Art", "Style: 2.5D",
          "Metric: StyleSim", "Metric: ContentSim"]

source = [0, 0, 1, 2, 3]
target = [2, 3, 3, 4, 5]
value  = [80, 20, 50, 100, 70]

# 1) 节点配色：饱和但不刺眼（你也可以按“组”统一色系）
node_hex = {
    "Content: Human":   "#2A9D8F",  # teal
    "Content: Animal":  "#4DA3D9",  # blue
    "Style: Line Art":  "#E9C46A",  # sand
    "Style: 2.5D":      "#F4A261",  # orange
    "Metric: StyleSim": "#8AB17D",  # green
    "Metric: ContentSim":"#6C83B5", # indigo
}

def hex_to_rgba(h, a=0.22):
    h = h.lstrip("#")
    r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{a})"

node_color = [node_hex.get(l, "#999999") for l in labels]

# 2) 连线配色：按 source 节点上色 + 透明度（关键！）
link_color = [hex_to_rgba(node_hex.get(labels[s], "#999999"), a=0.20) for s in source]

fig = go.Figure(go.Sankey(
    arrangement="snap",
    node=dict(
        label=labels,
        color=node_color,
        pad=18,
        thickness=18,
        line=dict(color="rgba(0,0,0,0.25)", width=0.6),
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=link_color,
    )
))

fig.update_layout(
    width=900, height=520,
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(family="Helvetica, Arial, sans-serif", size=14),
    margin=dict(l=20, r=20, t=20, b=20),
)

fig.show()