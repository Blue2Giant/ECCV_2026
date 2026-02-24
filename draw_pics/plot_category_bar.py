import argparse

from draw_distribution import visualize_category_counts
"""
python /Users/leolan/Downloads/WorkSpace/ECCV/draw_pics/plot_category_bar.py \
  --json /Users/leolan/Downloads/WorkSpace/ECCV/draw_pics/style_cate.json \
  --out-dir /Users/leolan/Downloads/WorkSpace/ECCV/figures \
  --name style_category_distribution_gap15_bar1_vertical \
  --caption "" \
  --bar-thickness 1 \
  --row-gap 1.5 \
  --orientation vertical

python draw_pics/plot_category_bar.py \
  --json draw_pics/content_cate.json \
  --out-dir figures \
  --name content_category_distribution_vertical_gap15_bar1 \
  --caption "" \
  --bar-thickness 1 \
  --row-gap 1.5 \
  --orientation vertical
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", dest="json_path", required=True)
    parser.add_argument("--out-dir", dest="output_dir", default="figures")
    parser.add_argument("--name", dest="output_name", default="category_distribution")
    parser.add_argument("--top-k", dest="top_k", type=int, default=None)
    parser.add_argument("--caption", dest="caption", default=None)
    parser.add_argument("--row-gap", dest="row_gap", type=float, default=1.18)
    parser.add_argument("--bar-thickness", dest="bar_thickness", type=float, default=None)
    parser.add_argument("--orientation", dest="orientation", default="horizontal", choices=["horizontal", "vertical"])
    args = parser.parse_args()

    visualize_category_counts(
        args.json_path,
        output_dir=args.output_dir,
        output_name=args.output_name,
        top_k=args.top_k,
        caption=args.caption,
        row_gap=args.row_gap,
        bar_thickness=args.bar_thickness,
        orientation=args.orientation,
    )


if __name__ == "__main__":
    main()
