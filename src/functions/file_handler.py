import os
import shutil
import logging

def copy_files(src: str, dest: str) -> None:
    if not os.path.exists(src):
        raise ValueError(f"Given source path does not exist: {src}")
    
    logging.info(f"-> Reset {dest}")
    if os.path.exists(dest):
        # Intentionally remove the dest directory so that everything is copied over fresh
        shutil.rmtree(dest)
    os.makedirs(dest, exist_ok=True)

    items: list[str] = os.listdir(src)
    for i in items:
        src_path: str = os.path.join(src, i)
        try:
            if os.path.islink(src_path):
                logging.info(f"--> Copying symlink: {src_path}")
                shutil.copy2(src_path, os.path.join(dest, i), follow_symlinks=False)
            elif os.path.isfile(src_path):
                logging.info(f"--> Copying: {src_path}")
                shutil.copy2(src_path, os.path.join(dest, i))
            elif os.path.isdir(src_path):
                dest_subfolder: str = os.path.join(dest, i)
                copy_files(src_path, dest_subfolder)
            else:
                logging.warning(f"Skipping unsupported file type: {src_path}")
        except (PermissionError) as pe:
            # Log error and exit if a permission error occurs
            logging.warning(f"Encountered error with {src_path}: {pe}")
            raise pe
        except (OSError) as e:
            # Log error and exit if an OS error occurs
            logging.warning(f"Skipping {src_path} due to error: {e}")
            raise e

def read_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as src_file:
        src_contents: str = src_file.read()
        return src_contents
    
def write_file(path: str, contents: str) -> None:
    with open(path, 'w', encoding='utf-8') as file:
        file.write(contents)

def check_directory(file_path: str) -> None:
    if os.path.isdir(file_path):
        logging.info(f"{file_path} directory already exists")
    elif dir_path := os.path.dirname(file_path):
        os.makedirs(dir_path, exist_ok=True)