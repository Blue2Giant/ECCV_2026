#sankey lora filter
import plotly.graph_objects as go
# sankey lora filter
import plotly.graph_objects as go
import os

labels = ["collected pool",  #0
          "FLUX based lora", #1 18000
          "Qwen based lora", #2 636
          "Illustrious based lora", #3 37000
          "Other model lora", #4 13000
          "FLUX content lora", #5 912
          "FLUX style lora", #6 1699
          "FLUX unstable lora", #7 15389
          "Qwen content lora", #8 29
          "Qwen style lora", #9 58
          "Qwen unstable lora", #10 549
          "Illustrious content lora", #11 6988
          "Illustrious style lora", #12 210
          "Illustrious unstable lora", #13 10802
          "FLUX content sampled by aesthetic score", #14 100
          "Illustrious content sampled by aesthetic score" #15 800
]

source = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 5, 11]
target = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
value  = [18000, 636, 37000, 13000, 912, 1699, 15389, 29, 58, 549, 6988, 210, 10802, 100, 800]

# 你给的主色系（不新增“新色”，只在这些色上做同色系变体）
node_hex = {
    "Content: Human":   "#2A9D8F",  # teal
    "Content: Animal":  "#4DA3D9",  # blue
    "Style: Line Art":  "#E9C46A",  # sand
    "Style: 2.5D":      "#F4A261",  # orange
    "Metric: StyleSim": "#8AB17D",  # green
    "Metric: ContentSim":"#6C83B5", # indigo
}

# --- 颜色工具：在同一主色系上派生更“合适”的变体 ---
def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    r, g, b = (max(0, min(255, int(x))) for x in rgb)
    return f"#{r:02X}{g:02X}{b:02X}"

def blend(c1, c2, t=0.5):
    """c = (1-t)*c1 + t*c2"""
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((r1*(1-t)+r2*t, g1*(1-t)+g2*t, b1*(1-t)+b2*t))

def lighten(c, t=0.25):
    return blend(c, "#FFFFFF", t)

def darken(c, t=0.12):
    return blend(c, "#000000", t)

def mute(c, t=0.45):
    # 往中灰靠一点，显得“不可用/不稳定”
    return blend(c, "#9AA0A6", t)

def hex_to_rgba(h, a=0.22):
    r, g, b = hex_to_rgb(h)
    return f"rgba({r},{g},{b},{a})"

# --- 规则：把你的业务节点映射到这套色系 ---
TEAL   = node_hex["Content: Human"]
BLUE   = node_hex["Content: Animal"]
SAND   = node_hex["Style: Line Art"]
ORANGE = node_hex["Style: 2.5D"]
GREEN  = node_hex["Metric: StyleSim"]
INDIGO = node_hex["Metric: ContentSim"]

def get_node_color(label: str) -> str:
    l = label.lower()

    # 先选“家族主色”
    if label == "collected pool":
        base = INDIGO
        return darken(lighten(base, 0.10), 0.06)
    elif label.startswith("FLUX"):
        base = TEAL
    elif label.startswith("Qwen"):
        base = BLUE
    elif label.startswith("Illustrious"):
        base = ORANGE
    elif label.startswith("Other"):
        base = SAND
    else:
        base = "#999999"

    # 再按语义做同色系变体
    if "sampled by aesthetic score" in l:
        # 用 green 强调“筛选/质量”，但保留家族色（更统一）
        return blend(base, GREEN, 0.45)
    if "style" in l:
        return lighten(base, 0.28)
    if "unstable" in l:
        return mute(base, 0.50)
    if "based lora" in l:
        return darken(base, 0.12)

    # 默认（content / 其他）
    return base

node_color = [get_node_color(l) for l in labels]

# 连线颜色：按 source 节点色 + 透明度
link_color = [hex_to_rgba(node_color[s], a=0.22) for s in source]

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
    width=980, height=560,
    paper_bgcolor="white", plot_bgcolor="white",
    font=dict(family="Helvetica, Arial, sans-serif", size=14),
    margin=dict(l=20, r=20, t=20, b=20),
)

# Save figure
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../figures")
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

save_path_svg = os.path.join(output_dir, "sankey_lora.svg")
save_path_png = os.path.join(output_dir, "sankey_lora.png")

# Requires kaleido package: pip install kaleido
try:
    fig.write_image(save_path_svg)
    fig.write_image(save_path_png, scale=2)
    print(f"Figures saved to {output_dir}")
except Exception as e:
    print(f"Error saving figures: {e}")

fig.show()