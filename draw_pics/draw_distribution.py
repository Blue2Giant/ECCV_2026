'''
keyword_count_rearranged.json文件大概是：
{"余少群":680,"刘亦菲":32678,"刘烨":3126,"王晓晨":5059,"胡歌":18247,"陈晓":6951,"李晟":15620,"黄宥明":1486,"张翰":10952,"何晟铭":2811,"黎一萱":440,"张嘉益":4074,"郭麒麟":4337,"金晨":4671,"晏紫东":1251,"杨幂":30086,"白宇":6527.......................
从中统计出所有出现次数在指定范围内的演员
再id_name_tar_mapping.json中找到包含他们名字组合的names
该json文件大概是：
local_mappings.append({
    "id": base_name,
    "name": names,
    "tar_path": tar_path  # Store relative path to save memory
})
其中names是一个列表，找到names中只有在指定范围内的演员名字组合
再找到所有包含但是不止包含指定范围内的演员名字组合
统计个数

python /Users/leolan/Downloads/WorkSpace/ECCV/draw_pics/draw_distribution.py \
  --json /Users/leolan/Downloads/WorkSpace/ECCV/draw_pics/style_cate.json \
  --out-dir /Users/leolan/Downloads/WorkSpace/ECCV/figures \
  --name style_category_distribution \
  --caption "" \
'''


import json
import os
from tqdm import tqdm

import matplotlib.pyplot as plt

def visualize_category_counts(
    category_count_file,
    output_dir="figures",
    output_name="category_distribution",
    top_k=None,
    caption=None,
    row_gap=1.18,
    orientation="horizontal",
    bar_thickness=None,
):
    with open(category_count_file, "r", encoding="utf-8") as f:
        category_count = json.load(f)

    items = [(str(k), float(v)) for k, v in category_count.items()]
    items.sort(key=lambda x: x[1], reverse=True)
    if top_k is not None:
        items = items[: int(top_k)]

    labels = [k for k, _ in items]
    values = [v for _, v in items]

    import textwrap
    wrapped_labels = [
        "\n".join(textwrap.wrap(l, width=18, break_long_words=False, break_on_hyphens=False))
        for l in labels
    ]
    max_line_len = max((max((len(s) for s in wl.split("\n")), default=0) for wl in wrapped_labels), default=0)
    max_lines = max((len(wl.split("\n")) for wl in wrapped_labels), default=1)

    palette = [
        "#001219",
        "#005F73",
        "#0A9396",
        "#94D2BD",
        "#E9D8A6",
        "#EE9B00",
        "#CA6702",
        "#BB3E03",
        "#AE2012",
        "#9B2226",
    ]
    cmap = plt.cm.colors.LinearSegmentedColormap.from_list("custom_cmap", palette, N=256)
    n = max(1, len(values))
    colors = [cmap(1.0 - (i / max(1, n - 1))) for i in range(n)]

    font_family = ["Avenir Next", "Avenir", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]

    plt.style.use("default")
    orientation = str(orientation).lower().strip()
    if orientation not in {"horizontal", "vertical"}:
        orientation = "horizontal"

    gap = float(row_gap)
    gap = max(0.85, min(2.8, gap))

    if bar_thickness is not None:
        bar_thickness = float(bar_thickness)
        bar_thickness = max(0.10, min(gap * 0.92, bar_thickness))

    if orientation == "horizontal":
        fig_height = max(4.6, min(12.0, 0.52 * len(values) * gap + 1.6))
        fig_width = 7.4
    else:
        fig_width = max(6.4, min(14.0, 0.55 * len(values) * gap + 1.8))
        fig_height = max(4.8, min(10.5, 3.8 + 0.18 * max_lines))

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor="white")
    ax.set_facecolor("white")

    if orientation == "horizontal":
        bar_height = bar_thickness if bar_thickness is not None else min(0.72, max(0.22, gap * 0.60))
        y = [i * gap for i in range(len(values))]
        ax.barh(y, values, color=colors, edgecolor="none", height=bar_height)
        ax.set_yticks(y)
        ax.set_yticklabels(
            wrapped_labels, fontfamily=font_family, fontsize=12.5, fontweight="bold", ha="right"
        )
        for t in ax.get_yticklabels():
            t.set_linespacing(1.18)
        ax.invert_yaxis()

        ax.set_xlabel("Count", fontfamily=font_family, fontsize=18, fontweight="bold")
        ax.tick_params(axis="x", labelsize=10, colors="#333333")
        ax.tick_params(axis="y", length=0, pad=8, colors="#111111")
    else:
        bar_width = bar_thickness if bar_thickness is not None else min(0.72, max(0.22, 0.60 / gap))
        x = [i * gap for i in range(len(values))]
        ax.bar(x, values, color=colors, edgecolor="none", width=bar_width)
        ax.set_xticks(x)
        ax.set_xticklabels(wrapped_labels, fontfamily=font_family, fontsize=12, fontweight="bold")
        for t in ax.get_xticklabels():
            t.set_linespacing(1.08)
        ax.set_ylabel("Count", fontfamily=font_family, fontsize=18, fontweight="bold")
        ax.tick_params(axis="y", labelsize=10, colors="#333333")
        ax.tick_params(axis="x", length=0, pad=10, colors="#111111")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#333333")
    ax.spines["bottom"].set_color("#333333")
    if orientation == "horizontal":
        ax.xaxis.grid(True, color="#dddddd", linestyle="--", alpha=0.7)
        ax.yaxis.grid(False)
    else:
        ax.yaxis.grid(True, color="#dddddd", linestyle="--", alpha=0.7)
        ax.xaxis.grid(False)

    if caption:
        fig.text(
            0.5,
            0.02,
            caption,
            ha="center",
            va="bottom",
            fontfamily=font_family,
            fontsize=14,
            fontweight="bold",
        )

    if orientation == "horizontal":
        left = max(0.14, min(0.26, 0.08 + 0.008 * max_line_len))
        bottom = 0.16 if caption else 0.10
        fig.subplots_adjust(left=left, right=0.98, top=0.96, bottom=bottom)
    else:
        bottom = max(0.22, min(0.45, 0.12 + 0.06 * max_lines))
        bottom = bottom + (0.06 if caption else 0.0)
        fig.subplots_adjust(left=0.10, right=0.98, top=0.94, bottom=bottom)

    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)
    png_path = os.path.join(output_dir, f"{output_name}.png")
    svg_path = os.path.join(output_dir, f"{output_name}.svg")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")
    fig.savefig(svg_path, bbox_inches="tight")
    plt.close(fig)

    return png_path, svg_path

