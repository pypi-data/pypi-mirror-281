import os 

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