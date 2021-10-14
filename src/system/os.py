# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import subprocess


def current_arch():
    arch = subprocess.check_output(["uname", "-m"]).decode().strip()
    if arch == "x86_64":
        return "x64"
    elif arch == "aarch64" or arch == "arm64":
        return "arm64"
    else:
        raise ValueError(f"Unsupported architecture: {arch}")


def current_platform():
    return subprocess.check_output(["uname", "-s"]).decode().strip().lower()