def read_ndjson_line_by_line(filepath):
    """Read a newline-delimited JSON file line by line."""
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            # Skip comments and empty lines
            line = line.strip()
            if line.startswith('//') or not line:
                continue
            try:
                obj = json.loads(line)
                data.append(obj)
            except json.JSONDecodeError as e:
                print(f"Error parsing line: {line[:50]}...")
                print(f"Error details: {e}")
    return data


def get_actors_in_range(keyword_count_file, min_count=0, max_count=200):
    """
    从keyword_count_rearranged.json文件中获取出现次数在指定范围内的演员
    """
    with open(keyword_count_file, 'r', encoding='utf-8') as f:
        keyword_count = json.load(f)
    
    actors_in_range = {actor: count for actor, count in keyword_count.items() 
                      if min_count <= count <= max_count}
    return actors_in_range

def get_actor_combinations(id_name_mapping_file, target_actors):
    """
    从id_name_tar_mapping.json文件中获取：
        - 只包含目标范围内演员名字组合的case个数
        - 包含目标范围内演员名字，但不止包含目标范围内演员名字组合的case个数
    """
    count_target_only = 0
    count_target_and_more = 0
    count_other = 0
    if type(target_actors) == dict:
        target_actors_set = set(target_actors.keys())
    else:
        target_actors_set = set(target_actors)

    # 用一个集合来记录count_target_only的演员名字组合
    target_only_set = set()

    # 统计人数为1的data sample占比
    count_only_one = 0
    
    json_dict = read_ndjson_line_by_line(id_name_mapping_file)
            
    for item in tqdm(json_dict, desc="Processing actor combinations"):
        names = item['name']
        # 如果names中的名字都在target_actors中，并且名字大于1个
        if all(name in target_actors_set for name in names) and len(names) > 1:
            count_target_only += 1
            target_only_set.update(names)
        # 如果names中有名字在target_actors中，但不止包含target_actors中的名字
        elif any(name in target_actors_set for name in names):
            count_target_and_more += 1
        else:
            count_other += 1
        # 统计人数为1的data sample占比
        if len(names) == 1:
            count_only_one += 1

    
    return count_target_only, count_target_and_more, count_other, target_only_set, count_only_one

