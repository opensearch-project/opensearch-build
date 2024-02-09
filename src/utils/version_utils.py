# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import semver


def get_password(version: str) -> str:
    # Starting in 2.12.0, demo configuration setup script requires a strong password
    if semver.compare(version, '2.12.0') != -1:
        return "myStrongPassword123!"
    else:
        return "admin"
