import os
import re
import shutil
import getpass
import datetime
from colorama import init

init()

def load_ignore_list(ignore_file):
    ignore_set = set()
    if os.path.exists(ignore_file):
        with open(ignore_file, 'r') as file:
            for line in file:
                pattern = line.strip()
                if pattern:
                    ignore_set.add(pattern)
    return ignore_set

def should_ignore(item, ignore_list):
    for ignore in ignore_list:
        if ignore.startswith('.') and item.endswith(ignore):
            return True
        elif ignore == item:
            return True
    return False

def natural_sort_key(s):
    """ Sort key function to sort strings by numerical content. """
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def list_files_recursively(directory, prefix='', file=None, base_directory=None, ignore_list=None):
    try:
        items = os.listdir(directory)
        items.sort(key=natural_sort_key)
    except PermissionError:
        file.write(f"{prefix}Permission Denied: {directory}\n")
        return
    except FileNotFoundError:
        file.write(f"{prefix}Directory Not Found: {directory}\n")
        return

    for index, item in enumerate(items):
        if should_ignore(item, ignore_list):
            continue
        item_path = os.path.join(directory, item)
        connector = '└──' if index == len(items) - 1 else '├──'
        file.write(f"{prefix}{connector} {item}\n")
        if os.path.isdir(item_path):
            extension = '    ' if index == len(items) - 1 else '│   '
            list_files_recursively(item_path, prefix + extension, file, base_directory, ignore_list)

def get_next_version_number(directory):
    versions = []
    for folder in os.listdir(directory):
        if re.match(r'\d{3}', folder) or folder == '000':
            versions.append(int(folder))
    
    if not versions:
        return '001'
    
    versions.sort()
    next_version = versions[-1] + 1
    if next_version == 1000:
        next_version = 0
    
    while True:
        version_str = f'{next_version:03d}'
        if not os.path.exists(os.path.join(directory, version_str)):
            return version_str
        next_version += 1
        if next_version == 1000:
            next_version = 0

