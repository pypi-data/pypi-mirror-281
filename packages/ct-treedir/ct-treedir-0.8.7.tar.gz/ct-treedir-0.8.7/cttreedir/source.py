import os

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
    src_dir = os.path.join(new_version_dir, "%src")
    src_self_dir = os.path.join(src_dir, "@self")
    src_self_docs_dir = os.path.join(src_self_dir, "docs")
    src_self_npm_dir = os.path.join(src_self_dir, "npm")
    src_self_sync_dir = os.path.join(src_self_dir, "sync")

    # Ensure all directories are created
    os.makedirs(src_self_docs_dir, exist_ok=True)
    os.makedirs(src_self_npm_dir, exist_ok=True)
    os.makedirs(src_self_sync_dir, exist_ok=True)

    with open(os.path.join(src_self_docs_dir, 'i.md'), 'w') as file:
        file.write(src_contribute_content)

    with open(os.path.join(src_self_npm_dir, 'dependencies.md'), 'w') as file:
        file.write(src_dependencies_content)
    
    with open(os.path.join(src_self_npm_dir, 'package.md'), 'w') as file:
        file.write(src_package_content)