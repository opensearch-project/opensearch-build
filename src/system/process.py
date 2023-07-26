# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import logging
import os
import subprocess
import tempfile
from typing import Any

import psutil


class Process:
    def __init__(self) -> None:
        self.process: subprocess.Popen[bytes] = None
        self.require_sudo: bool = False
        self.stdout: Any = None
        self.stderr: Any = None
        self.__stdout_data__: str = None
        self.__stderr_data__: str = None

    def start(self, command: str, cwd: str, require_sudo: bool = False) -> None:
        if self.started:
            raise ProcessStartedError(self.pid)

        self.stdout = tempfile.NamedTemporaryFile(mode="r+", delete=False, encoding='utf-8')
        self.stderr = tempfile.NamedTemporaryFile(mode="r+", delete=False, encoding='utf-8')

        self.require_sudo = require_sudo

        self.process = subprocess.Popen(
            command,
            cwd=cwd,
            shell=True,
            stdout=self.stdout,
            stderr=self.stderr,
        )

    def terminate(self) -> int:
        if not self.started:
            raise ProcessNotStartedError()

        parent = psutil.Process(self.process.pid)
        logging.debug("Checking for child processes")
        child_processes = parent.children(recursive=True)
        for child in child_processes:
            logging.debug(f"Found child process with pid {child.pid}")
            if child.pid != self.process.pid:
                logging.debug(f"Sending SIGKILL to {child.pid} ")
                child.kill() if self.require_sudo is False else subprocess.check_call(f"sudo kill -9 {child.pid}", shell=True)
        logging.info(f"Sending SIGKILL to PID {self.process.pid}")

        self.process.kill() if self.require_sudo is False else subprocess.check_call(f"sudo kill -9 {self.process.pid}", shell=True)

        logging.info(f"Process killed with exit code {self.process.returncode}")

        if self.stdout:
            self.stdout.seek(0)
            self.__stdout_data__ = self.stdout.read()
            self.stdout.flush()
            self.stdout.close()
            for proc in psutil.process_iter():
                try:
                    for item in proc.open_files():
                        if self.stdout.name == item.path:
                            raise Exception(f"stdout {item} is being used by process {proc}")
                except Exception as err:
                    logging.error(f"{err.args}")
            os.unlink(self.stdout.name)
            self.stdout = None

        if self.stderr:
            self.stderr.seek(0)
            self.__stderr_data__ = self.stderr.read()
            self.stderr.flush()
            self.stderr.close()
            for proc in psutil.process_iter():
                try:
                    for item in proc.open_files():
                        if self.stderr.name == item.path:
                            raise Exception(f"stderr {item} is being used by process {proc}")
                except Exception as err:
                    logging.error(f"{err.args}")
            os.unlink(self.stderr.name)
            self.stderr = None

        self.return_code = self.process.returncode
        self.process = None

        return self.return_code

    @property
    def started(self) -> bool:
        return True if self.process else False

    @property
    def pid(self) -> int:
        return self.process.pid if self.started else None

    @property
    def stdout_data(self) -> Any:
        return self.stdout.read() if self.stdout else self.__stdout_data__

    @property
    def stderr_data(self) -> Any:
        return self.stderr.read() if self.stderr else self.__stderr_data__


class ProcessStartedError(Exception):
    """
    Indicates that process already started.
    """

    def __init__(self, pid: int) -> None:
        self.pid = pid
        super().__init__(f"Process already started, pid: {pid}")


class ProcessNotStartedError(Exception):
    """
    Indicates that process has not started.
    """

    def __init__(self) -> None:
        super().__init__("Process has not started")
