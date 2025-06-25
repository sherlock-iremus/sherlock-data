import os
import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--file_dir")
parser.add_argument("--cache")
args = parser.parse_args()

def create_or_edit_nakala_cache(folder_path, yaml_file_path):

    if not os.path.exists(yaml_file_path):
        with open(yaml_file_path, 'w') as yaml_file:
            yaml.dump({}, yaml_file)

    with open(yaml_file_path, 'r') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file) or {}

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            if file_name not in yaml_data:
                print(f"Ajout d'une nouvelle image : '{file_name}'.")
                yaml_data[file_name] = None

    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False)

folder_path = args.file_dir
yaml_file_path = args.cache
create_or_edit_nakala_cache(folder_path, yaml_file_path)
