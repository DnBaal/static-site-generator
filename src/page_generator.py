import os

from block_markdown import markdown_to_html_node


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()

    raise ValueError("No h1 header")


def generate_page(from_path, template_path, dst_path):
    print(f" * {from_path} {template_path} -> {dst_path}")

    with open(from_path, "r") as from_file, open(template_path) as template_file:
        md = from_file.read()
        template = template_file.read()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dst_dir_path = os.path.dirname(dst_path)
    if dst_dir_path and not os.path.exists(dst_dir_path):
        os.makedirs(dst_dir_path, exist_ok=True)

    try:
        with open(dst_path, "w") as f:
            f.write(template)
        print(f"Wrote to: {dst_path}")
    except IOError as e:
        print(f"Error writing to file {dst_path}: {e}")
