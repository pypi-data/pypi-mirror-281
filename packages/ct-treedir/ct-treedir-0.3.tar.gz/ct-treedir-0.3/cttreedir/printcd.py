from .help import load_ignore_list, create_directory_tree

def run_printcd():
    ignore_file_path = '.treeignore'

    ignore_string = input("Enter custom .treeignore: ").strip()
    ignore_list = ignore_string.split(',') if ignore_string else load_ignore_list(ignore_file_path)

    author_string = input("Enter author name: ").strip()
    if not author_string:
        print("No author given, please author this document with you first name and last initial ending with a period.")
        return

    user_directory = input("Enter the directory path: ")

    create_directory_tree(user_directory, author_string, ignore_list)