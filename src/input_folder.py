import os
from pathlib import Path
from typing import List

def _rec_file_creator(dir_path: Path, root_dir: Path, file_paths: List[str], flat: bool) -> None:
    """Helper function to recursively walk through directories and collect file paths"""
    for item in dir_path.iterdir():
        if item.is_dir(): #if a directory then mark it with 'dir%'
            rel_path = "dir%/" + str(item.relative_to(root_dir))
            file_paths.append(rel_path)
            _rec_file_creator(item, root_dir, file_paths, flat)

        elif item.is_file(): #if a directory then mark it with 'file%'
            rel_path = "file%/" + (str(item.relative_to(root_dir)) if not flat else str(item.name))
            file_paths.append(rel_path)

def create_file_list(dir_path: str, flat_download: bool) -> List[str]:
    """
    Recursively create a list of all file and folder paths inside dir_path
    Each folder starts with 'dir%' and each file with 'file%'
    """
    root_dir = Path(dir_path).resolve()
    file_paths: List[str] = []

    _rec_file_creator(root_dir, root_dir, file_paths, flat_download)

    return file_paths
