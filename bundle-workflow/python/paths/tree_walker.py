import os

def walk(root):
    print(f'Walking tree from {root}')
    for dir, dirs, files in os.walk(root):
        for file_name in files:
            absolute_path = os.path.join(dir, file_name)
            relative_path = os.path.relpath(absolute_path, root)
            yield (os.path.realpath(absolute_path), relative_path)
