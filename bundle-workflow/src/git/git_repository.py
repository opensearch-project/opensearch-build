# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess
import tempfile


class GitRepository:
    """
    This class checks out a Git repository at a particular ref into an empty named directory (or temporary a directory if no named directory is given).
    Temporary directories will be automatically deleted when the GitRepository object goes out of scope; named directories will be left alone.
    Clients can obtain the actual commit ID by querying the "sha" attribute, and the temp directory name with "dir".
    """

    def __init__(self, url, ref, directory=None):
        self.url = url
        self.ref = ref
        if directory is None:
            self.temp_dir = tempfile.TemporaryDirectory()
            self.dir = self.temp_dir.name
        else:
            self.temp_dir = None
            self.dir = directory
            os.makedirs(self.dir, exist_ok=False)

        # Check out the repository
        self.execute("git init", True)
        self.execute(f"git remote add origin {self.url}", True)
        self.execute(f"git fetch --depth 1 origin {self.ref}", True)
        self.execute("git checkout FETCH_HEAD", True)
        self.sha = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.dir)
            .decode()
            .strip()
        )
        logging.info(f"Checked out {self.url}@{self.ref} into {self.dir} at {self.sha}")

    def execute(self, command, silent=False, subdirname=None):
        dirname = self.dir
        if subdirname:
            dirname = os.path.join(self.dir, subdirname)
        logging.info(f'Executing "{command}" in {dirname}')
        if silent:
            subprocess.check_call(
                command,
                cwd=dirname,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            subprocess.check_call(command, cwd=dirname, shell=True)
