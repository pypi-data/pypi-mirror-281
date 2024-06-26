import os
import datetime
import getpass
from .help import create_src, get_next_version_number

def run_printsrc():
    author_string = input("Enter author name: ").strip()
    if not author_string:
        print("No author given, please author this document with you first name and last initial ending with a period.")
        return

    user_directory = input("Enter the directory path: ")

    absolute_directory = os.path.abspath(user_directory)

    if not getpass.getuser() == "root":
        print("Administrator required. Please try sudo.")
        return
    
    previous_versions_dir = os.path.join(absolute_directory, '.directory')
    if not os.path.exists(previous_versions_dir):
        os.makedirs(previous_versions_dir)

    next_version = get_next_version_number(previous_versions_dir)
    today = datetime.datetime.today()

    new_version_dir = os.path.join(previous_versions_dir, next_version)
    if not os.path.exists(new_version_dir):
        os.makedirs(new_version_dir)

    create_src(next_version, author_string, today, new_version_dir)
