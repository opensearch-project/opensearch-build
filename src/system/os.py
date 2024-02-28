# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess


def current_architecture() -> str:
    architecture = subprocess.check_output(["uname", "-m"]).decode().strip()
    if architecture == "x86_64" or architecture == "amd64":
        return "x64"
    elif architecture == "aarch64" or architecture == "arm64":
        return "arm64"
    elif architecture == "ppc64le":
        return "ppc64le"
    else:
        raise ValueError(f"Unsupported architecture: {architecture}")


def current_platform() -> str:
    if os.name == "nt":
        return "windows"
    else:
        return subprocess.check_output(["uname", "-s"]).decode().strip().lower()


def deb_architecture(architecture: str) -> str:
    # This would convert arch from "current_architecture" to deb specific architecture alternatives

    deb_architecture_map = {
        "x64": "amd64",
        "arm64": "arm64",
    }

    return deb_architecture_map[architecture]


def rpm_architecture(architecture: str) -> str:
    # This would convert arch from "current_architecture" to rpm specific architecture alternatives

    rpm_architecture_map = {
        "x64": "x86_64",
        "arm64": "aarch64",
    }

    return rpm_architecture_map[architecture]
