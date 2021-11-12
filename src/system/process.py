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
        self.has_started = False

    def start(self, command, cwd):
        if self.has_started:
            raise AssertionError("Cannot start a started process!")

        self.stdout = tempfile.NamedTemporaryFile()
        self.stderr = tempfile.NamedTemporaryFile()

        self.process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True,
            stdout=self.stdout,
            stderr=self.stderr,
        )

        self.has_started = True

    def terminate(self):
        if not self.has_started:
            raise AssertionError("Cannot terminate a unstarted process!")

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

        logging.info(f"Process killed with exit code {self.process.returncode}")

        if self.stdout:
            self.stdout_data = self.stdout.read()
            self.stdout.close()

        if self.stderr:
            self.stderr_data = self.stderr.read()
            self.stderr.close()

        self.return_code = self.process.returncode
        self.process = None
        self.has_started = False

        return self.return_code, self.stdout_data, self.stderr_data

    def started(self):
        return self.has_started

    @property
    def pid(self):
        return self.process.pid if self.has_started else None