def create_dir_info(previous_versions_dir):
    readme_info_path = os.path.join(previous_versions_dir, 'README.md')
    amend_path = os.path.join(previous_versions_dir, 'amendments.md')
    purpose_path = os.path.join(previous_versions_dir, 'purpose.md')
    purpose_url = input("Enter your full github repo url: ").strip()
    if not purpose_url:
        print("No github repo given, one is required to generate a README.")
        return
    readme_content = (
        f"# Directory Tree\n\n"
        f"This `.directory` folder contains editions for the working file structure of this particular project.\n\n"
        f"## File Structure Elements\n\n"
        f"When creating or deleting files within the project, the `tree.cwd` file keeps maintenance of the editions of those changes. If the most recently available tree generated in the src folder does not match with the overall structure of the push, it will be denied to ensure a preservation of possibly necessary content.\n\n"
        f"> Note: this is an attempt for our maintainers to recognize quickly during the publishing process if any critical files were removed in the changes made by a contributor. Read more in [purpose.md]({purpose_url}/blob/main/.directory/purpose.md)\n\n"
        f"## Getting Started\n\n"
        f"If this is the first time you are contributing, it would be helpful to familiarize yourself with the contents of this project, including the previous stages. The `GDTES/GFSES` can be found in submodules within this folder, following a sequence from 001-999.\n\n"
        f"In each of these stages there are `tree.cwd` files for the particular edition.\n\n"
        f"### GDTES/GFSES\n\n"
        f"The above uses these terms to abbreviate: `Generated General Directory Tree Edition Stages` or `Generated General File Structure Edition Stages`. Either the Generated or General is silent. File Structure is synonymous with Directory Tree in this specific definition.\n\n"
        f"### 001-999?\n\n"
        f"While this may not seem like a very large or even reasonable amount of available slots, there is a somewhat of a easy explanation. If all slots are filled, it is the duty of the next contributor to remove all past edition stages except for the last and start from 001 again.\n\n"
        f"The reason for this is because this is a record of the project file structure, not a record of the contents of any of those files directly. Therefore, it is not important to maintain every edition, and as long as the last edition used and the new edition needed for the contribution are present, the push should be smooth sailing.\n\n"
        f"#### What if there are issues deleting the stages?\n\n"
        f"You may need to contact a maintainer of this project, which should be found in the `package.json` or `README.md`, and request for them to remove these if you are unable to.\n\n"
        f"This may happen because ct-treedir is a sudo operation. If you are using this for the first time, make sure you are using sudo mode to remove or add contents to .directory.\n\n"
        f"### Authoring\n\n"
        f"Another important aspect of this is to keep a record of who has made significant changes to this project. If you do not author your tree generation, it will be canceled. Read more about authoring in the purpose.\n\n"
        f"#### Removing Files\n\n"
        f"This is typically the most critical action while using ct-treedir. If files are removed from the `GDT`, this can cause critical cascading failures for other dependents of this repository.\n\n"
        f"#### Adding Files\n\n"
        f"Typically a less severe action while using ct-treedir. If files are added to the `GDT`, it does not usually impact pre-existing code.\n\n"
        f"#### Modifying Files\n\n"
        f"Also a less severe action while using ct-treedir. If files are amended under the `GDT`, it sometimes can have an impact on pre-existing code. While this is something to consider, the main reason behind this system is to \"allow other repo's with this package installed to keep existing imports relative to the original locations\"; as a standard.\n\n"
        f"In this case (when it does have a cascading effect throughout dependent's imports), there are more steps to complete before finalizing any contributions. Please see [amendments.md]({purpose_url}/blob/main/.directory/amendments.md) for more info.\n\n"
        f"## Changesets\n\n"
        f"If you are generating a new tree within your contribution to account for added or removed files, please only version the package to a minor or major change, not patch.\n\n"
        f"If you are unfamiliar with how this package is versioned, please see [contributing.md]({purpose_url}/blob/main/contributing.md) under the \"Pull Request Process\" section.\n\n"
        f"### %src\n\n"
        f"Changesets can point to a `%src` folder which highlight more info about what was changed in the edition. The convention that should be used is `{{%src}}: .directory/###/%/...`.\n\n"
        f"Descriptions for changesets and commits can be used in addition to this flag, which should simply point maintainers and further contributors to information you wish not to add into `CHANGELOG.md` or a commit message; Especially if the information is too large, the `%src` convention is preferred.\n"
    )
    amend_content = (
        f"# Amendments\n\n"
        f"When modifying files within this package, if it has a potential for breaking cascading effects throughout dependents, please follow the below disclaimers and guidelines.\n\n"
        f"### Patch vs. Minor/Major Disclaimer\n\n"
        f"If by refactoring the code, you have not added or removed any base functionality from the package (at it's most recent published version)--but instead only made improvements or fixed a small non-critical issue...\n\n"
        f"- Use a `patch` version changeset\n\n"
        f"If you did add or remove base functionality, please also follow the extended section guidelines below, and...\n\n"
        f"- Use at least a `minor` version changeset\n\n"
        f"### Generation Disclaimer\n\n"
        f"Even if you do not add or remove base functionality, it is still strongly advised to execute the directory tree generation to ensure everything is still operating correctly and to make any necessary changes to `/%src`.\n\n"
        f"#### %src\n\n"
        f"You may encounter letters concatenated with the normal edition stages convention (001-999), so **###(a-z)**. This is to indicate that changes were made to the `%src` files without anything changing in `tree.cwd`.\n\n"
        f"If you are enacting this process, you'll notice that all sub-editions will be reconsolidated into the main edition folder. In other words, any given ### folder will contain all of its corresponding ###(a-z) subfolders. By default, a second process will start at '###b', placing the original `%src` in '###a', and copying the `tree.cwd` to both.\n\n"
        f"## Guidelines\n\n"
        f"1. Make desired changes to the package.\n\n"
        f"2. Compare all changes to previous versions of the package, using the latest `src/tree.cwd`.\n\n"
        f"> If you are having problems viewing the tree, please install the available VSCode support extension [here](https://marketplace.visualstudio.com/items?itemName=alexgraham08.ct-treedir).\n\n"
        f"3. Make sure you have read the above disclaimers, the [purpose.md]({purpose_url}/blob/main/.directory/purpose.md), and also the [README.md]({purpose_url}/blob/main/.directory/README.md).\n\n"
        f"4. Decide if the compared changes are a patch, minor, or major change to the package. This step is subjective, but the above disclaimers may describe which path is best to take.\n\n"
        f"5. Generate the `GDTE` by using the [ct-treedir package on pip](https://pypi.org/project/ct-treedir/).\n\n"
        f"```zsh\n"
        f"pip install ct-treedir\n"
        f"ct-treedir generate (--parent/--only-src)\n"
        f"```\n\n"
        f"6. Verify that the generated folders and files are accurate to depict the changes that you have made to the repository.\n\n"
        f"7. Create a changeset with optional pointer using the `{{%src}}` convention.\n\n"
        f"8. Commit and push your changes.\n"
    )
    purpose_content = (
        f"# Directory Tree Purpose\n\n"
        f"The reason why directory tree is used in this project is to <!-- enter reason -->\n"
    )

    with open(readme_info_path, 'w') as file:
        file.write(readme_content)
    with open(amend_path, 'w') as file:
        file.write(amend_content)
    with open(purpose_path, 'w') as file:
        file.write(purpose_content)

