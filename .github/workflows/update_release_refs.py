import os
import sys
import yaml

folder_path = sys.argv[1]
# Define the folder where YAML files are located
# folder_path = f"/manifests/{new_version}"  # Replace with the actual folder path

# Get the folder name and use it as the new version
new_version = os.path.basename(folder_path)

# Define a list of component names that should have the same version as 'OpenSearch' and 'common-utils'
same_version_components = ['OpenSearch', 'common-utils']

# Iterate through YAML files in the folder and update the 'ref' in each file
for filename in os.listdir(folder_path):
    if filename.endswith('.yml'):
        yaml_file = os.path.join(folder_path, filename)
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
        for component in data.get('components', []):
            if component['name'] in same_version_components:
                ref = component.get('ref', 'Not found')
                component['ref'] = f'tags/{new_version}'
            else:
                component['ref'] = f'tags/{new_version}.0'
                
        with open(yaml_file, 'w') as file:
            yaml.dump(data, file)

print(f"Ref values updated in the specified YAML files in the folder. New version: {new_version}")