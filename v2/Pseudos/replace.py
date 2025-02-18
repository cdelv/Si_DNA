import os
import shutil

def replace_in_file(file_path, old_string, new_string):
    with open(file_path, 'r') as file:
        file_data = file.read()
    new_data = file_data.replace(old_string, new_string)
    with open(file_path, 'w') as file:
        file.write(new_data)
    print(f"Processed: {file_path}")

def search_and_replace(directory, old_string, new_string):
    for root, _, files in os.walk(directory):
        for file_name in files:
            if not file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                replace_in_file(file_path, old_string, new_string)

if __name__ == "__main__":
    source_directory = "PBE"  # Original directory name
    new_directory = "VK"     # New directory name
    old_string = "pbr"
    new_string = "vkr"

    # Get the current working directory
    current_dir = os.getcwd()

    # Full paths for source and new directories
    source_path = os.path.join(current_dir, source_directory)
    new_path = os.path.join(current_dir, new_directory)

    # Copy the entire directory
    shutil.copytree(source_path, new_path)
    print(f"Copied {source_directory} to {new_directory}")

    # Perform string replacement in the new directory
    search_and_replace(new_path, old_string, new_string)

    print("String replacement completed in the new directory.")
