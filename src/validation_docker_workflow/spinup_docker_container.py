# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import shutil
import subprocess
from subprocess import PIPE
from system.temporary_directory import TemporaryDirectory


yml_template = 'docker-compose.yml'
yml_template_location = './src/validation_docker_workflow/'

"""
This class is to spin up docker containers with the OS and OSD images specificed earlier.
It uses docker-compose to bring up docker containers. 
It returns True if containers are Up.
"""
class RunDocker():

    def inplace_change(filename, old_string, new_string):

        with open(filename) as f:
            s = f.read()
            if old_string not in s:
                print('"{old_string}" not found in {filename}.'.format(**locals()))
                return

        with open(filename, 'w') as f:
            print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
            s = s.replace(old_string, new_string)
            f.write(s)

    def run_container(OS_image, OSD_image, OS1_name, OS2_name, OSD_name):
        ## replace the placeholder in template docker-compose.yaml which is taken from sample in https://opensearch.org/docs/latest/opensearch/install/docker/#sample-docker-composeyml
        tmp_dir = TemporaryDirectory()
        shutil.copy2(yml_template_location + yml_template,tmp_dir.name)
        target_yml_file = tmp_dir.name + '/' + yml_template
        RunDocker.inplace_change(target_yml_file,'OS_IMAGE_PLACEHOLDER',OS_image)
        RunDocker.inplace_change(target_yml_file,'OSD_IMAGE_PLACEHOLDER',OSD_image)
        RunDocker.inplace_change(target_yml_file,'OS1_NAME',OS1_name)
        RunDocker.inplace_change(target_yml_file,'OS2_NAME',OS2_name)
        RunDocker.inplace_change(target_yml_file,'OSD_NAME_PLACEHOLDER',OSD_name)

        ## spin up containers
        docker_compose_up = 'docker-compose -f ' + target_yml_file + ' up -d'
        result = subprocess.run(docker_compose_up, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        
        return ( 'returncode=0' in (str(result)), target_yml_file)