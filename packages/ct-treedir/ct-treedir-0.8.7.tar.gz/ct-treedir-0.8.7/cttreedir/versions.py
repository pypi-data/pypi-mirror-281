import os
import re

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

def create_new_version_directory(previous_versions_dir):
    # Creates a new version directory inside .directory
    next_version = get_next_version_number(previous_versions_dir)
    new_version_dir = os.path.join(previous_versions_dir, next_version)
    if not os.path.exists(new_version_dir):
        os.makedirs(new_version_dir)
    return new_version_dir