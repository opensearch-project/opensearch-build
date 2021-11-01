# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess

import psutil  # type: ignore


class ProcessUtils:

    @staticmethod
    def terminate_process(self):
        parent = psutil.Process(self.process.pid)
        logging.debug("Checking for child processes")
        child_processes = parent.children(recursive=True)
        for child in child_processes:
            logging.debug(f"Found child process with pid {child.pid}")
            if child.pid != self.process.pid:
                logging.debug(f"Sending SIGKILL to {child.pid} ")
                child.kill()
        logging.info(f"Sending SIGTERM to PID {self.process.pid}")
        self.process.terminate()
        try:
            logging.info("Waiting for process to terminate")
            self.process.wait(10)
        except subprocess.TimeoutExpired:
            logging.info("Process did not terminate after 10 seconds. Sending SIGKILL")
            self.process.kill()
            try:
                logging.info("Waiting for process to terminate")
                self.process.wait(10)
            except subprocess.TimeoutExpired:
                logging.info("Process failed to terminate even after SIGKILL")
                raise
        finally:
            logging.info(f"Process terminated with exit code {self.process.returncode}")
            if self.stdout:
                with open(os.path.join(self.work_dir, self.stdout.name), "r") as stdout:
                    self.local_cluster_stdout = stdout.read()
                    self.stdout.close()
                    self.stdout = None
            if self.stderr:
                with open(os.path.join(self.work_dir, self.stderr.name), "r") as stderr:
                    self.local_cluster_stderr = stderr.read()
                self.stderr.close()
                self.stderr = None
            self.return_code = self.process.returncode
            self.process = None
