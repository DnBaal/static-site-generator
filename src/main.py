import os
import shutil

from copystatic import copy_files_recursive
from page_generator import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
content_path = "./content/index.md"
template_path = "./template.html"


def main():
    print("deleting public dir")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public dir...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating html page in public dir...")
    generate_page(content_path, template_path, dir_path_public + "/index.html")


if __name__ == "__main__":
    main()
