import os
import shutil

def copy_files(src: str, dest: str) -> None:
    if not os.path.exists(src):
        raise Exception(f"Given source path does not exist: {src}")
    
    print(f"-> Reset {dest}")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)

    items: list[str] = os.listdir(src)
    for i in items:
        src_path: str = os.path.join(src, i)
        if os.path.isfile(src_path):
            print(f"--> Copying: {src_path}")
            shutil.copy(src_path, dest)
        else:
            dest_subfolder: str = os.path.join(dest, i)
            copy_files(src_path, dest_subfolder)

def read_file(path: str) -> str:
    with open(path, 'r') as src_file:
        if src_file is None:
            raise Exception(f"File could not be read at {path}")
        src_contents: str = src_file.read()
        return src_contents
    
def write_file(path: str, contents: str) -> None:
    with open(path, 'w') as file:
        file.write(contents)

def check_directory(path: str) -> None:
    dir = os.path.dirname(path)
    os.makedirs(dir, 0o777, True)