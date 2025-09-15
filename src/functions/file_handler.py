import os
import shutil

def copy_files(src, dest):
    if not os.path.exists(src):
        raise Exception(f"Given source path does not exist: {src}")
    
    if os.path.exists(dest):
        shutil.rmtree(dest)

    print(f"-> Reset {dest}")
    os.mkdir(dest)

    items = os.listdir(src)
    for i in items:
        src_path = os.path.join(src, i)
        if os.path.isfile(src_path):
            print(f"--> Copying: {src_path}")
            shutil.copy(src_path, dest)
        else:
            dest_subfolder = os.path.join(dest, i)
            copy_files(src_path, dest_subfolder)