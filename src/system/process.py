# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import subprocess
import tempfile

import psutil  # type: ignore


class Process:
    def __init__(
        self
    ):
        self.process = None
        self.stdout = None
        self.stderr = None

    def start(self, command, cwd):
        self.stdout = tempfile.NamedTemporaryFile()
        self.stderr = tempfile.NamedTemporaryFile()

        self.process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True,
            stdout=self.stdout,
            stderr=self.stderr,
        )

    def terminate(self):
        parent = psutil.Process(self.process.pid)
        logging.debug("Checking for child processes")
        child_processes = parent.children(recursive=True)
        for child in child_processes:
            logging.debug(f"Found child process with pid {child.pid}")
            if child.pid != self.process.pid:
                logging.debug(f"Sending SIGKILL to {child.pid} ")
                child.kill()
        logging.info(f"Sending SIGKILL to PID {self.process.pid}")
        
        self.process.kill()
    
        logging.info(f"Process terminated with exit code {self.process.returncode}")
        if self.stdout:
            with open(self.stdout.name) as stdout:
                self.stdout_data = stdout.read()
                
        if self.stderr:
            with open(self.stderr.name) as stderr:
                self.stderr_data = stderr.read()

        self.return_code = self.process.returncode
        self.process = None

        return self.return_code, self.stdout_data, self.stderr_data

    @property
    def pid(self):
        return self.process.pid if self.process else None

    @property
    def stdout_x(self):
        return self.stdout

    @property
    def stderr_x(self):
        return self.stderr
