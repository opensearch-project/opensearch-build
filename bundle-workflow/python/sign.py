#!/usr/bin/env python

import os
import subprocess
import tempfile
import uuid
import argparse
from manifests.build_manifest import BuildManifest
from pprint import pprint
from pathlib import Path
from signing_workflow.signer import Signer

parser = argparse.ArgumentParser(description = "Sign artifacts")
parser.add_argument('manifest', type = argparse.FileType('r'), help="Manifest file.")
args = parser.parse_args()

manifest = BuildManifest.from_file(args.manifest)
basepath = os.path.abspath(os.path.join(__file__ ,"../../..")) + '/artifacts/'
signer = Signer()
for component in manifest.components:
        print(f'signing {component.name}')
        for key in component.artifacts:
            artifact_list = component.artifacts[key]
            for artifact in artifact_list:
                location = basepath + artifact 
                signer.sign(location)
                signer.verify(location + ".asc")
signer.close()

print('Done.')
