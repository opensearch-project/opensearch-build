# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import base64

import semver


def str_to_base64(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("utf-8")


def get_password(version: str, convert_to_base64: bool = False) -> str:
    # Starting in 2.12.0, demo configuration setup script requires a strong password
    password = "myStrongPassword123!" if semver.Version.parse(version).compare(semver.Version.parse('2.12.0')) != -1 else "admin"
    return str_to_base64(password) if convert_to_base64 else password
