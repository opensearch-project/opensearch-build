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
parser.add_argument('manifest', type = argparse.FileType('r'), help="Absolute path of local manifest file.")
parser.add_argument('--component',nargs='?',help="Component name")
parser.add_argument('--type',nargs='?',help="Artifact type")
args = parser.parse_args()

manifest = BuildManifest.from_file(args.manifest)
basepath = os.path.dirname(args.manifest.name)
print("hello",basepath)

signer = Signer()
for component in manifest.components:
    if (not args.component) or ( args.component and component.name == args.component):
        print(f'signing {component.name}')
        for artifact_type in component.artifacts:
            if (not args.type) or (args.type and artifact_type == args.type):
                artifact_list = component.artifacts[artifact_type]
                for artifact in artifact_list:
                    location = os.path.join(basepath, artifact)
                    print("LOCATION=", location)
                    signer.sign(location)
                    signer.verify(location + ".asc")
signer.close()

print('Done.')
