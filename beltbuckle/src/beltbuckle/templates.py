import os
import shutil
import re
from fnmatch import fnmatch

_template_root = "beltbuckle"

def replace_in_file(file_path, template_string, replacement_string):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()

        updated_contents = re.sub(template_string, replacement_string, file_contents)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_contents)
    except UnicodeDecodeError:
        print(f"Skipping binary file: {file_path}")

def read_gitignore(src_dir):
    gitignore_file = os.path.join(src_dir, ".gitignore")
    ignore_patterns = []

    if os.path.exists(gitignore_file):
        with open(gitignore_file, "r") as file:
            for line in file:
                line = line.strip()
                if not line.startswith("#") and line:
                    ignore_patterns.append(line)

    return ignore_patterns

def is_ignored(file_path, ignore_patterns):
    return any(fnmatch(file_path, pattern) for pattern in ignore_patterns)

def process_files(src_dir, dest_dir, template_string, replacement_string, ignore_patterns):
    for root, _, files in os.walk(src_dir):
        for f in files:
            src_file_path = os.path.join(root, f)
            relative_path = os.path.relpath(src_file_path, src_dir)
            if is_ignored(relative_path, ignore_patterns):
                continue

            dest_file_path = os.path.join(dest_dir, re.sub(template_string, replacement_string, relative_path))
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)

            shutil.copy2(src_file_path, dest_file_path)
            replace_in_file(dest_file_path, template_string, replacement_string)

def copy_and_replace(src_dir, dest_dir, template_string, replacement_string):
    shutil.rmtree(dest_dir, ignore_errors=True)
    os.makedirs(dest_dir)

    ignore_patterns = read_gitignore(src_dir)
    process_files(src_dir, dest_dir, template_string, replacement_string, ignore_patterns)

    dest_parent = os.path.dirname(dest_dir)
    new_dest_dir = os.path.join(dest_parent, re.sub(template_string, replacement_string, os.path.basename(dest_dir)))
    shutil.move(dest_dir, new_dest_dir)
