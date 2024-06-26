import os
import getpass
from .help import generate_info_tree, get_next_version_number

def run_printinfo():
    user_directory = input("Enter the directory path: ")

    absolute_directory = os.path.abspath(user_directory)

    if not getpass.getuser() == "root":
        print("Administrator required. Please try sudo.")
        return
    
    previous_versions_dir = os.path.join(absolute_directory, '.directory')
    if not os.path.exists(previous_versions_dir):
        os.makedirs(previous_versions_dir)

    next_version = get_next_version_number(previous_versions_dir)

    new_version_dir = os.path.join(previous_versions_dir, next_version)
    if not os.path.exists(new_version_dir):
        os.makedirs(new_version_dir)

    generate_info_tree(new_version_dir)
