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
        self.__stdout_data__ = None
        self.__stderr_data__ = None

    def start(self, command, cwd):
        if self.started:
            raise ProcessStartedError(self.pid)

        self.stdout = tempfile.NamedTemporaryFile(mode="r+")
        self.stderr = tempfile.NamedTemporaryFile(mode="r+")

        self.process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True,
            stdout=self.stdout,
            stderr=self.stderr,
        )

    def terminate(self):
        if not self.started:
            raise ProcessNotStartedError()

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
            self.__stdout_data__ = self.stdout.read()
            self.stdout.close()
            self.stdout = None

        if self.stderr:
            self.__stderr_data__ = self.stderr.read()
            self.stderr.close()
            self.stderr = None

        self.return_code = self.process.returncode
        self.process = None

        return self.return_code

    @property
    def started(self):
        return True if self.process else False

    @property
    def pid(self):
        return self.process.pid if self.started else None

    @property
    def stdout_data(self):
        return self.stdout.read() if self.stdout else self.__stdout_data__

    @property
    def stderr_data(self):
        return self.stderr.read() if self.stderr else self.__stderr_data__


class ProcessStartedError(Exception):
    """
    Indicates that process already started.
    """

    def __init__(self, pid):
        self.pid = pid
        super().__init__(f"Process already started, pid: {pid}")


class ProcessNotStartedError(Exception):
    """
    Indicates that process has not started.
    """

    def __init__(self):
        super().__init__("Process has not started")
