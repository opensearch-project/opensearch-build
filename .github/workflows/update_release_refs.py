import os
import re

# Define the folder where YAML files are located
folder_path = "1.3.15"  # Replace with the actual folder path

# Get the folder name and use it as the new version
new_version = os.path.basename(folder_path)

# Define a list of component names that should have the same version as 'OpenSearch' and 'common-utils'
same_version_components = ['OpenSearch', 'common-utils']

# Iterate through YAML files in the folder and update the 'ref' in each file
for filename in os.listdir(folder_path):
    if filename.endswith('.yml'):
        yaml_file = os.path.join(folder_path, filename)
        print(yaml_file)
        with open(yaml_file, 'r') as file:
            yaml_code = file.read()

        # for component_name in same_version_components:
            # Update the 'ref' for 'OpenSearch' and 'common-utils'
        ref_pattern = "ref: .*"
        print(re.findall(ref_pattern,yaml_code))
        updated_yaml = re.sub(ref_pattern, f"ref: tags/{new_version}", yaml_code)
        # # Update the 'ref' for other components
        # other_components_pattern = f"name: (?!{'|'.join(same_version_components)})\w+\n\s+ref: "
        # updated_yaml = re.sub(other_components_pattern, lambda match: match.group() + ".0", updated_yaml)

        # Save the updated content back to the file
        with open(yaml_file, 'w') as file:
            file.write(updated_yaml)

print(f"Ref values updated in the specified YAML files in the folder. New version: {new_version}")
