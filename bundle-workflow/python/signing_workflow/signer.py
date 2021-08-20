#!/usr/bin/env python

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0
import sys 

sys.path.insert(0,"../git")
from git.git_repository import GitRepository


'''
This class is responsible for signing an artifact using the OpenSearch-signer-client and verifying its signature.
The signed artifacts will be found in the same location as the original artifacts.
'''
class Signer:
    def __init__(self):
        self.git_repo = GitRepository("https://github.com/opensearch-project/opensearch-signer-client.git", "HEAD")
        self.git_repo.execute("./bootstrap", "src")
        self.git_repo.execute("rm config.cfg", "src")

    def sign(self, filename):
        signature_file = filename + ".asc"
        signing_cmd = ['./opensearch-signer-client', '-i', filename, '-o', signature_file, '-p', 'pgp']
        self.git_repo.execute(" ".join(signing_cmd), "src")

    def verify(self, filename):
        verify_cmd = ['gpg', '--verify-files', filename]
        self.git_repo.execute(" ".join(verify_cmd))
