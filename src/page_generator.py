import os
from pathlib import Path

from block_markdown import markdown_to_html_node


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()

    raise ValueError("No h1 header")


def generate_page(from_path, template_path, dst_path, basepath):
    print(f" * {from_path} {template_path} -> {dst_path}")

    with open(from_path, "r") as from_file, open(template_path) as template_file:
        md = from_file.read()
        template = template_file.read()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    dst_dir_path = os.path.dirname(dst_path)
    if dst_dir_path and not os.path.exists(dst_dir_path):
        os.makedirs(dst_dir_path, exist_ok=True)

    with open(dst_path, "w") as f:
        f.write(template)
    print(f"Wrote to: {dst_path}")


def generate_pages_recursive(dir_path_content, template_path, dst_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        raise ValueError("No src directory")

    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dst_path = os.path.join(dst_dir_path, filename)
        if os.path.isfile(from_path):
            dst_path = Path(dst_path).with_suffix(".html")
            generate_page(from_path, template_path, dst_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dst_path, basepath)
