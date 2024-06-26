import os
from .help import load_ignore_list, create_directory_tree, should_ignore

def list_subdirectories(parent_directory, ignore_list):
    try:
        # List all subdirectories
        subdirectories = [d for d in os.listdir(parent_directory) if os.path.isdir(os.path.join(parent_directory, d))]
        print("Initial subdirectories:", subdirectories)  # Debug statement

        # Filter subdirectories based on ignore list
        filtered_subdirectories = [d for d in subdirectories if not should_ignore(d, ignore_list)]
        print("Filtered subdirectories:", filtered_subdirectories)  # Debug statement

        return filtered_subdirectories
    except FileNotFoundError:
        print(f"Directory Not Found: {parent_directory}")
        return []
    except PermissionError:
        print(f"Permission Denied: {parent_directory}")
        return []

def select_subdirectories(subdirectories):
    print("Subdirectories:")
    for index, subdir in enumerate(subdirectories):
        print(f"{index}: {subdir}")

    selected_indices = input("Enter the indices you want generated: ").split(',')
    selected_indices = [int(i.strip()) for i in selected_indices if i.strip().isdigit()]

    return [subdirectories[i] for i in selected_indices if 0 <= i < len(subdirectories)]

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