def visualize_actor_counts(keyword_count_file, output_image='stat/actor_count_distribution.png', min_count=None, max_count=None):
    """
    Create a visualization of actor appearances sorted from smallest to largest
    with count of appearances on the y-axis, using an aesthetically pleasing color palette.
    """
    import matplotlib.font_manager as fm
    
    # 直接指定字体文件路径
    eurostile_bold = fm.FontProperties(fname="/home/i-xuhengyuan/.local/share/fonts/eurostile/Eurostile_Bold.otf")
    
    # Load all actor counts
    with open(keyword_count_file, 'r', encoding='utf-8') as f:
        keyword_count = json.load(f)
    
    # Sort actors by count (ascending order)
    sorted_counts = sorted(keyword_count.values())
    
    # Define color palette from provided hex codes
    palette = ['#001219', '#005F73', '#0A9396', '#94D2BD', '#E9D8A6', 
               '#EE9B00', '#CA6702', '#BB3E03', '#AE2012', '#9B2226']
    
    # Create gradient colors for bars based on position
    num_bars = len(sorted_counts)
    cmap = plt.cm.colors.LinearSegmentedColormap.from_list('custom_cmap', palette, N=256)
    colors = [cmap(i/num_bars) for i in range(num_bars)]
    
    # Calculate statistics
    min_val = min(sorted_counts)
    max_val = max(sorted_counts)
    median_val = sorted_counts[len(sorted_counts)//2]
    
    # Set style - no grid background
    plt.style.use('default')
    
    # Create figure with transparent background
    fig, ax = plt.subplots(figsize=(8, 6), facecolor='none')
    ax.set_facecolor('none')
    
    # Create bar chart with gradient colors
    bars = ax.bar(range(len(sorted_counts)), sorted_counts, width=1.0, 
                 color=colors, edgecolor='none', linewidth=0, alpha=1)
    
    # Enhance the plot - make borders thinner
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#333333')
    ax.spines['bottom'].set_color('#333333')
    
    # Add minimal grid with improved styling
    ax.yaxis.grid(color='#dddddd', linestyle='--', alpha=0.5)
    
    # Format y-axis labels with 'k' suffix and make much sparser
    from matplotlib.ticker import FuncFormatter, MaxNLocator
    def thousands_formatter(x, pos):
        return f'{int(x/1000)}k'
    ax.yaxis.set_major_formatter(FuncFormatter(thousands_formatter))
    
    # Make Y ticks sparser - only show a few major ticks
    ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
    
    # Remove x-tick labels and make y-tick labels larger
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax.tick_params(axis='y', colors='#333333')
        
    # Apply Eurostile font to y tick labels
    for label in ax.get_yticklabels():
        label.set_fontproperties(eurostile_bold)
        label.set_fontsize(30)  # 增大到80pt
    # Set y-label with much larger font size and Eurostile font
    ax.set_ylabel('Appearance Count', fontsize=40, color='#333333', fontproperties=eurostile_bold)
    
    # Add statistics directly on plot with larger font
    ax.text(len(sorted_counts)*0.05, max_val*0.95, 
           f'Range: {min_val} to {max_val} ', 
           fontsize=35, color='#333333', fontproperties=eurostile_bold)
    
    # Add median line with annotation
    ax.axhline(y=median_val, color=palette[5], linestyle='-', alpha=0.7, linewidth=3)
    ax.text(len(sorted_counts)*0.05, median_val*1.05, f'Median: {median_val}', 
           fontsize=35, color='#333333', fontproperties=eurostile_bold)
    
    # Highlight the range if provided
    if min_count is not None and max_count is not None:
        ax.axhspan(min_count, max_count, alpha=0.2, color='green')
        ax.text(len(sorted_counts)*0.7, (min_count + max_count)/2, 
               f'Selected Range: {min_count}-{max_count}', 
               fontsize=35, color='green', fontproperties=eurostile_bold)
    
    # Set x-label with larger font
    ax.set_xlabel('Celebrities', fontsize=40, color='#333333', fontproperties=eurostile_bold)
    
    # Tighter layout with reduced margins
    plt.tight_layout(pad=1.0)
    plt.savefig(output_image, dpi=300, bbox_inches='tight', transparent=True)
    print(f"Actor count distribution visualization saved to: {output_image}")
    
    # Close the figure to free memory
    plt.close()

def main():
    keyword_count_file = 'stat/cn_keyword_count_rearranged.json'
    id_name_mapping_file = 'stat/cn_id_name_tar_mapping.json'
    
    # 获取出现次数在指定范围内的演员
    min_count = 1000
    max_count = 1500
    actors_in_range = get_actors_in_range(keyword_count_file, min_count, max_count)
    print(f"出现次数在{min_count}-{max_count}范围内的演员有: {actors_in_range}")
    print(f"一共{len(actors_in_range)}个演员名字")
    
    # 获取演员组合的个数
    count_range_only, count_range_and_more, count_other, range_only_set, count_only_one = get_actor_combinations(id_name_mapping_file, actors_in_range)
    
    print(f"只包含在{min_count}-{max_count}范围内演员名字组合且长度大于1的case个数: {count_range_only}")
    print(f"包含在{min_count}-{max_count}范围内演员名字，但不止包含这个范围演员名字组合的case个数: {count_range_and_more}")
    print(f"其他case个数: {count_other}")
    print(f"只包含在{min_count}-{max_count}范围内演员名字组合的演员有: {range_only_set}，一共{len(range_only_set)}个演员名字")
    # 百分比显示
    print(f"统计人数为1的data sample占比: {count_only_one / count_other:.2%}")

    # 用新的range_only_set来统计
    count_range_only, count_range_and_more, count_other, range_only_set_new, count_only_one = get_actor_combinations(id_name_mapping_file, range_only_set)
    print(f"只包含范围内组合演员名字组合的case个数: {count_range_only}")
    print(f"包含范围内组合演员名字，但不止包含范围内组合演员名字组合的case个数: {count_range_and_more}")
    print(f"其他case个数: {count_other}")
    print(f"DEBUG: 前后两个range_only_set的长度是否相等: {len(range_only_set) == len(range_only_set_new)}")

    # save the range_only_set to a file
    output_file = f'stat/actors_in_range_{min_count}_{max_count}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(list(range_only_set), f, ensure_ascii=False, indent=4)
    print(f"范围内演员集合已保存到文件: {output_file}")

    # visualize_actor_counts(keyword_count_file, f'stat/eu_actor_count_distribution_{min_count}_{max_count}.pdf', 
    #                        min_count=min_count, max_count=max_count)
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path", default=None)
    parser.add_argument("--out-dir", dest="output_dir", default="figures")
    parser.add_argument("--name", dest="output_name", default="category_distribution")
    parser.add_argument("--top-k", dest="top_k", type=int, default=None)
    parser.add_argument("--caption", dest="caption", default=None)
    parser.add_argument("--row-gap", dest="row_gap", type=float, default=1.18)
    parser.add_argument("--orientation", dest="orientation", default="horizontal")
    parser.add_argument("--bar-thickness", dest="bar_thickness", type=float, default=None)
    args, _ = parser.parse_known_args()

    if args.json_path:
        visualize_category_counts(
            args.json_path,
            output_dir=args.output_dir,
            output_name=args.output_name,
            top_k=args.top_k,
            caption=args.caption,
            row_gap=args.row_gap,
            orientation=args.orientation,
            bar_thickness=args.bar_thickness,
        )
    else:
        main()
