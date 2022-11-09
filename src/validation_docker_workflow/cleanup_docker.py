# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess
import os
from subprocess import PIPE

yml_template = 'docker-compose.yml'

"""
This class is used to stop&remove docker containers created at step 3, and remove docker-compose.yml in /tmp/.
"""
class CleanupDocker():

    def cleanup(OS1_name, OS2_name, OSD_name, target_yml_file):
        ## stop and remove containers
        docker_command = f'{"docker-compose -f"} {target_yml_file} {"stop"} {OS1_name} {OS2_name} {OSD_name} {"&&"} {"docker-compose -f"} {target_yml_file} {"rm -f"} {OS1_name} {OS2_name} {OSD_name}'
        result = subprocess.run(docker_command, shell=True, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        
        # remove docker-compose.yml from the tmp folder
        try:
            os.remove(target_yml_file)
        except OSError as e: 
            print ("Error: %s - %s." % (e.filename, e.strerror))

        return ( 'returncode=0' in (str(result)))