def create_src(next_version, author_string, today, new_version_dir):
    src_contribute_content = (
        f"Contributions made in .directory/{next_version} were by: {author_string}.\n\n"
        f"~ Auto generated at {today.strftime('%Y-%m-%d')}T{today.strftime('%H:%M:%S')}\n"
    )
    src_dependencies_content = (
        f"<!-- add dependencies for this project here -->\n"
    )
    src_package_content = (
        f"<!-- add package info for this project here -->\n"
    )
    with open(os.path.join(new_version_dir, '%src/@self/docs/i.md'), 'w') as file:
        file.write(src_contribute_content)

    with open(os.path.join(new_version_dir, '%src/@self/npm/dependencies.md'), 'w') as file:
        file.write(src_dependencies_content)
    
    with open(os.path.join(new_version_dir, '%src/@self/npm/package.md'), 'w') as file:
        file.write(src_package_content)

def create_directory_tree(user_directory, author_string, ignore_list=None):
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

    original_tree_path = os.path.join(absolute_directory, 'tree.cwd')
    version_tree_path = os.path.join(new_version_dir, 'tree.cwd')

    today = datetime.datetime.today()
    tree_content = (
        "Generated Directory Tree\n"
        f"{today.strftime('%Y-%m-%d')}T{today.strftime('%H:%M:%S')}\n"
        f".directory/{next_version}/tree.cwd\n\n"
        f"{author_string}\n\n"
    )

    with open(original_tree_path, 'w') as file:
        file.write(tree_content)
        override_info_tree(previous_versions_dir)

        src_dir = os.path.join(absolute_directory, '%src')
        src_exports_dir = os.path.join(src_dir, '@exports')
        src_self_dir = os.path.join(src_dir, '@self')
        if not os.path.exists(src_exports_dir):
            os.makedirs(src_exports_dir)
        if not os.path.exists(os.path.join(src_exports_dir, "exports.md")):
            with open(os.path.join(src_exports_dir, "exports.md"), 'w') as file:
                file.write(f"<!-- define the convention for project exports here -->\n")
        if not os.path.exists(src_exports_dir):
            os.makedirs(src_exports_dir)
        if not os.path.exists(src_dir):
            os.makedirs(src_dir)
        if not os.path.exists(src_self_dir):
            os.makedirs(src_self_dir)
            os.makedirs(os.path.join(src_self_dir, "docs"))
            os.makedirs(os.path.join(src_self_dir, "npm"))
            os.makedirs(os.path.join(src_self_dir, "sync"))
        if not os.path.exists(os.path.join(src_self_dir, "self.md")):
            with open(os.path.join(src_self_dir, "self.md"), 'w') as file:
                file.write(
                    f"# Self Directory\n<!-- Template -->\n\n"
                    f"This directory holds information regarding npm, documentation, and synchronization between `GDTES`.\n\n"
                    f"### Docs\n\n- i.md\n\n"
                    f"### NPM\n\n- dependencies.md\n- packages.md\n\n"
                    f"### Sync\n\n- added.sync\n- deleted.sync\n- changed.sync\n\n"
                )
        create_src(next_version, author_string, today, new_version_dir)
        list_files_recursively(absolute_directory, '', file, absolute_directory, ignore_list)
    
    shutil.copyfile(original_tree_path, version_tree_path)

    print(f"The tree has been written to: '{original_tree_path}'.")

def override_info_tree(previous_versions_dir):
    check_override_info = input("Do you wish to override the .directory info? [Y/n]: ").strip().lower()
    if not os.path.exists(os.path.join(previous_versions_dir, 'amendments.md')):
        print("File already exists, please remove 'amendments.md' and try again.")
        if check_override_info == 'y':
            return
    if not os.path.exists(os.path.join(previous_versions_dir, 'purpose.md')):
        print("File already exists, please remove 'purpose.md' and try again.")
        if check_override_info == 'y':
            return
    if not os.path.exists(os.path.join(previous_versions_dir, 'README.md')):
        print("File already exists, please remove 'README.md' and try again.")
        if check_override_info == 'y':
            return
    generate_info_tree(previous_versions_dir)

def generate_info_tree(previous_versions_dir):
    info_tree_generation = input("Would you like to include a directory info template? [Y/n]: ").strip().lower()
    if(info_tree_generation == "y"):
            create_dir_info(previous_versions_dir)