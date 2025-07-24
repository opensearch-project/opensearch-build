# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess
from pathlib import Path
from typing import Any, List

from git.git_commit import GitCommit
from system.temporary_directory import TemporaryDirectory


class GitRepository:
    dir: str
    """
    This class checks out a Git repository at a particular ref into an empty named directory (or temporary a directory if no named directory is given).
    Temporary directories will be automatically deleted when the GitRepository object goes out of scope; named directories will be left alone.
    Clients can obtain the actual commit ID by querying the "sha" attribute, and the temp directory name with "dir".
    """

    def __init__(self, url: str, ref: str, directory: str = None, working_subdirectory: str = None) -> None:
        self.url = url
        self.ref = ref
        if directory is None:
            self.temp_dir = TemporaryDirectory()
            self.dir = os.path.realpath(self.temp_dir.name)
        else:
            self.temp_dir = None
            self.dir = directory
            os.makedirs(self.dir, exist_ok=False)
        self.working_subdirectory = working_subdirectory
        self.__checkout__()

    def __enter__(self) -> 'GitRepository':
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        if self.temp_dir:
            self.temp_dir.__exit__(exc_type, exc_value, exc_traceback)

    def __checkout__(self) -> None:
        self.execute_silent("git init", self.dir)
        self.execute_silent(f"git remote add origin {self.url}", self.dir)
        self.execute_silent(f"git fetch --depth 1 origin {self.ref}", self.dir)
        self.execute_silent("git checkout FETCH_HEAD", self.dir)
        self.sha = self.output("git rev-parse HEAD", self.dir)
        logging.info(f"Checked out {self.url}@{self.ref} into {self.dir} at {self.sha}")

    @property
    def working_directory(self) -> str:
        if self.working_subdirectory:
            return os.path.join(self.dir, self.working_subdirectory)
        else:
            return self.dir

    @classmethod
    def stable_ref(self, url: str, ref: str) -> List[str]:
        results = subprocess.check_output(f"git ls-remote {url} {ref}", shell=True).decode().strip().split("\t")
        return results if len(results) > 1 else [ref, ref]
        
    @classmethod
    def _compare_versions(cls, version1: str, version2: str) -> int:
        """
        Compare two version strings.
        
        Args:
            version1: First version string (e.g., '2.9.0')
            version2: Second version string (e.g., '2.10.0')
            
        Returns:
            -1 if version1 < version2, 0 if version1 == version2, 1 if version1 > version2
        """
        try:
            # Split version strings into components
            v1_parts = version1.split('.')
            v2_parts = version2.split('.')
            
            for i in range(len(v1_parts)):
                # Extract numeric parts (handle cases like '2.0.0-rc1')
                v1_num = v1_parts[i].split('-')[0]
                v2_num = v2_parts[i].split('-')[0]
                
                # Convert to integers for comparison
                try:
                    v1_int = int(v1_num)
                    v2_int = int(v2_num)
                    
                    if v1_int < v2_int:
                        return -1
                    elif v1_int > v2_int:
                        return 1
                except ValueError:
                    # If conversion fails, compare as strings
                    if v1_num < v2_num:
                        return -1
                    elif v1_num > v2_num:
                        return 1
                
                # If numeric parts are equal but one has a suffix like '-rc1'
                if '-' in v1_parts[i] and '-' not in v2_parts[i]:
                    return -1  # Version with suffix is considered lower
                elif '-' not in v1_parts[i] and '-' in v2_parts[i]:
                    return 1   # Version without suffix is considered higher
            
            # All components are equal
            return 0
        except Exception as e:
            logging.warning(f"Error comparing versions {version1} and {version2}: {e}")
            # Default to string comparison if parsing fails
            return -1 if version1 < version2 else (0 if version1 == version2 else 1)

    def execute_silent(self, command: str, cwd: str = None) -> None:
        cwd = cwd or self.working_directory
        logging.info(f'Executing "{command}" in {cwd}')
        subprocess.check_call(
            command,
            cwd=cwd,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def output(self, command: str, cwd: str = None) -> str:
        cwd = cwd or self.working_directory
        logging.info(f'Executing "{command}" in {cwd}')
        return subprocess.check_output(command, cwd=cwd, shell=True).decode().strip()

    def execute(self, command: str, cwd: str = None) -> None:
        cwd = cwd or self.working_directory
        logging.info(f'Executing "{command}" in {cwd}')
        subprocess.check_call(command, cwd=cwd, shell=True)

    def path(self, subdirname: str = None) -> Path:
        dirname = self.dir
        if subdirname:
            dirname = os.path.join(self.dir, subdirname)
        return Path(dirname)

    def log(self, after: str) -> List[GitCommit]:
        result = []
        cmd = f'git log --date=short --after={after} --pretty=format:"%h %ad"'
        log = self.output(cmd).split("\n")
        for line in log:
            if len(line) == 0:
                continue
            parts = line.split(" ")
            result.append(GitCommit(parts[0], parts[1]))
        return result
