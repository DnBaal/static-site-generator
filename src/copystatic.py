import os
import shutil


def copy_files_recursive(src, dst):
    if not os.path.exists(src):
        raise Exception("No src directory")

    if not os.path.exists(dst):
        os.mkdir(dst)

    for filename in os.listdir(src):
        from_path = os.path.join(src, filename)
        dst_path = os.path.join(dst, filename)
        print(f" * {from_path} -> {dst_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dst)
        else:
            copy_files_recursive(from_path, dst_path)
