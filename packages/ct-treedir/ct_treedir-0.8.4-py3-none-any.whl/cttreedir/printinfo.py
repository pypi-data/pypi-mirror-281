import os
import getpass
from .helpers.info import override_info_tree

def run_printinfo():
    user_directory = input("Enter the directory path: ")

    absolute_directory = os.path.abspath(user_directory)

    if not getpass.getuser() == "root":
        print("Administrator required. Please try sudo.")
        return
    
    previous_versions_dir = os.path.join(absolute_directory, '.directory')
    if not os.path.exists(previous_versions_dir):
        os.makedirs(previous_versions_dir)

    override_info_tree(main_src=absolute_directory, previous_versions_dir=previous_versions_dir)
