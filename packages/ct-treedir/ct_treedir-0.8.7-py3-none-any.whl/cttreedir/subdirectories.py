import os

from .ignore import should_ignore

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