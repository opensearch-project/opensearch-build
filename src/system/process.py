# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess

import psutil  # type: ignore


def terminate(process, work_dir, stdout, stderr):
    parent = psutil.Process(process.pid)
    logging.debug("Checking for child processes")
    child_processes = parent.children(recursive=True)
    for child in child_processes:
        logging.debug(f"Found child process with pid {child.pid}")
        if child.pid != process.pid:
            logging.debug(f"Sending SIGKILL to {child.pid} ")
            child.kill()
    logging.info(f"Sending SIGTERM to PID {process.pid}")
    process.terminate()
    try:
        logging.info("Waiting for process to terminate")
        process.wait(10)
    except subprocess.TimeoutExpired:
        logging.info("Process did not terminate after 10 seconds. Sending SIGKILL")
        process.kill()
        try:
            logging.info("Waiting for process to terminate")
            process.wait(10)
        except subprocess.TimeoutExpired:
            logging.info("Process failed to terminate even after SIGKILL")
            raise
    finally:
        logging.info(f"Process terminated with exit code {process.returncode}")
        if stdout:
            with open(os.path.join(work_dir, stdout.name), "r") as opened_stdout:
                local_cluster_stdout = opened_stdout.read()
                stdout.close()
                stdout = None
        if stderr:
            with open(os.path.join(work_dir, stderr.name), "r") as opened_stderr:
                local_cluster_stderr = opened_stderr.read()
            stderr.close()
            stderr = None
        return_code = process.returncode

        return None, local_cluster_stderr, local_cluster_stdout, return_code
