import os

from helpers.ignore import load_ignore_list
from helpers.directory import create_directory_tree
from helpers.subdirectories import list_subdirectories, select_subdirectories

def run_lsprintcd():
    ignore_file_path = '.treeignore'

    ignore_string = input("Enter custom .treeignore: ").strip()
    ignore_list = ignore_string.split(',') if ignore_string else []
    ignore_list.extend(load_ignore_list(ignore_file_path))

    print("Final ignore list:", ignore_list)  # Debug statement

    author_string = input("Enter author name: ").strip()
    if not author_string:
        print("No author given, please author this document with your first name and last initial ending with a period.")
        return

    parent_directory = input("Enter the parent directory: ")
    subdirectories = list_subdirectories(parent_directory, ignore_list)

    if not subdirectories:
        print("No subdirectories found or all are ignored.")
    else:
        selected_subdirectories = select_subdirectories(subdirectories)

        for subdirectory in selected_subdirectories:
            user_directory = os.path.join(parent_directory, subdirectory)
            create_directory_tree(user_directory, author_string, ignore_list)

if __name__ == "__main__":
    run_lsprintcd()
