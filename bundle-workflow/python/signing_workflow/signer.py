#!/usr/bin/env python

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

import os
import subprocess
import tempfile
import uuid
import argparse

'''
This class is responsible for signing an artifact using the OpenSearch-signer-client and verifying its signature.
The signed artifacts will be found in the same location as the original artifacts.
'''
class Signer:
    def __init__(self):
        subprocess.check_output(["git","clone","https://github.com/opensearch-project/opensearch-signer-client.git"])
        subprocess.check_output(["./bootstrap"],cwd='opensearch-signer-client/src')
        subprocess.check_output(["rm","config.cfg"],cwd='opensearch-signer-client/src')

    def sign(self, filename):
        signatureFile = filename + ".asc"
        basepath = os.path.basename(filename)
        signing_cmd=['./opensearch-signer-client', '-i', filename, '-o', signatureFile, '-p', 'pgp']
        subprocess.check_output(signing_cmd,cwd="opensearch-signer-client/src")

    def verify(self, filename):
        verify_cmd = ['gpg', '--verify-files',filename]
        subprocess.check_output(verify_cmd, cwd="opensearch-signer-client/src")

    def close(self):
        subprocess.run(["rm","-rf","opensearch-signer-client"])

