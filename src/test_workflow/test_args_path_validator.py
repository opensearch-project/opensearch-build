# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


import os

import validators  # type:ignore


class TestArgsPathValidator:

    @classmethod
    def validate(cls, path: str) -> str:
        return path if validators.url(path) else os.path.realpath(path)
