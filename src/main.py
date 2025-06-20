import os
import shutil
import sys

from copystatic import copy_files_recursive
from page_generator import generate_pages_recursive

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"
DIR_PATH_CONTENT = "./content"
DIR_PATH_DOCS = "./docs"
TEMPLATE_PATH = "./template.html"


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else "/"
    print("deleting docs dir...")
    if os.path.exists(DIR_PATH_DOCS):
        shutil.rmtree(DIR_PATH_DOCS)

    print("Copying static files to docs dir...")
    copy_files_recursive(DIR_PATH_STATIC, DIR_PATH_DOCS)

    print("Generating html content...")
    generate_pages_recursive(DIR_PATH_CONTENT, TEMPLATE_PATH, DIR_PATH_DOCS, basepath)


if __name__ == "__main__":
    main()
