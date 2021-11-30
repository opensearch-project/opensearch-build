# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess


def current_architecture() -> str:
    architecture = subprocess.check_output(["uname", "-m"]).decode().strip()
    if architecture == "x86_64":
        return "x64"
    elif architecture == "aarch64" or architecture == "arm64":
        return "arm64"
    else:
        raise ValueError(f"Unsupported architecture: {architecture}")


def current_platform() -> str:
    if os.name == "nt":
        return "windows"
    else:
        return subprocess.check_output(["uname", "-s"]).decode().strip().lower()
