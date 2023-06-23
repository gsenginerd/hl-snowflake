"""The File Util module provides helper functions for the file system."""
import os
from pathlib import Path


def get_project_root(path: str, project_root_folder_name: str) -> str:
    """
    This function returns the path of the project root folder given a path and the name of the project
    root folder.
    
    :param path: The path parameter is a string representing the path to a file or directory
    :type path: str
    :param project_root_folder_name: The name of the folder that represents the root of the project
    :type project_root_folder_name: str
    :return: the path of the project root folder, which is the parent folder that has the name specified
    in the `project_root_folder_name` parameter.
    """
    if Path(path).parts[-1] == project_root_folder_name:
        return os.getcwd()
    
    for parent in Path(path).parents:
        if parent.parts[-1] == project_root_folder_name:
            return parent.as_posix()
