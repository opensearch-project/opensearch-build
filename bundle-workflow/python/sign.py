#!/usr/bin/env python

import os
import subprocess as sp
import tempfile
import uuid
import argparse
from manifests.bundle_manifest import BundleManifest

parser = argparse.ArgumentParser(description = "Sign artifacts")
parser.add_argument('manifest', type = argparse.FileType('r'), help="Manifest file.")
args = parser.parse_args()

def sign(filename):
    signatureFile = filename + ".asc"
    signing_cmd = './opensearch-signer-client -i ' + filename + ' -o ' + signatureFile + ' -p pgp'
    sp.run(signing_cmd.split(),cwd='opensearch-signer-client/src')
    verify_cmd = 'gpg --verify-files ' + signatureFile
    sp.run(verify_cmd.split(),cwd='opensearch-signer-client/src')
    sp.run(['mv',signatureFile,'signed_artifacts/'])

manifest = BundleManifest.from_file(args.manifest)
output_dir = os.path.join(os.getcwd(), 'signed_artifacts')
os.makedirs(output_dir, exist_ok = True)
build_id = os.getenv('OPENSEARCH_BUILD_ID', uuid.uuid4().hex)

os.system('git clone https://github.com/opensearch-project/opensearch-signer-client.git')
os.system('cp ./config.cfg ./opensearch-signer-client/src/')
sp.run(['./bootstrap'],cwd='opensearch-signer-client/src')

print(f'Signing {manifest.build.name} into {output_dir}')
for component in manifest.components:
        print(f'signing {component.name}')
        sign(f'{component.location}')

os.system('rm -rf opensearch-signer-client')
print('Done.')
